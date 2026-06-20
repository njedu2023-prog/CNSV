from __future__ import annotations

from typing import Any

import pandas as pd


def _realized_vol(close: pd.Series, window: int) -> float | None:
    returns = pd.to_numeric(close, errors="coerce").pct_change().dropna()
    if returns.shape[0] < window:
        return None
    return float(returns.tail(window).std() * (252**0.5))


def _atr(df: pd.DataFrame, window: int = 14) -> float | None:
    required = {"high", "low", "close"}
    if not required.issubset(df.columns) or len(df) < window + 1:
        return None
    high = pd.to_numeric(df["high"], errors="coerce")
    low = pd.to_numeric(df["low"], errors="coerce")
    close = pd.to_numeric(df["close"], errors="coerce")
    previous_close = close.shift(1)
    true_range = pd.concat([(high - low), (high - previous_close).abs(), (low - previous_close).abs()], axis=1).max(axis=1)
    clean = true_range.dropna()
    return float(clean.tail(window).mean()) if clean.shape[0] >= window else None


def build_volatility_features(daily: pd.DataFrame, minute_structure: dict[str, Any] | None = None) -> dict[str, Any]:
    if daily.empty or "close" not in daily.columns:
        return {}
    df = daily.sort_values("trade_date") if "trade_date" in daily.columns else daily.copy()
    close = pd.to_numeric(df["close"], errors="coerce")
    high = pd.to_numeric(df["high"] if "high" in df.columns else df["close"], errors="coerce")
    low = pd.to_numeric(df["low"] if "low" in df.columns else df["close"], errors="coerce")
    intraday_range = (high - low) / close.replace(0, pd.NA)
    rv20 = _realized_vol(close, 20)
    yearly_rv20 = close.pct_change().rolling(20).std() * (252**0.5)
    clean_year = yearly_rv20.dropna().tail(252)
    if rv20 is None or clean_year.shape[0] < 30:
        state = "unknown"
    else:
        high_q = clean_year.quantile(0.7)
        low_q = clean_year.quantile(0.3)
        state = "high_vol" if rv20 >= high_q else "low_vol" if rv20 <= low_q else "normal_vol"
    return {
        "realized_vol_5d": _realized_vol(close, 5),
        "realized_vol_10d": _realized_vol(close, 10),
        "realized_vol_20d": rv20,
        "atr_14d": _atr(df, 14),
        "intraday_range_ma5": float(intraday_range.tail(5).mean()) if intraday_range.dropna().shape[0] >= 5 else None,
        "intraday_range_ma20": float(intraday_range.tail(20).mean()) if intraday_range.dropna().shape[0] >= 20 else None,
        "volatility_state": state,
    }
