from __future__ import annotations

import math
from typing import Any

from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS
from cnsv.risk import FORBIDDEN_RISK_FIELDS, RISK_STAGE, RISK_VERSION


def evaluate_risk_explanation(payload: dict[str, Any]) -> dict[str, Any]:
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
    availability = payload.get("risk_evidence_availability") or {}
    summary = payload.get("overall_risk_summary") or {}
    support = payload.get("decision_support_risk_explanation") or {}
    p2 = payload.get("p2_auxiliary_risk_explanation") or {}
    add("version_is_1_6", meta.get("version") == RISK_VERSION, f"version={meta.get('version')}")
    add("stage_is_risk_explanation", meta.get("stage") == RISK_STAGE, f"stage={meta.get('stage')}")
    add("is_trade_signal_false", meta.get("is_trade_signal") is False, "risk explanation only")
    add("forbidden_actions_present", set(FORBIDDEN_ACTIONS).issubset(set(payload.get("forbidden_actions", []))), "required forbidden actions present")
    add("no_forbidden_trade_fields", not _contains_forbidden_key(payload), "no forbidden trading field names")
    add("finite_payload", _finite(payload), "no NaN/inf values")
    add("human_support_available", "human_decision_support_report" not in availability.get("missing_reports", []), "V1.5 evidence required")
    add("required_sections_present", _required_sections_present(payload), "all V1.6 sections exist")
    add("p2_core_dependency_forbidden", p2.get("p2_core_dependency_forbidden") is True, "P2 remains auxiliary")
    add("not_report_named_signal", meta.get("report_type") == "risk_explanation_report", f"report_type={meta.get('report_type')}")
    add("missing_reports_degraded", not availability.get("missing_reports"), f"missing_reports={availability.get('missing_reports')}", warning=True)
    add("support_warn_explained", support.get("human_review_required_risk", {}).get("risk_level") != "high", "V1.5 review risk is explained", warning=True)
    add("evidence_conflict_explained", not (payload.get("evidence_conflict_risk_explanation") or {}).get("evidence_conflict"), "evidence conflict requires review", warning=True)
    add("risk_level_review", summary.get("overall_risk_level") not in {"high", "severe"}, f"overall_risk_level={summary.get('overall_risk_level')}", warning=True)
    status = "FAIL" if failed else "WARN" if warn else "PASS"
    return {"status": status, "failed_count": failed, "warn_count": warn, "blocking_error_count": failed, "checks": checks}


def _required_sections_present(payload: dict[str, Any]) -> bool:
    required = [
        "risk_evidence_availability",
        "overall_risk_summary",
        "risk_source_breakdown",
        "data_risk_explanation",
        "feature_risk_explanation",
        "baseline_model_risk_explanation",
        "path_distribution_risk_explanation",
        "observation_backtest_risk_explanation",
        "decision_support_risk_explanation",
        "p2_auxiliary_risk_explanation",
        "evidence_conflict_risk_explanation",
        "risk_scenario_cards",
        "risk_review_checklist",
    ]
    return all(bool(payload.get(key)) for key in required)


def _contains_forbidden_key(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(key) in FORBIDDEN_RISK_FIELDS or _contains_forbidden_key(inner) for key, inner in value.items())
    if isinstance(value, list):
        return any(_contains_forbidden_key(item) for item in value)
    return False


def _finite(value: Any) -> bool:
    if isinstance(value, dict):
        return all(_finite(inner) for inner in value.values())
    if isinstance(value, list):
        return all(_finite(item) for item in value)
    if isinstance(value, float):
        return math.isfinite(value)
    return True
