from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from cnsv.features.feature_bundle import build_feature_bundle
from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS, HORIZONS, clean_payload, sorted_daily
from cnsv.path import PATH_MODEL_IDS
from cnsv.path.path_distribution import run_path_distribution_from_features
from cnsv.path.path_evaluator import contains_forbidden_path_key
from cnsv.path.path_metrics import actual_path_outcome, summarize_validation_rows

STAGE = "V1.3_path_validation"


def run_path_validation(
    data_bundle: dict[str, Any],
    gate: dict[str, Any],
    horizons: tuple[int, ...] = HORIZONS,
    min_history: int = 260,
    validation_step: int = 20,
) -> dict[str, Any]:
    wf = run_path_walk_forward_validation(data_bundle, gate, horizons, min_history, validation_step)
    standard = _metrics_by_model_horizon(wf["rows"])
    purged = _metrics_by_model_horizon(purged_rows(wf["rows"]))
    p2_vs_p1 = compare_p2_vs_p1({"standard_walk_forward_metrics": standard, "purged_walk_forward_metrics": purged})
    quality = evaluate_path_validation_quality(standard, purged, wf["leakage_checks"], wf["rows"])
    manifest = data_bundle.get("data_manifest") or {}
    payload = {
        "meta": {
            "system": "CNSV",
            "version": "1.3.0",
            "stage": STAGE,
            "report_type": "path_validation_report",
            "ts_code": "600150.SH",
            "name": "中国船舶",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "latest_trade_date": manifest.get("latest_trade_date", ""),
            "is_trade_signal": False,
        },
        "path_validation_quality": quality,
        "validation_scope": {
            "horizons": list(horizons),
            "models": list(PATH_MODEL_IDS),
            "walk_forward": True,
            "validation_step": validation_step,
            "purged_walk_forward": True,
            "purged_sample_mode": "every_horizon_step",
        },
        "standard_walk_forward_metrics": standard,
        "purged_walk_forward_metrics": purged,
        "p2_vs_p1": p2_vs_p1,
        "path_leakage_checks": summarize_path_leakage_checks(wf["leakage_checks"]),
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "next_stage": "V1.4 observation backtest after path validation acceptance",
    }
    if contains_forbidden_path_key(payload):
        payload["path_validation_quality"]["status"] = "FAIL"
        payload["path_validation_quality"]["failed_count"] += 1
        payload["path_validation_quality"]["blocking_error_count"] += 1
        payload["path_validation_quality"]["checks"].append({"name": "forbidden_path_fields", "status": "FAIL", "detail": "forbidden trade action field detected"})
    return clean_payload(payload)


def run_path_walk_forward_validation(
    data_bundle: dict[str, Any],
    gate: dict[str, Any],
    horizons: tuple[int, ...] = HORIZONS,
    min_history: int = 260,
    validation_step: int = 20,
) -> dict[str, Any]:
    daily = sorted_daily(data_bundle.get("daily") if isinstance(data_bundle.get("daily"), pd.DataFrame) else pd.DataFrame())
    if daily.empty or not {"close", "high", "low"}.issubset(daily.columns):
        return {"rows": [], "leakage_checks": [], "validation_step": validation_step, "skipped_reason": "missing_daily_ohlc"}
    rows: list[dict[str, Any]] = []
    leakage_checks: list[dict[str, Any]] = []
    close = pd.to_numeric(daily["close"], errors="coerce").to_list()
    high = pd.to_numeric(daily["high"], errors="coerce").to_list()
    low = pd.to_numeric(daily["low"], errors="coerce").to_list()
    dates = daily["trade_date"].astype(str).tolist() if "trade_date" in daily.columns else [str(i) for i in range(len(daily))]
    max_horizon = max(horizons)
    last_start = len(daily) - max_horizon - 1
    for idx in range(min_history, max(min_history, last_start + 1), max(1, validation_step)):
        as_of_date = dates[idx]
        train_bundle = _slice_bundle_as_of(data_bundle, as_of_date)
        features = build_feature_bundle(train_bundle, gate)
        prediction = run_path_distribution_from_features(train_bundle, gate, features, horizons)
        leakage_checks.append(_path_leakage_check(as_of_date, train_bundle, idx, dates, horizons))
        for horizon in horizons:
            future_end = idx + horizon
            if future_end >= len(daily):
                continue
            base_close = close[idx]
            c_path = close[idx + 1 : future_end + 1]
            h_path = high[idx + 1 : future_end + 1]
            l_path = low[idx + 1 : future_end + 1]
            if not _valid_truth(base_close, c_path, h_path, l_path, horizon):
                continue
            truth = actual_path_outcome(c_path, h_path, l_path, float(base_close))
            for model_id in PATH_MODEL_IDS:
                row = (prediction.get("path_models", {}).get(model_id, {}).get("horizons", {}) or {}).get(f"{horizon}D", {})
                rows.append(
                    {
                        "as_of_date": as_of_date,
                        "truth_start_date": dates[idx + 1],
                        "truth_end_date": dates[future_end],
                        "horizon": f"{horizon}D",
                        "horizon_days": horizon,
                        "model_id": model_id,
                        "max_training_date": _max_training_date(train_bundle),
                        "state_date": as_of_date,
                        "fallback_used": bool(row.get("fallback_used", False)),
                        **{key: row.get(key) for key in _prediction_keys()},
                        **truth,
                    }
                )
    return {"rows": rows, "leakage_checks": leakage_checks, "validation_step": validation_step, "skipped_reason": ""}


def purged_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for model_id in PATH_MODEL_IDS:
        for horizon in sorted({row["horizon_days"] for row in rows}):
            group = sorted([row for row in rows if row["model_id"] == model_id and row["horizon_days"] == horizon], key=lambda row: row["as_of_date"])
            selected.extend(group[::horizon])
    return selected


def evaluate_path_validation_quality(standard: dict[str, Any], purged: dict[str, Any], leakage_checks: list[dict[str, Any]], rows: list[dict[str, Any]]) -> dict[str, Any]:
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
    add("path_leakage_checks", all(check.get("status") == "PASS" for check in leakage_checks), "training <= as_of, truth T+1..T+h")
    for model_id in PATH_MODEL_IDS:
        add(f"{model_id}.standard_present", model_id in standard, f"{model_id} standard metrics present")
        add(f"{model_id}.purged_present", model_id in purged, f"{model_id} purged metrics present")
        for horizon in ("5D", "10D", "20D"):
            row = standard.get(model_id, {}).get(horizon, {})
            add(f"{model_id}.{horizon}.sample_size", (row.get("sample_size") or 0) > 0, f"sample_size={row.get('sample_size')}")
            add(f"{model_id}.{horizon}.terminal_coverage", _coverage_reasonable(row.get("terminal_p10_p90_coverage")), f"coverage={row.get('terminal_p10_p90_coverage')}", warning=True)
            add(f"{model_id}.{horizon}.path_metrics", _core_metrics_present(row), "path validation metrics present")
            if model_id == "P2_state_conditional_path":
                add(f"{model_id}.{horizon}.fallback_rate", (row.get("fallback_rate") is not None), f"fallback_rate={row.get('fallback_rate')}", warning=True)
    status = "FAIL" if failed else "WARN" if warn else "PASS"
    return {"status": status, "failed_count": failed, "warn_count": warn, "blocking_error_count": failed, "checks": checks}


def summarize_path_leakage_checks(checks: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [check for check in checks if check.get("status") != "PASS"]
    return {
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failed_count": len(failed),
        "checks": checks[:20],
        "purged_sample_mode": "every_horizon_step",
        "rules": [
            "每个 as_of_date 的训练数据最大日期 <= as_of_date",
            "T 日状态只由 T 及以前数据构造",
            "真实验证结果只来自 T+1 到 T+h",
            "purged 模式按 horizon 间隔抽样降低重叠污染",
        ],
    }


def compare_p2_vs_p1(metrics: dict[str, Any]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for mode, model_metrics in metrics.items():
        output[mode] = {}
        p1 = model_metrics.get("P1_volatility_adjusted_path", {})
        p2 = model_metrics.get("P2_state_conditional_path", {})
        for horizon in ("5D", "10D", "20D"):
            a, b = p1.get(horizon, {}), p2.get(horizon, {})
            p1_rmse, p2_rmse = a.get("path_rmse_terminal"), b.get("path_rmse_terminal")
            output[mode][horizon] = {
                "P2_vs_P1_terminal_coverage_delta": _delta(b.get("terminal_p10_p90_coverage"), a.get("terminal_p10_p90_coverage")),
                "P2_vs_P1_terminal_rmse_delta": _delta(p2_rmse, p1_rmse),
                "P2_vs_P1_fallback_rate": b.get("fallback_rate"),
                "P2_vs_P1_conclusion": _compare_conclusion(p1_rmse, p2_rmse),
            }
    return output


def _metrics_by_model_horizon(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {model_id: {h: summarize_validation_rows([row for row in rows if row.get("model_id") == model_id and row.get("horizon") == h]) for h in ("5D", "10D", "20D")} for model_id in PATH_MODEL_IDS}


def _slice_bundle_as_of(data_bundle: dict[str, Any], as_of_date: str) -> dict[str, Any]:
    sliced: dict[str, Any] = {}
    for key, value in data_bundle.items():
        if isinstance(value, pd.DataFrame):
            sliced[key] = _slice_frame_as_of(value, as_of_date)
        elif key == "data_manifest" and isinstance(value, dict):
            sliced[key] = {**value, "latest_trade_date": as_of_date}
        else:
            sliced[key] = value
    return sliced


def _slice_frame_as_of(frame: pd.DataFrame, as_of_date: str) -> pd.DataFrame:
    if frame.empty or "trade_date" not in frame.columns:
        return frame.copy()
    return frame.loc[frame["trade_date"].astype(str) <= str(as_of_date)].copy().sort_values("trade_date").reset_index(drop=True)


def _path_leakage_check(as_of_date: str, train_bundle: dict[str, Any], idx: int, dates: list[str], horizons: tuple[int, ...]) -> dict[str, Any]:
    max_training = _max_training_date(train_bundle)
    truth_start = dates[idx + 1] if idx + 1 < len(dates) else ""
    truth_end = dates[idx + max(horizons)] if idx + max(horizons) < len(dates) else ""
    passed = str(max_training) <= str(as_of_date) and str(truth_start) > str(as_of_date) and str(truth_end) > str(as_of_date)
    return {"name": "path_training_window", "status": "PASS" if passed else "FAIL", "as_of_date": as_of_date, "max_training_date": max_training, "state_date": as_of_date, "truth_start_date": truth_start, "truth_end_date": truth_end}


def _max_training_date(data_bundle: dict[str, Any]) -> str:
    dates = []
    for value in data_bundle.values():
        if isinstance(value, pd.DataFrame) and not value.empty and "trade_date" in value.columns:
            dates.append(str(value["trade_date"].astype(str).max()))
    return max(dates) if dates else ""


def _valid_truth(base_close: Any, close: list[Any], high: list[Any], low: list[Any], horizon: int) -> bool:
    try:
        values = [float(base_close), *map(float, close), *map(float, high), *map(float, low)]
    except (TypeError, ValueError):
        return False
    return len(close) == len(high) == len(low) == horizon and all(v > 0 for v in values)


def _prediction_keys() -> list[str]:
    return [
        "terminal_return_p10",
        "terminal_return_p50",
        "terminal_return_p90",
        "max_up_return_p10",
        "max_up_return_p50",
        "max_up_return_p90",
        "max_down_return_p10",
        "max_down_return_p50",
        "max_down_return_p90",
        "max_drawdown_p10",
        "max_drawdown_p50",
        "max_drawdown_p90",
        "touch_up_3pct_prob",
        "touch_up_5pct_prob",
        "touch_down_3pct_prob",
        "touch_down_5pct_prob",
        "positive_terminal_prob",
    ]


def _coverage_reasonable(value: Any) -> bool:
    return value is not None and 0.60 <= float(value) <= 0.95


def _core_metrics_present(row: dict[str, Any]) -> bool:
    return all(row.get(key) is not None for key in ("terminal_p10_p90_coverage", "touch_up_3pct_brier", "touch_down_3pct_brier", "path_rmse_terminal"))


def _delta(left: Any, right: Any) -> float | None:
    return None if left is None or right is None else float(left) - float(right)


def _compare_conclusion(p1_rmse: Any, p2_rmse: Any) -> str:
    if p1_rmse is None or p2_rmse is None:
        return "insufficient data"
    diff = float(p2_rmse) - float(p1_rmse)
    if diff < -0.001:
        return "P2 improves P1"
    if diff > 0.001:
        return "P2 underperforms P1"
    return "neutral"
