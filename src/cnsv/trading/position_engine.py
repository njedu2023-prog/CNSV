from __future__ import annotations

from typing import Any

from cnsv.trading.utils import clamp, safe_float


def compute_position(signal: dict[str, Any], probability: dict[str, Any], ev: dict[str, Any], risk: dict[str, Any]) -> dict[str, Any]:
    sig = signal["signal"]
    ranges = {
        "STRONG_BUY": (0.25, 0.35, "25%~35%", "ADD"),
        "BUY": (0.10, 0.20, "10%~20%", "ADD"),
        "HOLD": (None, None, "维持原仓", "HOLD"),
        "WATCH": (0.0, 0.0, "0%", "WAIT"),
        "REDUCE": (0.10, 0.20, "降至 10%~20%", "REDUCE"),
        "SELL": (0.0, 0.10, "降至 0%~10%", "EXIT_OR_REDUCE"),
        "STRONG_SELL": (0.0, 0.0, "0%", "EXIT"),
        "BLOCKED": (0.0, 0.0, "0%", "BLOCKED"),
    }
    low, high, label, action = ranges[sig]
    if low is None:
        suggested = None
    elif high == low:
        suggested = low
    else:
        quality = clamp((safe_float(probability.get("prob_up_1d")) - safe_float(probability.get("prob_down_1d"))) + safe_float(ev.get("risk_adjusted_ev")) * 5.0, 0.0, 1.0)
        risk_cut = 0.7 if risk.get("risk_level") in {"MEDIUM_HIGH", "HIGH"} else 1.0
        suggested = low + (high - low) * quality * risk_cut
    return {
        "position_action": action,
        "suggested_position_pct": suggested,
        "position_range": label,
        "position_reason": _reason(sig, risk),
        "manual_reference_only": True,
    }


def _reason(signal: str, risk: dict[str, Any]) -> str:
    if signal in {"BUY", "STRONG_BUY"}:
        return "仓位根据上涨概率、EV、波动率和尾部风险共同生成，仅供人工参考。"
    if signal in {"SELL", "STRONG_SELL", "REDUCE"}:
        return "风险收益比转弱，建议降低风险暴露。"
    if signal == "BLOCKED":
        return "风控或数据条件不满足，仓位参考为 0%。"
    if risk.get("buy_blocked"):
        return "存在买入拦截项，不建议主动开仓。"
    return "当前信号不强，仓位以人工复核为准。"
