from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cnsv.data.data_manifest import manifest_summary
from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS, clean_payload, current_state
from cnsv.utils.io import ensure_parent


def build_baseline_report_payload(
    gate: dict[str, Any],
    manifest: dict[str, Any],
    features: dict[str, Any],
    feature_quality: dict[str, Any],
    baseline_run: dict[str, Any],
    baseline_registry: list[dict[str, Any]],
) -> dict[str, Any]:
    moneyflow = features.get("moneyflow", {}) or {}
    state = current_state(features)
    return clean_payload(
        {
            "meta": {
                "system": "CNSV",
                "version": "1.2.1",
                "stage": "V1.2.1_state_grouped_baseline_fix",
                "report_type": "baseline_model_report",
                "ts_code": "600150.SH",
                "name": "中国船舶",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "latest_trade_date": manifest.get("latest_trade_date", baseline_run.get("latest_trade_date", "")),
                "is_trade_signal": False,
            },
            "cnsvdata_gate": gate,
            "data_manifest": manifest_summary(manifest),
            "feature_quality": feature_quality,
            "baseline_quality": baseline_run.get("baseline_quality", {}),
            "current_state": {
                "latest_close": baseline_run.get("current_close"),
                "trend_state": state.get("trend_state"),
                "volatility_state": state.get("volatility_state"),
                "flow_strength_basic": state.get("flow_strength_basic"),
                "can_use_moneyflow_as_strong_factor": moneyflow.get("can_use_as_strong_factor"),
            },
            "baseline_models": baseline_run.get("models", {}),
            "baseline_registry": baseline_registry,
            "forbidden_actions": FORBIDDEN_ACTIONS,
            "next_stage": "V1.2.2 baseline validation / walk-forward validation",
        }
    )


def write_baseline_report_json(payload: dict[str, Any], path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return target
