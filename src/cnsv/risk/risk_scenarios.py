from __future__ import annotations

from typing import Any


def build_risk_scenario_cards(payload: dict[str, Any]) -> list[dict[str, Any]]:
    path = payload.get("path_distribution_risk_explanation") or {}
    conflict = payload.get("evidence_conflict_risk_explanation") or {}
    p2 = payload.get("p2_auxiliary_risk_explanation") or {}
    data = payload.get("data_risk_explanation") or {}
    availability = payload.get("risk_evidence_availability") or {}
    return [
        _card("downside_touch_risk_card", "下穿路径风险", path.get("touch_down_risk", {}).get("risk_level", "medium"), ["touch_down_5pct_prob"], "下穿概率升高时，风险解释层要求人工复核路径尾部。"),
        _card("max_drawdown_risk_card", "最大回撤风险", path.get("max_drawdown_risk", {}).get("risk_level", "medium"), ["max_drawdown_p50", "max_drawdown_p90"], "历史路径回撤仅表示观察风险，不构成执行参数。"),
        _card("model_conflict_risk_card", "模型分歧风险", conflict.get("risk_level", "medium"), conflict.get("risk_evidence", []), "模型分歧表示证据不一致，需要人工复核。"),
        _card("p2_instability_risk_card", "P2 辅助层不稳定风险", p2.get("p2_auxiliary_risk_level", "medium"), ["P2 fallback_rate", "state_sample_size"], "P2 只作为辅助状态层，禁止作为核心依赖。"),
        _card("data_quality_risk_card", "数据质量风险", data.get("risk_level", "low"), data.get("risk_evidence", []), "数据缺失或门禁异常时，风险解释必须降级。"),
        _card("evidence_insufficiency_risk_card", "证据不足风险", "high" if availability.get("missing_reports") else "low", availability.get("missing_reports", []), "上游证据缺失时不得输出高置信解释。"),
    ]


def _card(scenario_id: str, name: str, level: str, evidence: list[Any], explanation: str) -> dict[str, Any]:
    return {
        "scenario_id": scenario_id,
        "scenario_name": name,
        "risk_level": level,
        "trigger_evidence": evidence,
        "risk_explanation": explanation,
        "historical_support": "来自 V1.0-V1.5 已生成报告的观察证据",
        "human_review_items": ["人工复核证据来源", "确认风险解释未被用作交易动作"],
        "not_trade_signal_statement": "本卡片是风险解释，不是交易信号。",
    }
