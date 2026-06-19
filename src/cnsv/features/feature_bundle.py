from __future__ import annotations

from typing import Any

from cnsv.features.minute_structure_features import build_minute_structure_features
from cnsv.features.moneyflow_features import build_moneyflow_features
from cnsv.features.price_volume_features import build_price_volume_features


def build_feature_bundle(data_bundle: dict[str, Any], gate: dict[str, Any]) -> dict[str, Any]:
    daily = data_bundle.get("daily")
    one_min = data_bundle.get("one_min")
    moneyflow = data_bundle.get("moneyflow")
    latest_trade_date = ""
    manifest = data_bundle.get("data_manifest") or {}
    latest_trade_date = str(manifest.get("latest_trade_date") or "")
    features = {
        "price_volume": build_price_volume_features(daily),
        "minute_structure": build_minute_structure_features(one_min),
        "moneyflow": build_moneyflow_features(moneyflow, gate, latest_trade_date),
    }
    feature_status = "PASS" if all(features.values()) else "WARN"
    return {**features, "feature_status": feature_status}
