from __future__ import annotations

from typing import Any

import pandas as pd

from cnsv.models.baseline_schema import HORIZONS, price_from_return, quantile, terminal_returns

MODEL_ID = "B1_historical_distribution"


def run_b1_historical_distribution(daily: pd.DataFrame, current_close: float | None, horizons: tuple[int, ...] = HORIZONS) -> dict[str, Any]:
    results: dict[str, Any] = {"model_id": MODEL_ID, "horizons": {}}
    for horizon in horizons:
        returns = terminal_returns(daily, horizon)
        sample_size = int(returns.shape[0])
        mean_return = float(returns.mean()) if sample_size else None
        median_return = float(returns.median()) if sample_size else None
        std_return = float(returns.std()) if sample_size > 1 else None
        horizon_result = {
            "model_id": MODEL_ID,
            "horizon": horizon,
            "sample_size": sample_size,
            "mean_return": mean_return,
            "median_return": median_return,
            "std_return": std_return,
            "p05_return": quantile(returns, 0.05),
            "p10_return": quantile(returns, 0.10),
            "p25_return": quantile(returns, 0.25),
            "p50_return": quantile(returns, 0.50),
            "p75_return": quantile(returns, 0.75),
            "p90_return": quantile(returns, 0.90),
            "p95_return": quantile(returns, 0.95),
            "positive_prob": float((returns > 0).mean()) if sample_size else None,
            "negative_prob": float((returns < 0).mean()) if sample_size else None,
        }
        horizon_result["expected_price"] = price_from_return(current_close, mean_return)
        horizon_result["p10_price"] = price_from_return(current_close, horizon_result["p10_return"])
        horizon_result["p50_price"] = price_from_return(current_close, horizon_result["p50_return"])
        horizon_result["p90_price"] = price_from_return(current_close, horizon_result["p90_return"])
        results["horizons"][f"{horizon}D"] = horizon_result
    return results

