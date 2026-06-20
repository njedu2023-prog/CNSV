from __future__ import annotations

import pandas as pd

STATE_COLUMNS = ("trend_state", "volatility_state", "flow_strength_basic")


def _trade_key(frame: pd.DataFrame) -> pd.Series:
    if "trade_date" not in frame.columns:
        return pd.Series(range(len(frame)), index=frame.index, dtype="object")
    return frame["trade_date"].astype(str)


def _build_trend_state(daily: pd.DataFrame) -> pd.Series:
    close = pd.to_numeric(daily["close"], errors="coerce")
    ma5 = close.rolling(5, min_periods=5).mean()
    ma10 = close.rolling(10, min_periods=10).mean()
    ma20 = close.rolling(20, min_periods=20).mean()
    state = pd.Series("neutral", index=daily.index, dtype="object")
    state[(close > ma5) & (ma5 > ma10) & (ma10 > ma20)] = "strong_uptrend"
    state[(close > ma20) & (ma5 > ma20) & (state == "neutral")] = "uptrend"
    state[(close < ma5) & (ma5 < ma10) & (ma10 < ma20)] = "strong_downtrend"
    state[(close < ma20) & (state == "neutral")] = "downtrend"
    state[ma20.isna() | close.isna()] = "unknown"
    return state


def _build_volatility_state(daily: pd.DataFrame) -> pd.Series:
    close = pd.to_numeric(daily["close"], errors="coerce")
    rv20 = close.pct_change().rolling(20, min_periods=20).std() * (252**0.5)
    high_q = rv20.rolling(252, min_periods=30).quantile(0.70)
    low_q = rv20.rolling(252, min_periods=30).quantile(0.30)
    state = pd.Series("unknown", index=daily.index, dtype="object")
    ready = rv20.notna() & high_q.notna() & low_q.notna()
    state[ready & (rv20 >= high_q)] = "high_vol"
    state[ready & (rv20 <= low_q)] = "low_vol"
    state[ready & (rv20 < high_q) & (rv20 > low_q)] = "normal_vol"
    return state


def _build_flow_strength(moneyflow: pd.DataFrame) -> pd.DataFrame:
    if moneyflow.empty or "trade_date" not in moneyflow.columns:
        return pd.DataFrame(columns=["trade_date", "flow_strength_basic"])
    df = moneyflow.sort_values("trade_date").copy()
    net_field = next((name for name in ("net_mf_amount", "main_net_inflow", "net_amount") if name in df.columns), None)
    if not net_field:
        return pd.DataFrame({"trade_date": _trade_key(df), "flow_strength_basic": "unknown"})
    net_amount = pd.to_numeric(df[net_field], errors="coerce")
    if {"buy_lg_amount", "sell_lg_amount", "buy_elg_amount", "sell_elg_amount"}.issubset(df.columns):
        main_force = (
            pd.to_numeric(df["buy_lg_amount"], errors="coerce")
            - pd.to_numeric(df["sell_lg_amount"], errors="coerce")
            + pd.to_numeric(df["buy_elg_amount"], errors="coerce")
            - pd.to_numeric(df["sell_elg_amount"], errors="coerce")
        )
    else:
        main_force = pd.Series(pd.NA, index=df.index, dtype="float64")
    state = pd.Series("mixed", index=df.index, dtype="object")
    state[(main_force > 0) & (net_amount > 0)] = "positive"
    state[(main_force < 0) & (net_amount < 0)] = "negative"
    state[net_amount.isna()] = "unknown"
    return pd.DataFrame({"trade_date": _trade_key(df), "flow_strength_basic": state})


def build_historical_state_daily(daily: pd.DataFrame, moneyflow: pd.DataFrame | None = None) -> pd.DataFrame:
    if daily.empty:
        return daily.copy()
    if "close" not in daily.columns:
        return daily.copy()
    out = daily.sort_values("trade_date").reset_index(drop=True) if "trade_date" in daily.columns else daily.reset_index(drop=True).copy()
    out["trend_state"] = _build_trend_state(out)
    out["volatility_state"] = _build_volatility_state(out)
    flow = _build_flow_strength(moneyflow if isinstance(moneyflow, pd.DataFrame) else pd.DataFrame())
    if not flow.empty:
        out["_state_trade_key"] = _trade_key(out)
        flow = flow.rename(columns={"trade_date": "_state_trade_key"})
        out = out.merge(flow, on="_state_trade_key", how="left", suffixes=("", "_from_moneyflow"))
        out["flow_strength_basic"] = out["flow_strength_basic"].fillna("unknown")
        out = out.drop(columns=["_state_trade_key"])
    else:
        out["flow_strength_basic"] = "unknown"
    return out


def state_coverage(daily: pd.DataFrame) -> dict[str, int | bool]:
    has_columns = set(STATE_COLUMNS).issubset(daily.columns)
    if not has_columns:
        return {"has_state_columns": False, "state_rows": 0, "usable_state_rows": 0}
    state_frame = daily.loc[:, STATE_COLUMNS].astype("object")
    usable = state_frame.notna().all(axis=1) & (state_frame != "unknown").all(axis=1)
    return {
        "has_state_columns": True,
        "state_rows": int(state_frame.notna().all(axis=1).sum()),
        "usable_state_rows": int(usable.sum()),
    }
