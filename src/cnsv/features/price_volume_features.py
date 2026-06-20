from __future__ import annotations

import pandas as pd


def _num(row: pd.Series, *names: str) -> float | None:
    for name in names:
        if name in row and pd.notna(row[name]):
            return float(row[name])
    return None


def _last(series: pd.Series) -> float | None:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    return float(clean.iloc[-1]) if not clean.empty else None


def _mean(series: pd.Series, window: int) -> float | None:
    clean = pd.to_numeric(series, errors="coerce")
    return float(clean.tail(window).mean()) if clean.dropna().shape[0] >= window else None


def _ret(close: pd.Series, days: int) -> float | None:
    clean = pd.to_numeric(close, errors="coerce")
    if clean.dropna().shape[0] < days + 1:
        return None
    base = clean.iloc[-days - 1]
    latest = clean.iloc[-1]
    return float(latest / base - 1) if pd.notna(base) and base else None


def _ratio(series: pd.Series, window: int) -> float | None:
    clean = pd.to_numeric(series, errors="coerce")
    if clean.dropna().shape[0] < window + 1:
        return None
    base = clean.iloc[-window - 1 : -1].mean()
    latest = clean.iloc[-1]
    return float(latest / base) if pd.notna(base) and base else None


def _position(close: pd.Series, high: pd.Series, low: pd.Series, window: int) -> float | None:
    if close.dropna().shape[0] < window or high.dropna().shape[0] < window or low.dropna().shape[0] < window:
        return None
    rolling_high = pd.to_numeric(high, errors="coerce").tail(window).max()
    rolling_low = pd.to_numeric(low, errors="coerce").tail(window).min()
    latest_close = _last(close)
    denominator = rolling_high - rolling_low
    if latest_close is None or not denominator:
        return None
    return float((latest_close - rolling_low) / denominator)


def build_price_volume_features(daily: pd.DataFrame) -> dict[str, float | str | bool | None]:
    if daily.empty:
        return {}
    df = daily.sort_values("trade_date") if "trade_date" in daily.columns else daily.copy()
    close = pd.to_numeric(df["close"], errors="coerce")
    high = pd.to_numeric(df["high"] if "high" in df.columns else df["close"], errors="coerce")
    low = pd.to_numeric(df["low"] if "low" in df.columns else df["close"], errors="coerce")
    vol_col = "vol" if "vol" in df.columns else "volume" if "volume" in df.columns else None
    amount_col = "amount" if "amount" in df.columns else None
    latest = df.iloc[-1]
    volume = pd.to_numeric(df[vol_col], errors="coerce") if vol_col else pd.Series(dtype="float64")
    amount = pd.to_numeric(df[amount_col], errors="coerce") if amount_col else pd.Series(dtype="float64")

    latest_high = _num(latest, "high")
    latest_low = _num(latest, "low")
    high_20 = high.tail(20).max() if high.dropna().shape[0] >= 20 else None
    low_20 = low.tail(20).min() if low.dropna().shape[0] >= 20 else None
    high_60 = high.tail(60).max() if high.dropna().shape[0] >= 60 else None
    low_60 = low.tail(60).min() if low.dropna().shape[0] >= 60 else None
    return {
        "latest_trade_date": str(latest.get("trade_date", "")),
        "latest_open": _num(latest, "open"),
        "latest_high": latest_high,
        "latest_low": latest_low,
        "latest_close": _num(latest, "close"),
        "latest_pre_close": _num(latest, "pre_close", "prev_close"),
        "latest_pct_chg": _num(latest, "pct_chg", "pct_change"),
        "latest_volume": _num(latest, "vol", "volume"),
        "latest_amount": _num(latest, "amount"),
        "ma5": _mean(close, 5),
        "ma10": _mean(close, 10),
        "ma20": _mean(close, 20),
        "ma60": _mean(close, 60),
        "ret_1d": _ret(close, 1),
        "ret_3d": _ret(close, 3),
        "ret_5d": _ret(close, 5),
        "ret_10d": _ret(close, 10),
        "ret_20d": _ret(close, 20),
        "ret_60d": _ret(close, 60),
        "volume_ma5": _mean(volume, 5) if vol_col else None,
        "volume_ma20": _mean(volume, 20) if vol_col else None,
        "volume_ratio_5d": _ratio(volume, 5) if vol_col else None,
        "volume_ratio_20d": _ratio(volume, 20) if vol_col else None,
        "amount_ma5": _mean(amount, 5) if amount_col else None,
        "amount_ma20": _mean(amount, 20) if amount_col else None,
        "amount_ratio_5d": _ratio(amount, 5) if amount_col else None,
        "amount_ratio_20d": _ratio(amount, 20) if amount_col else None,
        "price_position_20d": _position(close, high, low, 20),
        "price_position_60d": _position(close, high, low, 60),
        "new_high_20d": bool(latest_high is not None and high_20 is not None and latest_high >= high_20),
        "new_low_20d": bool(latest_low is not None and low_20 is not None and latest_low <= low_20),
        "new_high_60d": bool(latest_high is not None and high_60 is not None and latest_high >= high_60),
        "new_low_60d": bool(latest_low is not None and low_60 is not None and latest_low <= low_60),
    }
