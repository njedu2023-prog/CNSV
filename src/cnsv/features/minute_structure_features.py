from __future__ import annotations

import pandas as pd


def _safe_ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return float(numerator / denominator)


def build_minute_structure_features(one_min: pd.DataFrame) -> dict[str, float | str | bool | None]:
    if one_min.empty:
        return {}
    df = one_min.sort_values([c for c in ("trade_date", "datetime", "time") if c in one_min.columns])
    if "trade_date" in df.columns:
        df = df[df["trade_date"] == df["trade_date"].max()]
    close = pd.to_numeric(df["close"], errors="coerce")
    open_series = pd.to_numeric(df["open"] if "open" in df.columns else df["close"], errors="coerce")
    high = pd.to_numeric(df["high"] if "high" in df.columns else df["close"], errors="coerce")
    low = pd.to_numeric(df["low"] if "low" in df.columns else df["close"], errors="coerce")
    valid_close = close.dropna()
    if valid_close.empty:
        return {}
    latest_open = float(open_series.dropna().iloc[0]) if not open_series.dropna().empty else None
    latest_close = float(close.iloc[-1])
    intraday_high = float(high.max())
    intraday_low = float(low.min())
    day_range = intraday_high - intraday_low

    def period_return(minutes: int) -> float | None:
        if len(close.dropna()) < minutes + 1:
            return None
        base = float(close.iloc[-minutes - 1])
        return latest_close / base - 1 if base else None

    def slice_return(start: int, end: int) -> float | None:
        part = close.iloc[start:end].dropna()
        if len(part) < 2:
            return None
        base = float(part.iloc[0])
        return float(part.iloc[-1] / base - 1) if base else None

    def volume_ratio(start: int, end: int) -> float | None:
        if not vol_col:
            return None
        volume = pd.to_numeric(df[vol_col], errors="coerce")
        total = float(volume.sum())
        part = float(volume.iloc[start:end].sum())
        return _safe_ratio(part, total)

    vol_col = "vol" if "vol" in df.columns else "volume" if "volume" in df.columns else None
    amount_col = "amount" if "amount" in df.columns else None
    half = max(len(df) // 2, 1)
    last_30_start = max(len(df) - 30, 0)
    last_60_start = max(len(df) - 60, 0)
    close_position = (latest_close - intraday_low) / day_range if day_range else None
    high_to_close_gap = (intraday_high - latest_close) / latest_close if latest_close else None
    return {
        "latest_intraday_date": str(df["trade_date"].max()) if "trade_date" in df.columns else "",
        "latest_intraday_open": latest_open,
        "latest_intraday_high": intraday_high,
        "latest_intraday_low": intraday_low,
        "latest_intraday_close": latest_close,
        "intraday_range_pct": day_range / latest_close if latest_close else None,
        "close_position_in_day_range": close_position,
        "morning_return": slice_return(0, half),
        "afternoon_return": slice_return(half - 1, len(df)),
        "last_30min_return": period_return(30),
        "last_60min_return": period_return(60),
        "morning_volume_ratio": volume_ratio(0, half),
        "afternoon_volume_ratio": volume_ratio(half, len(df)),
        "last_30min_volume_ratio": volume_ratio(last_30_start, len(df)),
        "last_60min_volume_ratio": volume_ratio(last_60_start, len(df)),
        "intraday_volume_sum": float(pd.to_numeric(df[vol_col], errors="coerce").sum()) if vol_col else None,
        "intraday_amount_sum": float(pd.to_numeric(df[amount_col], errors="coerce").sum()) if amount_col else None,
        "late_session_strength": bool((period_return(30) or 0) > 0 and (close_position or 0) > 0.6),
        "late_session_weakness": bool((period_return(30) or 0) < 0 and (close_position or 1) < 0.4),
        "intraday_reversal_flag": bool((close_position or 1) < 0.35 and (high_to_close_gap or 0) > 0.01),
    }
