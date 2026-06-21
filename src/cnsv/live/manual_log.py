from __future__ import annotations
import json
from datetime import date
from pathlib import Path
from typing import Any
from cnsv.utils.io import ensure_parent
def build_manual_action_log(payload:dict[str,Any])->dict[str,Any]:
 meta=payload.get("meta") or {}; panel=payload.get("manual_confirmation_panel") or {}
 return {"log_type":"manual_decision_review_log","version":meta.get("version"),"stage":meta.get("stage"),"decision_session_id":panel.get("decision_session_id"),"decision_snapshot_id":panel.get("decision_snapshot_id"),"latest_trade_date":meta.get("latest_trade_date"),"manual_review_status":panel.get("manual_review_status"),"manual_decision_status":payload.get("manual_decision_status"),"evidence_snapshot":{"available_reports":(payload.get("live_decision_evidence_availability") or {}).get("available_reports",[]),"missing_reports":(payload.get("live_decision_evidence_availability") or {}).get("missing_reports",[]),"quality_status":(payload.get("live_manual_decision_quality") or {}).get("status"),"overall_risk_level":(payload.get("risk_explanation_card") or {}).get("overall_risk_level")},"operator_notes":panel.get("operator_notes",""),"execution_action_recorded":False,"manual_only_statement":"仅记录人工复核与证据状态，不记录系统执行动作。"}
def write_manual_logs(payload:dict[str,Any],directory:str|Path)->tuple[Path,Path]:
 base=Path(directory); day=date.today().isoformat(); jp=ensure_parent(base/f"{day}_manual_decision_log.json"); mp=ensure_parent(base/f"{day}_manual_decision_log.md"); log=build_manual_action_log(payload); jp.write_text(json.dumps(log,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8"); mp.write_text(_markdown(log),encoding="utf-8"); return jp,mp
def _markdown(log:dict[str,Any])->str:
 s=log.get("evidence_snapshot") or {}
 return "\n".join(["# CNSV V2.0 人工复核日志","",f"- decision_session_id: {log.get('decision_session_id')}",f"- decision_snapshot_id: {log.get('decision_snapshot_id')}",f"- latest_trade_date: {log.get('latest_trade_date')}",f"- manual_review_status: {log.get('manual_review_status')}",f"- manual_decision_status: {log.get('manual_decision_status')}",f"- available_reports: {', '.join(s.get('available_reports', []))}",f"- missing_reports: {', '.join(s.get('missing_reports', [])) or '无'}",f"- overall_risk_level: {s.get('overall_risk_level')}","","本日志只记录人工复核状态与证据快照，不记录系统执行动作。"])+"\n"
