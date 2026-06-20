from __future__ import annotations

import math
from typing import Any

import pandas as pd

from cnsv.models.baseline_schema import HORIZONS, daily_log_return_std, price_from_return, terminal_returns

MODEL_ID = "B0_random_walk"
Z10 = -1.2815515655446004
Z90 = 1.2815515655446004


def run_b0_random_walk(daily: pd.DataFrame, current_close: float | None, horizons: tuple[int, ...] = HORIZONS) -> dict[str, Any]:
    daily_std = daily_log_return_std(daily, window=60) or daily_log_return_std(daily)
    results: dict[str, Any] = {"model_id": MODEL_ID, "horizons": {}}
    for horizon in horizons:
        volatility_estimate = daily_std * math.sqrt(horizon) if daily_std is not None else None
        p10_return = Z10 * volatility_estimate if volatility_estimate is not None else None
        p50_return = 0.0 if current_close is not None else None
        p90_return = Z90 * volatility_estimate if volatility_estimate is not None else None
        horizon_result = {
            "model_id": MODEL_ID,
            "horizon": horizon,
            "current_close": current_close,
            "expected_return": 0.0 if current_close is not None else None,
            "expected_price": current_close,
            "volatility_estimate": volatility_estimate,
            "p10_return": p10_return,
            "p50_return": p50_return,
            "p90_return": p90_return,
            "p10_price": price_from_return(current_close, p10_return),
            "p50_price": price_from_return(current_close, p50_return),
            "p90_price": price_from_return(current_close, p90_return),
            "sample_size": int(terminal_returns(daily, horizon).shape[0]),
        }
        results["horizons"][f"{horizon}D"] = horizon_result
    return results

