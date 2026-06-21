from cnsv.risk.risk_scoring import score_overall_risk


def test_risk_scoring_degrades_without_human_support():
    result = score_overall_risk(
        {"missing_reports": ["human_decision_support_report"]},
        {"decision_support_risk": {"risk_level": "high"}},
        None,
    )

    assert result["overall_risk_level"] == "severe"
    assert result["risk_confidence"] == "insufficient"
    assert result["human_review_required"] is True


def test_risk_scoring_uses_source_breakdown():
    result = score_overall_risk(
        {"missing_reports": []},
        {"path_distribution_risk": {"risk_level": "high"}, "data_risk": {"risk_level": "low"}},
        {"support_levels": {"evidence_strength": "moderate"}, "evidence_conflict_summary": {"evidence_conflict": False}},
    )

    assert result["overall_risk_level"] == "high"
    assert "path_distribution_risk" in result["primary_risk_sources"]
