from __future__ import annotations

from typing import Any

from cnsv.trading.utils import safe_float


def evaluate_trading_risk(reports: dict[str, Any], probability: dict[str, Any], distribution: dict[str, Any], ev: dict[str, Any]) -> dict[str, Any]:
    data = reports.get("data_report") or {}
    feature = reports.get("feature_report") or {}
    baseline_validation = reports.get("baseline_validation_report") or {}
    path_validation = reports.get("path_validation_report") or {}
    features = feature.get("features") or {}
    volatility = features.get("volatility") or {}

    gate = data.get("cnsvdata_gate") or feature.get("cnsvdata_gate") or {}
    block_reasons: list[str] = []
    buy_block_reasons: list[str] = []
    warnings: list[str] = []

    if gate.get("ready") is False:
        block_reasons.append("CNSVdata 未就绪")
    if gate.get("status") == "FAIL":
        block_reasons.append("数据门禁失败")
    if gate.get("status") == "WARN":
        buy_block_reasons.append("数据状态为 WARN，不允许正式 BUY")
    if not gate:
        block_reasons.append("缺少 CNSVdata gate")

    validation_status = (baseline_validation.get("validation_quality") or {}).get("status")
    path_validation_status = (path_validation.get("path_validation_quality") or {}).get("status")
    if validation_status == "FAIL" or path_validation_status == "FAIL":
        block_reasons.append("模型验证失败")
    if validation_status == "WARN" or path_validation_status == "WARN":
        warnings.append("模型验证存在 WARN，需要人工复核")

    crash_prob = safe_float((distribution.get("return_bins_1d") or {}).get("lt_minus_5pct"))
    p10 = safe_float(distribution.get("p10_return_1d"))
    confidence = safe_float(probability.get("direction_confidence"))
    risk_ev = safe_float(ev.get("risk_adjusted_ev"))
    if crash_prob >= 0.18:
        buy_block_reasons.append("大跌概率过高")
    if p10 <= -0.05:
        buy_block_reasons.append("预期 P10 跌幅过大")
    if confidence < 0.55:
        buy_block_reasons.append("方向置信度不足")
    if risk_ev < 0:
        buy_block_reasons.append("风险调整 EV 为负")
    if volatility.get("volatility_state") in {"high_vol", "extreme_vol"}:
        buy_block_reasons.append("波动率异常")

    score = 0
    score += 2 if crash_prob >= 0.15 else 1 if crash_prob >= 0.08 else 0
    score += 2 if p10 <= -0.05 else 1 if p10 <= -0.03 else 0
    score += 1 if risk_ev < 0.005 else 0
    score += 1 if volatility.get("volatility_state") in {"high_vol", "extreme_vol"} else 0
    risk_level = "HIGH" if block_reasons or score >= 4 else "MEDIUM_HIGH" if score == 3 else "MEDIUM" if score == 2 else "MEDIUM_LOW" if score == 1 else "LOW"
    return {
        "risk_level": risk_level,
        "risk_level_cn": _risk_cn(risk_level),
        "risk_passed": not block_reasons,
        "blocked": bool(block_reasons),
        "block_reasons": block_reasons,
        "buy_blocked": bool(block_reasons or buy_block_reasons),
        "buy_block_reasons": block_reasons + buy_block_reasons,
        "warnings": warnings,
        "downside_tail_prob": crash_prob,
        "p10_return_1d": p10,
        "human_risk_explanation": _human_explanation(risk_level, block_reasons + buy_block_reasons, crash_prob),
    }


def _risk_cn(level: str) -> str:
    return {
        "LOW": "低风险",
        "MEDIUM_LOW": "中低风险",
        "MEDIUM": "中风险",
        "MEDIUM_HIGH": "中高风险",
        "HIGH": "高风险",
    }[level]


def _human_explanation(level: str, reasons: list[str], crash_prob: float) -> str:
    if reasons:
        return "；".join(reasons) + "，因此需要风控降级或拦截。"
    if level in {"MEDIUM_HIGH", "HIGH"}:
        return "尾部风险偏高，单次交易可能出现较大回撤，必须控制仓位。"
    if crash_prob > 0.08:
        return "大跌概率仍需关注，适合轻仓而非重仓。"
    return "当前硬风控未触发，但仍需人工确认后执行。"
