from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

from cnsv.models.baseline_schema import sorted_daily


def build_path_samples(
    daily: pd.DataFrame,
    horizon: int,
    latest_close: float,
    state_daily: pd.DataFrame | None = None,
    state_key: dict[str, Any] | None = None,
    volatility_scale: float = 1.0,
    include_price_paths: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    df = sorted_daily(daily if isinstance(daily, pd.DataFrame) else pd.DataFrame())
    if df.empty or latest_close <= 0 or not {"close", "high", "low"}.issubset(df.columns):
        return [], {"dropped_count": 0, "state_sample_size": 0, "skipped_reason": "missing_daily_ohlc"}
    states = _aligned_states(df, state_daily)
    close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
    high = pd.to_numeric(df["high"], errors="coerce").to_numpy(dtype=float)
    low = pd.to_numeric(df["low"], errors="coerce").to_numpy(dtype=float)
    dates = df["trade_date"].astype(str).tolist() if "trade_date" in df.columns else [str(i) for i in range(len(df))]
    samples: list[dict[str, Any]] = []
    dropped = 0
    state_seen = 0
    last_base = len(df) - horizon - 1
    for idx in range(0, max(0, last_base + 1)):
        if state_key and not _state_matches(states, idx, state_key):
            continue
        if state_key:
            state_seen += 1
        base = close[idx]
        c = close[idx + 1 : idx + horizon + 1]
        h = high[idx + 1 : idx + horizon + 1]
        l = low[idx + 1 : idx + horizon + 1]
        if not _valid_window(base, c, h, l, horizon):
            dropped += 1
            continue
        close_ret = (c / base - 1.0) * volatility_scale
        high_ret = (h / base - 1.0) * volatility_scale
        low_ret = (l / base - 1.0) * volatility_scale
        sample = {
            "base_date": dates[idx],
            "target_date": dates[idx + horizon],
            "close_return_path": close_ret.tolist(),
            "high_return_path": high_ret.tolist(),
            "low_return_path": low_ret.tolist(),
        }
        if include_price_paths:
            sample.update(
                {
                    "close_price_path": (latest_close * (1.0 + close_ret)).tolist(),
                    "high_price_path": (latest_close * (1.0 + high_ret)).tolist(),
                    "low_price_path": (latest_close * (1.0 + low_ret)).tolist(),
                }
            )
        samples.append(sample)
    return samples, {"dropped_count": dropped, "state_sample_size": state_seen if state_key else len(samples), "skipped_reason": ""}


def max_drawdown(close_return_path: list[float]) -> float | None:
    values = np.array([1.0] + [1.0 + float(x) for x in close_return_path], dtype=float)
    if values.size < 2 or np.any(~np.isfinite(values)) or np.any(values <= 0):
        return None
    running_high = np.maximum.accumulate(values)
    drawdowns = values / running_high - 1.0
    out = float(drawdowns.min())
    return out if math.isfinite(out) else None


def _valid_window(base: float, close: np.ndarray, high: np.ndarray, low: np.ndarray, horizon: int) -> bool:
    arrays = (close, high, low)
    if not math.isfinite(float(base)) or base <= 0:
        return False
    return all(arr.size == horizon and np.all(np.isfinite(arr)) and np.all(arr > 0) for arr in arrays)


def _aligned_states(daily: pd.DataFrame, state_daily: pd.DataFrame | None) -> pd.DataFrame:
    columns = ["trend_state", "volatility_state", "flow_strength_basic"]
    if not isinstance(state_daily, pd.DataFrame) or state_daily.empty:
        return pd.DataFrame(index=daily.index, columns=columns)
    if "trade_date" not in daily.columns or "trade_date" not in state_daily.columns:
        return state_daily.reindex(daily.index)[columns] if set(columns).issubset(state_daily.columns) else pd.DataFrame(index=daily.index, columns=columns)
    state = state_daily[["trade_date", *[c for c in columns if c in state_daily.columns]]].copy()
    merged = daily[["trade_date"]].astype({"trade_date": str}).merge(state.astype({"trade_date": str}), on="trade_date", how="left")
    for col in columns:
        if col not in merged.columns:
            merged[col] = None
    return merged[columns]


def _state_matches(states: pd.DataFrame, idx: int, state_key: dict[str, Any]) -> bool:
    for col, value in state_key.items():
        if value in (None, "", "unknown"):
            return False
        if idx >= len(states) or str(states.iloc[idx].get(col)) != str(value):
            return False
    return True
