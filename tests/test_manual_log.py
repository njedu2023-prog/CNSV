import json
from cnsv.live.manual_log import build_manual_action_log, write_manual_logs
def _payload():
 return {"meta":{"version":"2.0","stage":"V2.0_live_manual_decision_system","latest_trade_date":"2026-06-18"},"manual_confirmation_panel":{"decision_session_id":"session","decision_snapshot_id":"snapshot","manual_review_status":"not_started","operator_notes":""},"manual_decision_status":"review_required","live_decision_evidence_availability":{"available_reports":["risk_explanation_report"],"missing_reports":[]},"live_manual_decision_quality":{"status":"WARN"},"risk_explanation_card":{"overall_risk_level":"high"}}
def test_manual_log_contains_snapshot_and_no_execution_action(tmp_path):
 jp,mp=write_manual_logs(_payload(),tmp_path); log=json.loads(jp.read_text(encoding="utf-8")); assert log["decision_session_id"]=="session"; assert log["evidence_snapshot"]["available_reports"]; assert log["execution_action_recorded"] is False; assert mp.exists()
def test_manual_log_builder_has_session_id(): assert build_manual_action_log(_payload())["decision_session_id"]=="session"
