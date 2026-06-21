from __future__ import annotations

from typing import Any

from cnsv.trading.utils import safe_float


SIGNAL_CN = {
    "STRONG_BUY": "强烈买入",
    "BUY": "建议买入",
    "HOLD": "继续持有",
    "WATCH": "继续观察",
    "REDUCE": "建议减仓",
    "SELL": "建议卖出",
    "STRONG_SELL": "强烈卖出",
    "BLOCKED": "风控阻断",
}


def decide_signal(probability: dict[str, Any], distribution: dict[str, Any], ev: dict[str, Any], risk: dict[str, Any]) -> dict[str, Any]:
    up = safe_float(probability.get("prob_up_1d"))
    down = safe_float(probability.get("prob_down_1d"))
    confidence = safe_float(probability.get("direction_confidence"))
    risk_ev = safe_float(ev.get("risk_adjusted_ev"))
    crash_prob = safe_float((distribution.get("return_bins_1d") or {}).get("lt_minus_5pct"))
    reasons: list[str] = []

    if risk.get("blocked"):
        signal = "BLOCKED"
        reasons = risk.get("block_reasons") or ["数据或模型条件不满足交易决策要求"]
    elif down >= 0.75 or crash_prob >= 0.25 or risk_ev < -0.015 or risk.get("risk_level") == "HIGH":
        signal = "STRONG_SELL"
        reasons = ["下行概率或尾部风险过高，优先保护本金"]
    elif down >= 0.60 or risk_ev < -0.005 or crash_prob >= 0.15:
        signal = "SELL"
        reasons = ["下跌概率、EV 或尾部风险触发卖出条件"]
    elif risk.get("buy_blocked"):
        signal = "WATCH"
        reasons = risk.get("buy_block_reasons") or ["风控不允许主动买入"]
    elif up >= 0.70 and risk_ev >= 0.02 and confidence >= 0.75 and crash_prob < 0.08:
        signal = "STRONG_BUY"
        reasons = ["上涨概率、EV 和方向置信度均达到强买条件"]
    elif up >= 0.60 and risk_ev >= 0.01 and confidence >= 0.65 and crash_prob < 0.12:
        signal = "BUY"
        reasons = ["上涨概率与 EV 为正，风险未触发买入拦截"]
    elif down > up and risk_ev < 0.002:
        signal = "REDUCE"
        reasons = ["下行概率占优且 EV 偏弱，适合降低仓位"]
    elif 0.45 <= up <= 0.60 and risk_ev >= -0.005:
        signal = "HOLD"
        reasons = ["概率与 EV 暂未形成强方向，持仓可继续观察"]
    else:
        signal = "WATCH"
        reasons = ["信号强度不足，适合观察而非主动交易"]
    return {
        "signal": signal,
        "signal_cn": SIGNAL_CN[signal],
        "suggested_action": _action(signal),
        "decision_reasons": reasons,
    }


def _action(signal: str) -> str:
    return {
        "STRONG_BUY": "分批参与，仍需控制仓位",
        "BUY": "轻仓参与",
        "HOLD": "持仓继续观察",
        "WATCH": "观察等待",
        "REDUCE": "降低仓位",
        "SELL": "降低至低仓位或退出",
        "STRONG_SELL": "优先退出",
        "BLOCKED": "不允许输出买卖建议",
    }[signal]
