from __future__ import annotations

import math
from typing import Any

from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS
from cnsv.support import FORBIDDEN_SUPPORT_FIELDS, SUPPORT_VERSION


def evaluate_human_decision_support(payload: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    failed = 0
    warn = 0

    def add(name: str, passed: bool, detail: str, warning: bool = False) -> None:
        nonlocal failed, warn
        if passed:
            status = "PASS"
        elif warning:
            status = "WARN"
            warn += 1
        else:
            status = "FAIL"
            failed += 1
        checks.append({"name": name, "status": status, "detail": detail})

    meta = payload.get("meta") or {}
    support = payload.get("support_levels") or {}
    availability = payload.get("evidence_availability") or {}
    add("version_is_1_5", meta.get("version") == SUPPORT_VERSION, f"version={meta.get('version')}")
    add("is_trade_signal_false", meta.get("is_trade_signal") is False, "V1.5 remains observation support only")
    add("forbidden_actions_present", set(FORBIDDEN_ACTIONS).issubset(set(payload.get("forbidden_actions", []))), "required forbidden actions present")
    add("no_forbidden_trade_fields", not _contains_forbidden_key(payload), "no forbidden trade action field names")
    add("finite_payload", _finite(payload), "no NaN/inf values")
    add("observation_backtest_available", "observation_backtest_report" not in availability.get("missing_reports", []), "V1.4 evidence required")
    add("evidence_availability_present", bool(availability), "evidence availability exists")
    add("current_state_summary_present", bool(payload.get("current_state_summary")), "current state exists")
    add("model_evidence_summary_present", bool(payload.get("model_evidence_summary")), "model evidence exists")
    add("path_observations_present", bool(payload.get("path_opportunity_observation")) and bool(payload.get("path_risk_observation")), "path observations exist")
    add("attention_items_present", bool(payload.get("human_attention_items")), "human attention items exist")
    add("review_checklist_present", bool(payload.get("human_review_checklist")), "human review checklist exists")
    add("p2_is_auxiliary", "辅助" in str((payload.get("model_consistency_summary") or {}).get("p2_role")), "P2 remains auxiliary")
    add("missing_reports_degraded", not availability.get("missing_reports"), f"missing_reports={availability.get('missing_reports')}", warning=True)
    add("evidence_strength_not_insufficient", support.get("evidence_strength") != "insufficient", f"evidence_strength={support.get('evidence_strength')}", warning=True)
    add("human_review_flag", support.get("human_review_required") is False, f"human_review_required={support.get('human_review_required')}", warning=True)
    add("evidence_conflict", not (payload.get("evidence_conflict_summary") or {}).get("evidence_conflict"), "evidence conflict requires human review", warning=True)
    status = "FAIL" if failed else "WARN" if warn else "PASS"
    return {"status": status, "failed_count": failed, "warn_count": warn, "blocking_error_count": failed, "checks": checks}


def _contains_forbidden_key(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(k) in FORBIDDEN_SUPPORT_FIELDS or _contains_forbidden_key(v) for k, v in value.items())
    if isinstance(value, list):
        return any(_contains_forbidden_key(v) for v in value)
    return False


def _finite(value: Any) -> bool:
    if isinstance(value, dict):
        return all(_finite(inner) for inner in value.values())
    if isinstance(value, list):
        return all(_finite(item) for item in value)
    if isinstance(value, float):
        return math.isfinite(value)
    return True
