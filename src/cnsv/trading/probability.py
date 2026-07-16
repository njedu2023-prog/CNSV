from __future__ import annotations

from typing import Any

from cnsv.trading.intraday_next_day_model import fit_intraday_next_day_model
from cnsv.trading.next_day_model import fit_next_day_model


def compute_next_day_probability(reports: dict[str, Any]) -> dict[str, Any]:
    intraday = fit_intraday_next_day_model(reports)
    if intraday.get("model_ready"):
        return intraday
    realtime = reports.get("intraday_realtime_ready")
    if isinstance(realtime, dict):
        intraday["latest_data_trade_date"] = realtime.get("trade_date") or None
        intraday["asof_time"] = realtime.get("asof_time") or None
        intraday["asof_price"] = realtime.get("asof_price")
        intraday["uses_intraday_snapshot"] = bool(realtime.get("ready"))
        intraday["realtime_status"] = realtime.get("status")
        return intraday
    daily = fit_next_day_model(reports)
    daily.setdefault("prediction_basis", "next_trading_day_close_vs_daily_close")
    daily.setdefault("asof_time", "15:00:00")
    daily["intraday_fallback_reason"] = intraday.get("fallback_reason")
    return daily
