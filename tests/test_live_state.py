from cnsv.live.live_state import build_live_state_payload
def test_live_state_payload_contains_required_cards():
 p=build_live_state_payload({"feature_report":{"price_volume":{"latest_close":36.14},"moneyflow":{"main_force_net":1.0,"flow_strength_score":-1.0},"trend":{"trend_state":"downtrend"},"volatility":{"volatility_state":"normal_vol"}},"risk_explanation_report":{"overall_risk_summary":{"overall_risk_level":"high","human_review_required":True},"evidence_conflict_risk_explanation":{"evidence_conflict":True}}},{"missing_reports":[],"failed_quality_gates":[],"stale_evidence":[]})
 assert p["live_state_overview"]["manual_decision_status"]=="review_required"; assert "current_state_card" in p; assert "path_observation_card" in p; assert "evidence_conflict_card" in p
