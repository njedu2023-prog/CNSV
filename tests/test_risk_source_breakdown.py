from cnsv.risk.risk_source_breakdown import build_risk_source_breakdown


def test_risk_source_breakdown_contains_required_sources():
    reports = {
        "data_report": {"validation": {"status": "PASS"}},
        "feature_report": {"feature_quality": {"status": "PASS"}},
        "baseline_model_report": {"baseline_quality": {"status": "PASS"}},
        "baseline_validation_report": {"validation_quality": {"status": "PASS"}},
        "path_distribution_report": {"path_quality": {"status": "PASS"}},
        "path_validation_report": {"path_validation_quality": {"status": "PASS"}},
        "observation_backtest_report": {"observation_backtest_quality": {"status": "PASS"}, "backtest_scope": {"purged_sample_size": 20}},
        "human_decision_support_report": {"human_decision_support_quality": {"status": "WARN"}, "evidence_conflict_summary": {"evidence_conflict": True}},
    }
    breakdown = build_risk_source_breakdown(reports, {"missing_reports": []})
    assert "data_risk" in breakdown
    assert "path_distribution_risk" in breakdown
    assert "evidence_conflict_risk" in breakdown
    assert breakdown["evidence_conflict_risk"]["risk_level"] == "high"
    assert breakdown["observation_backtest_risk"]["source_reports"]
