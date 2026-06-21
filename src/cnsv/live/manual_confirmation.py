from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
def build_manual_confirmation_panel(decision_session_id:str,snapshot_id:str,manual_status:str,checklist:list[dict[str,Any]])->dict[str,Any]:
 status="blocked_by_risk" if manual_status=="risk_blocked" else "blocked_by_missing_evidence" if manual_status=="evidence_incomplete" else "not_started"
 return {"operator_name":"N/A","decision_session_id":decision_session_id,"decision_snapshot_id":snapshot_id,"manual_review_timestamp":datetime.now(timezone.utc).isoformat(),"manual_review_status":status,"operator_notes":"","manual_confirmation_items":[{"id":i["id"],"confirmed":False,"required":i.get("required",True)} for i in checklist],"manual_decision_status":manual_status}
