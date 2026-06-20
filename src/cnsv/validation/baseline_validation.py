from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS, HORIZONS, clean_payload
from cnsv.utils.io import ensure_parent
from cnsv.validation.leakage_checks import contains_forbidden_validation_key
from cnsv.validation.metrics import compare_b2_vs_b1, summarize_prediction_rows
from cnsv.validation.walk_forward import MODEL_IDS, purged_rows, run_walk_forward_validation

STAGE = "V1.2.2_baseline_validation"


def build_validation_registry() -> list[dict[str, Any]]:
    return [
        {
            "stage": STAGE,
            "validation_id": "walk_forward_distribution_validation",
            "models": list(MODEL_IDS),
            "horizons": list(HORIZONS),
            "purged_sample_mode": "every_horizon_step",
            "is_trade_signal": False,
        }
    ]


def run_baseline_validation(data_bundle: dict[str, Any], gate: dict[str, Any], horizons: tuple[int, ...] = HORIZONS) -> dict[str, Any]:
    wf = run_walk_forward_validation(data_bundle, gate, horizons)
    standard = _metrics_by_model_horizon(wf["rows"])
    purged = _metrics_by_model_horizon(purged_rows(wf["rows"]))
    metrics = {"standard_walk_forward_metrics": standard, "purged_walk_forward_metrics": purged}
    b2_vs_b1 = compare_b2_vs_b1(metrics)
    quality = evaluate_validation_quality(metrics, wf["leakage_checks"], wf["rows"], b2_vs_b1)
    manifest = data_bundle.get("data_manifest") or {}
    payload = {
        "meta": {
            "system": "CNSV",
            "version": "1.2.2",
            "stage": STAGE,
            "report_type": "baseline_validation_report",
            "ts_code": "600150.SH",
            "name": "中国船舶",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "latest_trade_date": manifest.get("latest_trade_date", ""),
            "is_trade_signal": False,
        },
        "validation_quality": quality,
        "validation_scope": {
            "horizons": list(horizons),
            "models": list(MODEL_IDS),
            "walk_forward": True,
            "validation_step": wf.get("validation_step", 1),
            "purged_walk_forward": True,
            "purged_sample_mode": "every_horizon_step",
        },
        "model_metrics": metrics,
        "b2_vs_b1": b2_vs_b1,
        "leakage_checks": summarize_leakage_checks(wf["leakage_checks"]),
        "validation_registry": build_validation_registry(),
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "next_stage": "V1.3 20D path distribution after validation acceptance",
    }
    if contains_forbidden_validation_key(payload):
        payload["validation_quality"]["status"] = "FAIL"
        payload["validation_quality"]["failed_count"] += 1
        payload["validation_quality"]["blocking_error_count"] += 1
        payload["validation_quality"]["checks"].append({"name": "forbidden_validation_fields", "status": "FAIL", "detail": "forbidden validation output field detected"})
    return clean_payload(payload)


def evaluate_validation_quality(metrics: dict[str, Any], leakage_checks: list[dict[str, Any]], rows: list[dict[str, Any]], b2_vs_b1: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    failed = 0
    warn = 0

    def add(name: str, passed: bool, detail: str, warning: bool = False) -> None:
        nonlocal failed, warn
        if passed:
            status = "PASS"
        elif warning:
            status = "WARN"
            warn += 1
        else:
            status = "FAIL"
            failed += 1
        checks.append({"name": name, "status": status, "detail": detail})

    add("validation_samples_present", bool(rows), f"rows={len(rows)}")
    add("no_future_training_data", all(check.get("status") == "PASS" for check in leakage_checks), "training max date must be <= as_of_date")
    standard = metrics.get("standard_walk_forward_metrics", {})
    for model_id in MODEL_IDS:
        add(f"{model_id}.present", model_id in standard, f"{model_id} validation metrics present")
        for horizon in ("5D", "10D", "20D"):
            row = standard.get(model_id, {}).get(horizon, {})
            add(f"{model_id}.{horizon}.present", bool(row), f"{model_id} {horizon} present")
            if row:
                add(f"{model_id}.{horizon}.sample_size", (row.get("sample_size") or 0) > 0, f"sample_size={row.get('sample_size')}")
                add(f"{model_id}.{horizon}.interval_coverage", _coverage_reasonable(row.get("p10_p90_interval_coverage")), f"coverage={row.get('p10_p90_interval_coverage')}", warning=True)
                add(f"{model_id}.{horizon}.quantile_order", _quantile_metrics_present(row), "p10/p50/p90 metrics present")
                if model_id == "B2_state_grouped_distribution":
                    fallback = row.get("fallback_rate")
                    add(f"{model_id}.{horizon}.fallback_rate", fallback is not None and fallback <= 0.5, f"fallback_rate={fallback}", warning=True)
    add("b2_vs_b1_comparison_present", bool(b2_vs_b1), "B2 vs B1 comparison generated")
    status = "FAIL" if failed else "WARN" if warn else "PASS"
    return {
        "status": status,
        "failed_count": failed,
        "warn_count": warn,
        "blocking_error_count": failed,
        "checks": checks,
    }


def summarize_leakage_checks(checks: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [check for check in checks if check.get("status") != "PASS"]
    return {
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failed_count": len(failed),
        "max_training_date_rule": "training data must be <= as_of_date",
        "actual_return_rule": "actual_return uses T+horizon close only",
        "state_rule": "state features are built from T and prior data",
        "overlap_note": "20D validation includes overlapping samples; purged metrics use every_horizon_step.",
    }


def _metrics_by_model_horizon(rows: list[dict[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for model_id in MODEL_IDS:
        output[model_id] = {}
        for horizon in ("5D", "10D", "20D"):
            group = [row for row in rows if row.get("model_id") == model_id and row.get("horizon") == horizon]
            output[model_id][horizon] = summarize_prediction_rows(group)
    return output


def _coverage_reasonable(value: Any) -> bool:
    if value is None:
        return False
    return 0.70 <= float(value) <= 0.90


def _quantile_metrics_present(row: dict[str, Any]) -> bool:
    return all(row.get(key) is not None for key in ("p10_coverage", "p90_coverage", "p10_p90_interval_coverage"))


def write_validation_json(payload: dict[str, Any], path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return target


def write_validation_registry(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(build_validation_registry(), ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return target
