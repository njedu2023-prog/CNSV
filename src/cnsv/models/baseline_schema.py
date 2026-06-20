from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

HORIZONS = (5, 10, 20)
FORBIDDEN_FIELD_TOKENS = ("signal", "buy", "sell", "position", "stop_loss", "take_profit")
FORBIDDEN_ACTIONS = ["formal_signal_generation", "auto_order", "broker_api"]


def clean_number(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def clean_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: clean_payload(inner) for key, inner in value.items()}
    if isinstance(value, list):
        return [clean_payload(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, np.generic):
        return clean_payload(value.item())
    return value


def sorted_daily(daily: pd.DataFrame) -> pd.DataFrame:
    if daily.empty:
        return daily.copy()
    return daily.sort_values("trade_date").reset_index(drop=True) if "trade_date" in daily.columns else daily.reset_index(drop=True)


def close_series(daily: pd.DataFrame) -> pd.Series:
    if "close" not in daily.columns:
        return pd.Series(dtype="float64")
    return pd.to_numeric(sorted_daily(daily)["close"], errors="coerce")


def terminal_returns(daily: pd.DataFrame, horizon: int) -> pd.Series:
    close = close_series(daily)
    if close.dropna().shape[0] <= horizon:
        return pd.Series(dtype="float64")
    returns = np.log(close.shift(-horizon) / close)
    return pd.Series(returns).replace([np.inf, -np.inf], np.nan).dropna()


def latest_close(daily: pd.DataFrame, features: dict[str, Any] | None = None) -> float | None:
    feature_close = clean_number((features or {}).get("price_volume", {}).get("latest_close"))
    if feature_close is not None:
        return feature_close
    close = close_series(daily).dropna()
    return float(close.iloc[-1]) if not close.empty else None


def price_from_return(current_close: float | None, terminal_return: float | None) -> float | None:
    current = clean_number(current_close)
    ret = clean_number(terminal_return)
    if current is None or ret is None or current <= 0:
        return None
    price = current * math.exp(ret)
    return price if math.isfinite(price) and price > 0 else None


def quantile(values: pd.Series, q: float) -> float | None:
    clean = pd.to_numeric(values, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if clean.empty:
        return None
    return float(clean.quantile(q))


def daily_log_return_std(daily: pd.DataFrame, window: int | None = None) -> float | None:
    close = close_series(daily)
    returns = np.log(close / close.shift(1)).replace([np.inf, -np.inf], np.nan).dropna()
    if window:
        returns = returns.tail(window)
    if returns.shape[0] < 2:
        return None
    std = float(returns.std())
    return std if math.isfinite(std) else None


def current_state(features: dict[str, Any]) -> dict[str, Any]:
    moneyflow = features.get("moneyflow", {}) or {}
    return {
        "trend_state": (features.get("trend", {}) or {}).get("trend_state"),
        "volatility_state": (features.get("volatility", {}) or {}).get("volatility_state"),
        "flow_strength_basic": moneyflow.get("flow_strength_basic") or moneyflow.get("moneyflow_strength_basic"),
    }
