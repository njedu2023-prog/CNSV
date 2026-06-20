from __future__ import annotations

from typing import Any

import pandas as pd

from cnsv.models.baseline_b1_historical_distribution import run_b1_historical_distribution
from cnsv.models.baseline_schema import HORIZONS, clean_number, daily_log_return_std, price_from_return

MODEL_ID = "B3_volatility_adjusted"
Z10 = -1.2815515655446004
Z90 = 1.2815515655446004


def _volatility_scale(daily: pd.DataFrame, features: dict[str, Any]) -> tuple[float, list[str]]:
    warnings: list[str] = []
    realized_vol_20d = clean_number((features.get("volatility", {}) or {}).get("realized_vol_20d"))
    long_term_daily = daily_log_return_std(daily)
    long_term_vol = long_term_daily * (252**0.5) if long_term_daily is not None else None
    if realized_vol_20d is None or long_term_vol in (None, 0):
        return 1.0, ["volatility_scale_defaulted"]
    raw = realized_vol_20d / long_term_vol
    clipped = max(0.5, min(2.0, raw))
    if clipped != raw:
        warnings.append("volatility_scale_clipped")
    return clipped, warnings


def run_b3_volatility_adjusted(
    daily: pd.DataFrame,
    current_close: float | None,
    features: dict[str, Any],
    horizons: tuple[int, ...] = HORIZONS,
) -> dict[str, Any]:
    scale, warnings = _volatility_scale(daily, features)
    b1 = run_b1_historical_distribution(daily, current_close, horizons)
    results: dict[str, Any] = {"model_id": MODEL_ID, "volatility_scale": scale, "warnings": warnings, "horizons": {}}
    for horizon in horizons:
        base = b1["horizons"][f"{horizon}D"]
        mean_return = base.get("mean_return")
        base_std = base.get("std_return")
        adjusted_std = base_std * scale if base_std is not None else None
        p10 = mean_return + Z10 * adjusted_std if mean_return is not None and adjusted_std is not None else None
        p50 = mean_return
        p90 = mean_return + Z90 * adjusted_std if mean_return is not None and adjusted_std is not None else None
        results["horizons"][f"{horizon}D"] = {
            "model_id": MODEL_ID,
            "horizon": horizon,
            "mean_return": mean_return,
            "adjusted_std": adjusted_std,
            "volatility_scale": scale,
            "p10_return": p10,
            "p50_return": p50,
            "p90_return": p90,
            "p10_price": price_from_return(current_close, p10),
            "p50_price": price_from_return(current_close, p50),
            "p90_price": price_from_return(current_close, p90),
            "sample_size": base.get("sample_size"),
        }
    return results

