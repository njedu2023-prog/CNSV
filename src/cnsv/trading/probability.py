from __future__ import annotations

from typing import Any

from cnsv.trading.intraday_next_day_model import fit_intraday_next_day_model
from cnsv.trading.next_day_model import fit_next_day_model


def compute_next_day_probability(reports: dict[str, Any]) -> dict[str, Any]:
    intraday = fit_intraday_next_day_model(reports)
    if intraday.get("model_ready"):
        return intraday
    daily = fit_next_day_model(reports)
    daily.setdefault("prediction_basis", "next_trading_day_close_vs_daily_close")
    daily.setdefault("asof_time", "15:00:00")
    daily["intraday_fallback_reason"] = intraday.get("fallback_reason")
    return daily
