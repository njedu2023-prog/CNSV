from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from cnsv.backtest import BACKTEST_STAGE, BACKTEST_VERSION
from cnsv.backtest.backtest_evaluator import evaluate_observation_backtest
from cnsv.backtest.backtest_metrics import metrics_by_model_horizon
from cnsv.backtest.bucket_analysis import build_bucket_metrics, build_condition_quality
from cnsv.backtest.leakage_checks import summarize_observation_leakage
from cnsv.backtest.model_comparison import compare_path_models
from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS, HORIZONS, clean_payload
from cnsv.path import PATH_MODEL_IDS
from cnsv.path.path_validation import purged_rows, run_path_walk_forward_validation


def run_observation_backtest(
    data_bundle: dict[str, Any],
    gate: dict[str, Any],
    horizons: tuple[int, ...] = HORIZONS,
    min_history: int = 260,
    validation_step: int = 50,
) -> dict[str, Any]:
    wf = run_path_walk_forward_validation(data_bundle, gate, horizons=horizons, min_history=min_history, validation_step=validation_step)
    rows = wf.get("rows", [])
    purged = purged_rows(rows)
    standard_metrics = metrics_by_model_horizon(rows)
    purged_metrics = metrics_by_model_horizon(purged)
    manifest = data_bundle.get("data_manifest") or {}
    payload: dict[str, Any] = {
        "meta": {
            "system": "CNSV",
            "version": BACKTEST_VERSION,
            "stage": BACKTEST_STAGE,
            "report_type": "observation_backtest_report",
            "ts_code": "600150.SH",
            "name": "中国船舶",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "latest_trade_date": manifest.get("latest_trade_date", ""),
            "is_trade_signal": False,
        },
        "cnsvdata_gate": _stage_gate(gate),
        "backtest_scope": {
            "horizons": list(horizons),
            "models": list(PATH_MODEL_IDS),
            "standard_walk_forward": True,
            "purged_walk_forward": True,
            "standard_sample_size": len(rows),
            "purged_sample_size": len(purged),
            "validation_step": validation_step,
            "backtest_type": "observation_only",
        },
        "model_backtest_metrics": {
            "standard_walk_forward": standard_metrics,
            "purged_walk_forward": purged_metrics,
        },
        "observation_bucket_metrics": build_bucket_metrics(rows),
        "model_comparison": {
            "standard_walk_forward": compare_path_models(standard_metrics),
            "purged_walk_forward": compare_path_models(purged_metrics),
        },
        "observation_condition_quality": build_condition_quality(rows),
        "observation_backtest_leakage_checks": summarize_observation_leakage(wf.get("leakage_checks", [])),
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "next_stage": "V1.5 human decision support",
    }
    payload["observation_backtest_quality"] = evaluate_observation_backtest(payload)
    return clean_payload(payload)


def _stage_gate(gate: dict[str, Any]) -> dict[str, Any]:
    stage_gate = dict(gate)
    stage_gate["can_run_backtest"] = True
    stage_gate["backtest_permission_stage"] = "V1.4"
    stage_gate["stage_permission_note"] = "V1.4 permits observation-only backtest; formal trade signal generation remains forbidden."
    stage_gate["can_generate_formal_signal"] = False
    return stage_gate
