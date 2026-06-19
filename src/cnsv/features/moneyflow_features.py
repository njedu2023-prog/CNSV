from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd


def build_moneyflow_features(moneyflow: pd.DataFrame, gate: dict[str, Any], latest_trade_date: str = "") -> dict[str, Any]:
    if moneyflow.empty:
        return {
            "main_force_available": False,
            "moneyflow_warning": "moneyflow data is empty",
            "can_use_as_strong_factor": False,
        }
    df = moneyflow.sort_values("trade_date") if "trade_date" in moneyflow.columns else moneyflow.copy()
    latest = df.iloc[-1]
    net_field = next((name for name in ("net_mf_amount", "main_net_inflow", "net_amount", "buy_sm_amount") if name in df.columns), None)
    net_amount = float(latest[net_field]) if net_field and pd.notna(latest[net_field]) else None
    mf_date = str(latest.get("trade_date", ""))
    lag_days = None
    if latest_trade_date and mf_date:
        try:
            lag_days = (date.fromisoformat(latest_trade_date[:10]) - date.fromisoformat(mf_date[:10])).days
        except ValueError:
            lag_days = None
    can_strong = bool(gate.get("can_use_moneyflow_as_strong_factor", False))
    warning = "" if can_strong else "moneyflow is restricted to low-confidence use by CNSVdata gate"
    return {
        "net_mf_amount": net_amount,
        "main_force_available": net_amount is not None,
        "moneyflow_latest_trade_date": mf_date,
        "moneyflow_lag_days": lag_days,
        "moneyflow_strength_basic": "positive" if net_amount and net_amount > 0 else "negative" if net_amount and net_amount < 0 else "neutral",
        "moneyflow_warning": warning,
        "can_use_as_strong_factor": can_strong,
    }
