from __future__ import annotations

import math
from typing import Any

import pandas as pd

from cnsv.models.baseline_b1_historical_distribution import run_b1_historical_distribution
from cnsv.models.baseline_schema import HORIZONS, current_state, price_from_return, quantile
from cnsv.models.baseline_state_history import STATE_COLUMNS, state_coverage

MODEL_ID = "B2_state_grouped_distribution"
MIN_STATE_SAMPLE = 30


def _state_key(features: dict[str, Any]) -> str:
    state = current_state(features)
    return "|".join(str(state.get(key) or "unknown") for key in ("trend_state", "volatility_state", "flow_strength_basic"))


def _state_terminal_returns(daily: pd.DataFrame, mask: pd.Series, horizon: int) -> pd.Series:
    close = pd.to_numeric(daily["close"], errors="coerce") if "close" in daily.columns else pd.Series(dtype="float64")
    returns = (close.shift(-horizon) / close).map(lambda value: None if pd.isna(value) or value <= 0 else value)
    log_returns = pd.Series(float("nan"), index=daily.index, dtype="float64")
    clean = pd.to_numeric(returns, errors="coerce")
    log_returns.loc[clean.notna()] = clean.loc[clean.notna()].map(math.log)
    return pd.to_numeric(log_returns.loc[mask], errors="coerce").dropna()


def run_b2_state_grouped_distribution(
    daily: pd.DataFrame,
    current_close: float | None,
    features: dict[str, Any],
    horizons: tuple[int, ...] = HORIZONS,
) -> dict[str, Any]:
    state = current_state(features)
    state_key = _state_key(features)
    b1 = run_b1_historical_distribution(daily, current_close, horizons)
    coverage = state_coverage(daily)
    results: dict[str, Any] = {
        "model_id": MODEL_ID,
        "state_key": state_key,
        "state_columns": list(STATE_COLUMNS),
        "state_coverage": coverage,
        "horizons": {},
    }
    has_state_columns = bool(coverage.get("has_state_columns"))
    for horizon in horizons:
        if has_state_columns:
            mask = (
                daily["trend_state"].astype(str).eq(str(state.get("trend_state")))
                & daily["volatility_state"].astype(str).eq(str(state.get("volatility_state")))
                & daily["flow_strength_basic"].astype(str).eq(str(state.get("flow_strength_basic")))
            )
            returns = _state_terminal_returns(daily, mask, horizon)
        else:
            returns = pd.Series(dtype="float64")
        state_sample_size = int(returns.shape[0])
        fallback_used = state_sample_size < MIN_STATE_SAMPLE
        if fallback_used:
            fallback_reason = "state_sample_size_lt_30" if has_state_columns else "missing_historical_state_columns"
            fallback = b1["horizons"][f"{horizon}D"]
            horizon_result = {
                "model_id": MODEL_ID,
                "horizon": horizon,
                "state_key": state_key,
                "state_sample_size": state_sample_size,
                "fallback_used": True,
                "fallback_reason": fallback_reason,
                "fallback_method": "B1_historical_distribution",
                "fallback_gating": False,
                "next_coverage_action": "extend historical state coverage for trend_state, volatility_state, and flow_strength_basic",
                "mean_return": fallback.get("mean_return"),
                "median_return": fallback.get("median_return"),
                "p10_return": fallback.get("p10_return"),
                "p50_return": fallback.get("p50_return"),
                "p90_return": fallback.get("p90_return"),
                "positive_prob": fallback.get("positive_prob"),
                "expected_price": fallback.get("expected_price"),
                "p10_price": fallback.get("p10_price"),
                "p50_price": fallback.get("p50_price"),
                "p90_price": fallback.get("p90_price"),
            }
        else:
            mean_return = float(returns.mean())
            median_return = float(returns.median())
            p10 = quantile(returns, 0.10)
            p50 = quantile(returns, 0.50)
            p90 = quantile(returns, 0.90)
            horizon_result = {
                "model_id": MODEL_ID,
                "horizon": horizon,
                "state_key": state_key,
                "state_sample_size": state_sample_size,
                "fallback_used": False,
                "fallback_reason": "",
                "fallback_method": "",
                "fallback_gating": False,
                "mean_return": mean_return,
                "median_return": median_return,
                "p10_return": p10,
                "p50_return": p50,
                "p90_return": p90,
                "positive_prob": float((returns > 0).mean()),
                "expected_price": price_from_return(current_close, mean_return),
                "p10_price": price_from_return(current_close, p10),
                "p50_price": price_from_return(current_close, p50),
                "p90_price": price_from_return(current_close, p90),
            }
        results["horizons"][f"{horizon}D"] = horizon_result
    return results
