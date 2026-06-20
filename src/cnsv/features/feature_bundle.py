from __future__ import annotations

from typing import Any

import pandas as pd

from cnsv.features.minute_structure_features import build_minute_structure_features
from cnsv.features.moneyflow_features import build_moneyflow_features
from cnsv.features.price_volume_features import build_price_volume_features
from cnsv.features.trend_features import build_trend_features
from cnsv.features.volatility_features import build_volatility_features


def build_feature_bundle(data_bundle: dict[str, Any], gate: dict[str, Any]) -> dict[str, Any]:
    daily = data_bundle.get("daily")
    one_min = data_bundle.get("one_min")
    moneyflow = data_bundle.get("moneyflow")
    latest_trade_date = ""
    manifest = data_bundle.get("data_manifest") or {}
    latest_trade_date = str(manifest.get("latest_trade_date") or "")
    daily_df = daily if isinstance(daily, pd.DataFrame) else pd.DataFrame()
    one_min_df = one_min if isinstance(one_min, pd.DataFrame) else pd.DataFrame()
    moneyflow_df = moneyflow if isinstance(moneyflow, pd.DataFrame) else pd.DataFrame()
    price_volume = build_price_volume_features(daily_df)
    minute_structure = build_minute_structure_features(one_min_df)
    moneyflow_features = build_moneyflow_features(moneyflow_df, gate, latest_trade_date, daily_df, price_volume)
    trend = build_trend_features(price_volume, daily_df)
    volatility = build_volatility_features(daily_df, minute_structure)
    features = {
        "price_volume": price_volume,
        "minute_structure": minute_structure,
        "moneyflow": moneyflow_features,
        "trend": trend,
        "volatility": volatility,
    }
    feature_status = "PASS" if all(features.values()) else "WARN"
    return {**features, "feature_status": feature_status}
