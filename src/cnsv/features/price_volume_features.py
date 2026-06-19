from __future__ import annotations

import pandas as pd


def _num(row: pd.Series, *names: str) -> float | None:
    for name in names:
        if name in row and pd.notna(row[name]):
            return float(row[name])
    return None


def build_price_volume_features(daily: pd.DataFrame) -> dict[str, float | None]:
    if daily.empty:
        return {}
    df = daily.sort_values("trade_date") if "trade_date" in daily.columns else daily.copy()
    close = pd.to_numeric(df["close"], errors="coerce")
    vol_col = "vol" if "vol" in df.columns else "volume" if "volume" in df.columns else None
    amount_col = "amount" if "amount" in df.columns else None
    latest = df.iloc[-1]

    def ratio(series: pd.Series, window: int) -> float | None:
        if len(series.dropna()) < window + 1:
            return None
        base = series.iloc[-window - 1 : -1].mean()
        return float(series.iloc[-1] / base) if base else None

    return {
        "latest_close": _num(latest, "close"),
        "latest_pct_chg": _num(latest, "pct_chg", "pct_change"),
        "latest_volume": _num(latest, "vol", "volume"),
        "latest_amount": _num(latest, "amount"),
        "ma5": float(close.tail(5).mean()) if len(close.dropna()) >= 5 else None,
        "ma10": float(close.tail(10).mean()) if len(close.dropna()) >= 10 else None,
        "ma20": float(close.tail(20).mean()) if len(close.dropna()) >= 20 else None,
        "ret_1d": float(close.pct_change(1).iloc[-1]) if len(close.dropna()) >= 2 else None,
        "ret_5d": float(close.pct_change(5).iloc[-1]) if len(close.dropna()) >= 6 else None,
        "ret_20d": float(close.pct_change(20).iloc[-1]) if len(close.dropna()) >= 21 else None,
        "volume_ratio_5d": ratio(pd.to_numeric(df[vol_col], errors="coerce"), 5) if vol_col else None,
        "amount_ratio_5d": ratio(pd.to_numeric(df[amount_col], errors="coerce"), 5) if amount_col else None,
    }
