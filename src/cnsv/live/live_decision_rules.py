from __future__ import annotations
from typing import Any
def compute_manual_decision_status(evidence:dict[str,Any], risk_report:dict[str,Any]|None)->dict[str,Any]:
 missing=evidence.get("missing_reports") or []; failed=evidence.get("failed_quality_gates") or []; stale=evidence.get("stale_evidence") or []
 rq=((risk_report or {}).get("risk_explanation_quality") or {}).get("status"); rs=(risk_report or {}).get("overall_risk_summary") or {}; conflict=((risk_report or {}).get("evidence_conflict_risk_explanation") or {}).get("evidence_conflict"); p2=(risk_report or {}).get("p2_auxiliary_risk_explanation") or {}; level=rs.get("overall_risk_level")
 if missing or failed or stale: return _state("evidence_incomplete","evidence_incomplete",True,_reasons(missing,failed,stale))
 if rq=="FAIL" or level=="severe" or p2.get("p2_core_dependency_forbidden") is False: return _state("risk_blocked","risk_blocked",True,["risk explanation blocks V2.0 manual use"])
 if bool(rs.get("human_review_required")) or conflict or level=="high": return _state("ready_for_manual_review","review_required",True,["high risk or evidence conflict requires manual review"])
 return _state("ready_for_manual_review","ready_for_manual_review",False,["evidence complete and no blocking risk"])
def _state(system_status:str,manual_status:str,review_required:bool,reasons:list[Any])->dict[str,Any]: return {"overall_system_status":system_status,"manual_decision_status":manual_status,"manual_review_required":review_required,"status_reasons":reasons}
def _reasons(missing:list[Any],failed:list[Any],stale:list[Any])->list[Any]:
 out=[]
 if missing: out.append({"missing_reports":missing})
 if failed: out.append({"failed_quality_gates":failed})
 if stale: out.append({"stale_evidence":stale})
 return out
