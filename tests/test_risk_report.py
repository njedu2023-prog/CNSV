from cnsv.risk.risk_report import build_risk_explanation_markdown


def test_risk_markdown_contains_stage_and_guardrail():
    text = build_risk_explanation_markdown({"meta": {"version": "1.6", "stage": "V1.6_risk_explanation", "latest_trade_date": "2026-06-18"}, "risk_explanation_quality": {"status": "WARN", "failed_count": 0, "warn_count": 1}, "risk_evidence_availability": {"all_required_available": True, "available_reports": [], "missing_reports": []}, "overall_risk_summary": {"overall_risk_level": "medium", "risk_confidence": "medium", "primary_risk_sources": [], "secondary_risk_sources": [], "human_review_required": True}, "forbidden_actions": ["formal_signal_generation", "auto_order", "broker_api"], "risk_scenario_cards": [], "risk_review_checklist": []})
    assert "CNSV V1.6 风控解释报告" in text
    assert "不是交易信号" in text
    assert "建议买入" not in text
