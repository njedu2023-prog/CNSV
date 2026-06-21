from cnsv.live.live_evaluator import evaluate_live_manual_decision
def _payload():
 return {"meta":{"version":"2.0","stage":"V2.0_live_manual_decision_system","report_type":"live_manual_decision_report","is_trade_signal":False},"live_decision_evidence_availability":{"missing_reports":[],"failed_quality_gates":[],"warning_quality_gates":[]},"risk_explanation_card":{"overall_risk_level":"medium"},"evidence_conflict_card":{"evidence_conflict":False},"manual_confirmation_panel":{"manual_review_status":"not_started"},"manual_decision_status":"ready_for_manual_review","manual_review_required":False,"auto_order_enabled":False,"broker_api_enabled":False,"formal_signal_enabled":False,"forbidden_actions":["formal_signal_generation","auto_order","broker_api"],"manual_action_log":{"execution_action_recorded":False}}
def test_live_evaluator_requires_disabled_execution_switches():
 p=_payload(); p["auto_order_enabled"]=True; assert evaluate_live_manual_decision(p)["status"]=="FAIL"
def test_live_evaluator_fails_for_direct_trade_field():
 p=_payload(); p["target_position"]=0.5; assert evaluate_live_manual_decision(p)["status"]=="FAIL"
def test_live_evaluator_accepts_manual_payload():
 q=evaluate_live_manual_decision(_payload()); assert q["status"] in {"PASS","WARN"}; assert q["failed_count"]==0
