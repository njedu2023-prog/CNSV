from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cnsv.data.data_manifest import manifest_summary
from cnsv.utils.io import ensure_parent


def _clean(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _clean(inner) for key, inner in value.items()}
    if isinstance(value, list):
        return [_clean(item) for item in value]
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def build_feature_report_payload(
    gate: dict[str, Any],
    manifest: dict[str, Any],
    features: dict[str, Any],
    feature_quality: dict[str, Any],
    feature_registry: list[dict[str, Any]],
) -> dict[str, Any]:
    latest_trade_date = manifest.get("latest_trade_date", "")
    return _clean(
        {
            "meta": {
                "system": "CNSV",
                "version": "1.1.0",
                "report_type": "feature_report",
                "ts_code": "600150.SH",
                "name": "中国船舶",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "latest_trade_date": latest_trade_date,
            },
            "cnsvdata_gate": gate,
            "data_manifest": manifest_summary(manifest),
            "feature_quality": feature_quality,
            "features": {
                "price_volume": features.get("price_volume", {}),
                "minute_structure": features.get("minute_structure", {}),
                "moneyflow": features.get("moneyflow", {}),
                "trend": features.get("trend", {}),
                "volatility": features.get("volatility", {}),
            },
            "feature_registry": feature_registry,
            "allowed_actions": {
                "can_generate_formal_signal": False,
            },
            "forbidden_actions": ["formal_signal_generation", "auto_order", "broker_api"],
            "next_stage": "V1.2 baseline models",
        }
    )


def write_feature_report_json(payload: dict[str, Any], path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return target
