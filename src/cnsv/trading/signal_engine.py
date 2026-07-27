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
    advice = build_trade_advice(signal, probability, ev, risk)
    return {
        "signal": signal,
        "signal_cn": SIGNAL_CN[signal],
        "decision_reasons": reasons,
        **advice,
    }


def build_trade_advice(
    signal: str,
    probability: dict[str, Any],
    ev: dict[str, Any],
    risk: dict[str, Any],
) -> dict[str, str]:
    if signal == "STRONG_BUY":
        return _advice("BUY", "分批买入；持仓继续持有", "分批买入", "继续持有，可小幅加仓")
    if signal == "BUY":
        return _advice("BUY", "轻仓买入；持仓继续持有", "轻仓买入", "继续持有")
    if signal == "HOLD":
        return _advice("HOLD", "暂不追买；持仓继续持有", "暂不追买", "继续持有，触发止损时卖出")
    if signal == "WATCH":
        return _advice("WAIT", "暂不买入；持仓观察", "暂不买入", "继续观察，不加仓，触发止损时卖出")
    if signal == "REDUCE":
        return _advice("REDUCE", "暂不买入；持仓减仓", "暂不买入", "降低至低仓位")
    if signal == "SELL":
        return _advice("SELL", "不买入；持仓卖出或降至低仓位", "不买入", "卖出或降低至低仓位")
    if signal == "STRONG_SELL":
        return _advice("SELL", "不买入；持仓卖出", "不买入", "优先卖出")

    up = safe_float(probability.get("prob_up_1d"))
    down = safe_float(probability.get("prob_down_1d"))
    direction = probability.get("predicted_direction") or ("UP" if up >= down else "DOWN")
    risk_ev = safe_float(ev.get("risk_adjusted_ev"))
    reasons = risk.get("block_reasons") or []
    hard_data_block = any(
        marker in str(reason)
        for reason in reasons
        for marker in ("数据门禁", "模型不可用", "缺少", "交易日历", "交易日不一致")
    )
    if direction == "DOWN" or risk_ev < 0 or hard_data_block:
        return _advice(
            "NO_BUY_REDUCE",
            "暂不买入；持仓减仓",
            "暂不买入",
            "减至低仓位，触发止损时卖出",
        )
    return _advice(
        "NO_BUY_HOLD",
        "暂不买入；持仓观察",
        "暂不买入",
        "继续持有但不加仓，触发止损时卖出",
    )


def _advice(code: str, summary: str, entry: str, holding: str) -> dict[str, str]:
    return {
        "trade_advice": code,
        "trade_advice_cn": summary,
        "entry_advice": entry,
        "holding_advice": holding,
        "suggested_action": summary,
    }
