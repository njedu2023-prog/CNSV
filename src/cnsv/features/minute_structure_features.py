from __future__ import annotations

import pandas as pd


def build_minute_structure_features(one_min: pd.DataFrame) -> dict[str, float | None]:
    if one_min.empty:
        return {}
    df = one_min.sort_values([c for c in ("trade_date", "datetime", "time") if c in one_min.columns])
    if "trade_date" in df.columns:
        df = df[df["trade_date"] == df["trade_date"].max()]
    close = pd.to_numeric(df["close"], errors="coerce")
    high = pd.to_numeric(df["high"] if "high" in df.columns else df["close"], errors="coerce")
    low = pd.to_numeric(df["low"] if "low" in df.columns else df["close"], errors="coerce")
    latest_close = float(close.iloc[-1])
    intraday_high = float(high.max())
    intraday_low = float(low.min())
    day_range = intraday_high - intraday_low

    def period_return(minutes: int) -> float | None:
        if len(close.dropna()) < minutes + 1:
            return None
        base = float(close.iloc[-minutes - 1])
        return latest_close / base - 1 if base else None

    vol_col = "vol" if "vol" in df.columns else "volume" if "volume" in df.columns else None
    amount_col = "amount" if "amount" in df.columns else None
    return {
        "latest_intraday_high": intraday_high,
        "latest_intraday_low": intraday_low,
        "latest_intraday_close": latest_close,
        "intraday_range_pct": day_range / latest_close if latest_close else None,
        "close_position_in_day_range": (latest_close - intraday_low) / day_range if day_range else None,
        "last_30min_return": period_return(30),
        "last_60min_return": period_return(60),
        "intraday_volume_sum": float(pd.to_numeric(df[vol_col], errors="coerce").sum()) if vol_col else None,
        "intraday_amount_sum": float(pd.to_numeric(df[amount_col], errors="coerce").sum()) if amount_col else None,
    }
