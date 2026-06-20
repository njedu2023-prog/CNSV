from __future__ import annotations

from typing import Any

import pandas as pd


def _slope(series: pd.Series, window: int) -> float | None:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.shape[0] < window + 1:
        return None
    previous = clean.iloc[-window - 1 : -1].mean()
    current = clean.iloc[-window:].mean()
    return float(current / previous - 1) if previous else None


def _above(close: float | None, ma: float | None) -> bool | None:
    if close is None or ma is None:
        return None
    return bool(close > ma)


def build_trend_features(price_volume: dict[str, Any], daily: pd.DataFrame | None = None) -> dict[str, Any]:
    close = price_volume.get("latest_close")
    ma5 = price_volume.get("ma5")
    ma10 = price_volume.get("ma10")
    ma20 = price_volume.get("ma20")
    ma60 = price_volume.get("ma60")
    close_series = pd.to_numeric(daily["close"], errors="coerce") if daily is not None and "close" in daily.columns else pd.Series(dtype="float64")
    if close is not None and ma5 is not None and ma10 is not None and ma20 is not None and close > ma5 > ma10 > ma20:
        trend_state = "strong_uptrend"
    elif close is not None and ma20 is not None and ma5 is not None and close > ma20 and ma5 > ma20:
        trend_state = "uptrend"
    elif close is not None and ma5 is not None and ma10 is not None and ma20 is not None and close < ma5 < ma10 < ma20:
        trend_state = "strong_downtrend"
    elif close is not None and ma20 is not None and close < ma20:
        trend_state = "downtrend"
    else:
        trend_state = "neutral"
    return {
        "trend_ma5_ma20": None if ma5 is None or ma20 is None else float(ma5 - ma20),
        "trend_ma10_ma60": None if ma10 is None or ma60 is None else float(ma10 - ma60),
        "close_above_ma5": _above(close, ma5),
        "close_above_ma10": _above(close, ma10),
        "close_above_ma20": _above(close, ma20),
        "close_above_ma60": _above(close, ma60),
        "ma5_slope": _slope(close_series, 5),
        "ma10_slope": _slope(close_series, 10),
        "ma20_slope": _slope(close_series, 20),
        "trend_state": trend_state,
    }
