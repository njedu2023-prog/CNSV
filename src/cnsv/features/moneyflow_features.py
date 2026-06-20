from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd


def _num(row: pd.Series, name: str) -> float | None:
    return float(row[name]) if name in row and pd.notna(row[name]) else None


def _net(row: pd.Series, buy: str, sell: str) -> float | None:
    buy_value = _num(row, buy)
    sell_value = _num(row, sell)
    if buy_value is None or sell_value is None:
        return None
    return buy_value - sell_value


def _ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return float(numerator / denominator)


def _clip(value: float, lower: float = -1.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def _continuity(series: pd.Series, window: int) -> int | None:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.shape[0] < window:
        return None
    tail = clean.tail(window)
    return int((tail > 0).sum() - (tail < 0).sum())


def _positive_days(series: pd.Series, window: int) -> int | None:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.shape[0] < window:
        return None
    return int((clean.tail(window) > 0).sum())


def build_moneyflow_features(
    moneyflow: pd.DataFrame,
    gate: dict[str, Any],
    latest_trade_date: str = "",
    daily: pd.DataFrame | None = None,
    price_volume_features: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if moneyflow.empty:
        return {
            "main_force_available": False,
            "moneyflow_warning": "moneyflow data is empty",
            "can_use_as_strong_factor": False,
        }
    df = moneyflow.sort_values("trade_date") if "trade_date" in moneyflow.columns else moneyflow.copy()
    latest = df.iloc[-1]
    net_field = next((name for name in ("net_mf_amount", "main_net_inflow", "net_amount") if name in df.columns), None)
    net_amount = float(latest[net_field]) if net_field and pd.notna(latest[net_field]) else None
    small_order_net = _net(latest, "buy_sm_amount", "sell_sm_amount")
    medium_order_net = _net(latest, "buy_md_amount", "sell_md_amount")
    large_order_net = _net(latest, "buy_lg_amount", "sell_lg_amount")
    extra_large_order_net = _net(latest, "buy_elg_amount", "sell_elg_amount")
    main_force_net = None if large_order_net is None or extra_large_order_net is None else large_order_net + extra_large_order_net
    mf_date = str(latest.get("trade_date", ""))
    lag_days = None
    if latest_trade_date and mf_date:
        try:
            lag_days = (date.fromisoformat(latest_trade_date[:10]) - date.fromisoformat(mf_date[:10])).days
        except ValueError:
            lag_days = None
    latest_amount = None
    if daily is not None and not daily.empty and "amount" in daily.columns:
        daily_df = daily.sort_values("trade_date") if "trade_date" in daily.columns else daily
        latest_amount = float(pd.to_numeric(daily_df.iloc[-1:]["amount"], errors="coerce").iloc[0])
    net_mf_ratio = _ratio(net_amount, latest_amount)
    main_force_ratio = _ratio(main_force_net, latest_amount)
    score = None
    if net_mf_ratio is not None and main_force_ratio is not None:
        score = 50 * _clip(net_mf_ratio / 0.05) + 50 * _clip(main_force_ratio / 0.05)
    can_strong = bool(gate.get("can_use_moneyflow_as_strong_factor", False))
    warnings: list[str] = []
    if not can_strong:
        warnings.append("moneyflow is restricted to low-confidence use by CNSVdata gate")
    required = {
        "buy_sm_amount",
        "sell_sm_amount",
        "buy_md_amount",
        "sell_md_amount",
        "buy_lg_amount",
        "sell_lg_amount",
        "buy_elg_amount",
        "sell_elg_amount",
        "net_mf_amount",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        warnings.append(f"missing moneyflow fields: {missing}")
    if latest_amount in (None, 0):
        warnings.append("daily amount is missing or zero")
    price_features = price_volume_features or {}
    price_ret_1d = price_features.get("ret_1d")
    volume_ratio_5d = price_features.get("volume_ratio_5d")
    price_flow_confirm = bool(
        (price_ret_1d is not None and price_ret_1d > 0 and (net_amount or 0) > 0)
        or (price_ret_1d is not None and price_ret_1d < 0 and (net_amount or 0) < 0)
    )
    price_flow_divergence = bool(
        (price_ret_1d is not None and price_ret_1d > 0 and (net_amount or 0) < 0)
        or (price_ret_1d is not None and price_ret_1d < 0 and (net_amount or 0) > 0)
    )
    if volume_ratio_5d is not None and volume_ratio_5d > 1 and (net_amount or 0) > 0:
        volume_flow_confirm = "inflow_confirmed"
    elif volume_ratio_5d is not None and volume_ratio_5d > 1 and (net_amount or 0) < 0:
        volume_flow_confirm = "outflow_confirmed"
    else:
        volume_flow_confirm = "neutral"
    net_series = pd.to_numeric(df[net_field], errors="coerce") if net_field else pd.Series(dtype="float64")
    flow_reversal_1d = None
    if net_series.dropna().shape[0] >= 2:
        previous = net_series.dropna().iloc[-2]
        current = net_series.dropna().iloc[-1]
        flow_reversal_1d = bool(previous * current < 0)
    flow_reversal_3d = None
    if net_series.dropna().shape[0] >= 4:
        previous_3d = net_series.dropna().iloc[-4:-1].sum()
        current = net_series.dropna().iloc[-1]
        flow_reversal_3d = bool(previous_3d * current < 0)
    if main_force_net is not None and main_force_net > 0 and (net_amount or 0) > 0:
        flow_strength_basic = "positive"
    elif main_force_net is not None and main_force_net < 0 and (net_amount or 0) < 0:
        flow_strength_basic = "negative"
    else:
        flow_strength_basic = "mixed"
    return {
        "net_mf_amount": net_amount,
        "net_mf_ratio": net_mf_ratio,
        "small_order_net": small_order_net,
        "medium_order_net": medium_order_net,
        "large_order_net": large_order_net,
        "extra_large_order_net": extra_large_order_net,
        "main_force_net": main_force_net,
        "main_force_ratio": main_force_ratio,
        "main_force_available": main_force_net is not None,
        "moneyflow_latest_trade_date": mf_date,
        "moneyflow_lag_days": lag_days,
        "moneyflow_strength_basic": flow_strength_basic,
        "flow_strength_basic": flow_strength_basic,
        "flow_strength_score": score,
        "flow_continuity_3d": _continuity(net_series, 3),
        "flow_continuity_5d": _continuity(net_series, 5),
        "flow_continuity_10d": _continuity(net_series, 10),
        "positive_flow_days_5d": _positive_days(net_series, 5),
        "positive_flow_days_10d": _positive_days(net_series, 10),
        "flow_reversal_1d": flow_reversal_1d,
        "flow_reversal_3d": flow_reversal_3d,
        "price_flow_confirm": price_flow_confirm,
        "price_flow_divergence": price_flow_divergence,
        "volume_flow_confirm": volume_flow_confirm,
        "moneyflow_warning": "; ".join(warnings),
        "can_use_as_strong_factor": can_strong,
    }
