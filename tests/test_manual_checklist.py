from cnsv.live.manual_checklist import build_manual_review_checklist
def test_manual_checklist_contains_required_items():
 ids={i["id"] for i in build_manual_review_checklist({})}
 assert {"check_data_freshness","check_latest_trade_date","check_path_downside","check_drawdown_exposure","check_model_conflict","check_p2_fallback","check_evidence_conflict","check_risk_level","confirm_no_auto_order"}.issubset(ids)
