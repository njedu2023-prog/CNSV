from cnsv.risk.risk_checklist import build_risk_review_checklist


def test_risk_review_checklist_contains_required_items():
    ids = {item["id"] for item in build_risk_review_checklist()}

    assert "check_data_freshness" in ids
    assert "check_p2_fallback" in ids
    assert "check_human_review_required" in ids
