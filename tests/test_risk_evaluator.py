from cnsv.risk.risk_evaluator import evaluate_risk_explanation


def _payload():
    return {
        "meta": {"version": "1.6", "stage": "V1.6_risk_explanation", "report_type": "risk_explanation_report", "is_trade_signal": False},
        "risk_evidence_availability": {"missing_reports": []},
        "overall_risk_summary": {"overall_risk_level": "medium"},
        "risk_source_breakdown": {"data_risk": {"risk_level": "low"}},
        "data_risk_explanation": {"risk_level": "low"},
        "feature_risk_explanation": {"risk_level": "low"},
        "baseline_model_risk_explanation": {"risk_level": "low"},
        "path_distribution_risk_explanation": {"risk_level": "medium"},
        "observation_backtest_risk_explanation": {"risk_level": "medium"},
        "decision_support_risk_explanation": {"human_review_required_risk": {"risk_level": "medium"}},
        "p2_auxiliary_risk_explanation": {"p2_core_dependency_forbidden": True},
        "evidence_conflict_risk_explanation": {"evidence_conflict": False},
        "risk_scenario_cards": [{"scenario_id": "downside_touch_risk_card"}],
        "risk_review_checklist": [{"id": "check_data_freshness"}],
        "forbidden_actions": ["formal_signal_generation", "auto_order", "broker_api"],
    }


def test_risk_evaluator_fails_for_forbidden_trade_field():
    payload = _payload()
    payload["buy_signal"] = True
    assert evaluate_risk_explanation(payload)["status"] == "FAIL"


def test_risk_evaluator_accepts_warn_risk_payload():
    quality = evaluate_risk_explanation(_payload())
    assert quality["status"] in {"PASS", "WARN"}
    assert quality["failed_count"] == 0
