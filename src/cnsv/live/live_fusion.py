from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from cnsv.live import LIVE_REPORT_TYPE, LIVE_STAGE, LIVE_VERSION
from cnsv.live.live_evaluator import evaluate_live_manual_decision
from cnsv.live.live_state import build_live_state_payload
from cnsv.live.manual_checklist import build_manual_review_checklist
from cnsv.live.manual_confirmation import build_manual_confirmation_panel
from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS, clean_payload
def build_live_manual_decision_payload(evidence_bundle:dict[str,Any])->dict[str,Any]:
 reports=evidence_bundle["reports"]; av=evidence_bundle["live_decision_evidence_availability"]; risk=reports.get("risk_explanation_report") or {}; sp=build_live_state_payload(reports,av); overview=sp["live_state_overview"]; ltd=overview.get("latest_trade_date") or "N/A"; sid=f"manual-{ltd}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"; snap=f"live-{ltd}-{len(av.get('available_reports',[]))}reports"; checklist=build_manual_review_checklist(risk); panel=build_manual_confirmation_panel(sid,snap,overview["manual_decision_status"],checklist)
 payload={"meta":{"system":"CNSV","version":LIVE_VERSION,"stage":LIVE_STAGE,"report_type":LIVE_REPORT_TYPE,"ts_code":"600150.SH","name":"中国船舶","generated_at":datetime.now(timezone.utc).isoformat(),"latest_trade_date":ltd,"is_trade_signal":False},"cnsvdata_gate":_stage_gate((reports.get("data_report") or {}).get("cnsvdata_gate") or risk.get("cnsvdata_gate") or {}),"live_decision_evidence_availability":av,"live_state_overview":overview,"evidence_dashboard":sp["evidence_dashboard"],"current_state_card":sp["current_state_card"],"path_observation_card":sp["path_observation_card"],"risk_explanation_card":sp["risk_explanation_card"],"evidence_conflict_card":sp["evidence_conflict_card"],"manual_review_checklist":checklist,"manual_confirmation_panel":panel,"manual_decision_status":overview["manual_decision_status"],"manual_review_required":overview["manual_review_required"],"auto_order_enabled":False,"broker_api_enabled":False,"formal_signal_enabled":False,"forbidden_actions":FORBIDDEN_ACTIONS,"next_stage":"V2.0 acceptance and daily manual operation"}
 payload["manual_action_log"]={"decision_session_id":sid,"decision_snapshot_id":snap,"manual_review_status":panel["manual_review_status"],"execution_action_recorded":False}; payload["live_manual_decision_quality"]=evaluate_live_manual_decision(payload); return clean_payload(payload)
def _stage_gate(gate:dict[str,Any])->dict[str,Any]:
 out=dict(gate); out["can_generate_formal_signal"]=False; out["can_auto_order"]=False; out["can_connect_broker_api"]=False; out["live_stage_permission"]="V2.0 supports manual review only."; return out
