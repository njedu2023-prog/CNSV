from __future__ import annotations

from typing import Any

from cnsv.trading.return_distribution import BIN_MIDPOINTS
from cnsv.trading.utils import safe_float


def compute_ev(return_distribution: dict[str, Any]) -> dict[str, Any]:
    bins = return_distribution.get("return_bins_1d") or {}
    raw_ev = sum(BIN_MIDPOINTS[key] * safe_float(bins.get(key)) for key in BIN_MIDPOINTS)
    transaction_cost = 0.0015
    downside_tail = safe_float(bins.get("lt_minus_5pct"))
    p10 = safe_float(return_distribution.get("p10_return_1d"))
    risk_penalty = max(0.0, downside_tail * 0.025 + abs(min(p10, 0.0)) * 0.08)
    cost_adjusted = raw_ev - transaction_cost
    risk_adjusted = cost_adjusted - risk_penalty
    return {
        "raw_ev": raw_ev,
        "transaction_cost": transaction_cost,
        "risk_penalty": risk_penalty,
        "cost_adjusted_ev": cost_adjusted,
        "risk_adjusted_ev": risk_adjusted,
        "ev_rating": _rating(risk_adjusted),
        "ev_rating_cn": _rating_cn(risk_adjusted),
    }


def _rating(value: float) -> str:
    if value >= 0.02:
        return "strong_positive"
    if value >= 0.01:
        return "positive"
    if value >= -0.005:
        return "neutral"
    if value < -0.015:
        return "strong_negative"
    return "negative"


def _rating_cn(value: float) -> str:
    return {
        "strong_positive": "强正期望",
        "positive": "正期望",
        "neutral": "中性",
        "negative": "负期望",
        "strong_negative": "明显负期望",
    }[_rating(value)]
