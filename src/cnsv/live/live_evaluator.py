from __future__ import annotations
import math
from typing import Any
from cnsv.live import ALLOWED_MANUAL_DECISION_STATUS, ALLOWED_MANUAL_REVIEW_STATUS, FORBIDDEN_LIVE_FIELDS, LIVE_STAGE, LIVE_VERSION
from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS
def evaluate_live_manual_decision(payload:dict[str,Any])->dict[str,Any]:
 checks=[]; failed=0; warn=0
 def add(name,passed,detail,warning=False):
  nonlocal failed,warn
  status="PASS" if passed else "WARN" if warning else "FAIL"; warn+=0 if passed or not warning else 1; failed+=0 if passed or warning else 1; checks.append({"name":name,"status":status,"detail":detail})
 meta=payload.get("meta") or {}; ev=payload.get("live_decision_evidence_availability") or {}; panel=payload.get("manual_confirmation_panel") or {}; risk=payload.get("risk_explanation_card") or {}
 add("version_is_2_0",meta.get("version")==LIVE_VERSION,f"version={meta.get('version')}"); add("stage_is_live_manual_decision",meta.get("stage")==LIVE_STAGE,f"stage={meta.get('stage')}"); add("is_trade_signal_false",meta.get("is_trade_signal") is False,"manual cockpit only")
 add("automation_disabled",payload.get("auto_order_enabled") is False and payload.get("broker_api_enabled") is False and payload.get("formal_signal_enabled") is False,"execution switches disabled")
 add("forbidden_actions_present",set(FORBIDDEN_ACTIONS).issubset(set(payload.get("forbidden_actions",[]))),"required forbidden actions present"); add("no_forbidden_live_fields",not _contains_forbidden_key(payload),"no direct trading command fields"); add("finite_payload",_finite(payload),"no NaN/inf values")
 add("risk_explanation_available","risk_explanation_report" not in ev.get("missing_reports",[]),"V1.6 evidence required"); add("no_failed_upstream_unblocked",not(ev.get("failed_quality_gates") and payload.get("manual_decision_status") not in {"evidence_incomplete","risk_blocked"}),"failed upstream gates must block or degrade")
 add("manual_decision_status_allowed",payload.get("manual_decision_status") in ALLOWED_MANUAL_DECISION_STATUS,f"manual_decision_status={payload.get('manual_decision_status')}"); add("manual_review_status_allowed",panel.get("manual_review_status") in ALLOWED_MANUAL_REVIEW_STATUS,f"manual_review_status={panel.get('manual_review_status')}"); add("manual_log_safe",not _manual_log_has_forbidden(payload.get("manual_action_log") or {}),"manual log has no execution action")
 add("missing_reports_warn",not ev.get("missing_reports"),f"missing_reports={ev.get('missing_reports')}",True); add("quality_warnings_warn",not ev.get("warning_quality_gates"),f"warning_quality_gates={len(ev.get('warning_quality_gates',[]))}",True); add("risk_review_warn",not payload.get("manual_review_required"),f"manual_review_required={payload.get('manual_review_required')}",True); add("evidence_conflict_warn",not (payload.get("evidence_conflict_card") or {}).get("evidence_conflict"),"evidence conflict requires manual confirmation",True); add("high_risk_warn",risk.get("overall_risk_level") not in {"high","severe"},f"overall_risk_level={risk.get('overall_risk_level')}",True)
 return {"status":"FAIL" if failed else "WARN" if warn else "PASS","failed_count":failed,"warn_count":warn,"blocking_error_count":failed,"checks":checks}
def _contains_forbidden_key(value:Any)->bool:
 if isinstance(value,dict): return any(str(k) in FORBIDDEN_LIVE_FIELDS or _contains_forbidden_key(v) for k,v in value.items())
 if isinstance(value,list): return any(_contains_forbidden_key(x) for x in value)
 return False
def _finite(value:Any)->bool:
 if isinstance(value,dict): return all(_finite(v) for v in value.values())
 if isinstance(value,list): return all(_finite(x) for x in value)
 if isinstance(value,float): return math.isfinite(value)
 return True
def _manual_log_has_forbidden(log:dict[str,Any])->bool: return any(t in str(log).lower() for t in ["broker_order","buy_signal","sell_signal","target_position","stop_loss","take_profit","target_price"])
