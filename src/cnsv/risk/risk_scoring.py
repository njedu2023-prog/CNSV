from __future__ import annotations

from typing import Any


_ORDER = {"low": 0, "medium": 1, "high": 2, "severe": 3}


def worse_level(*levels: str) -> str:
    clean = [level for level in levels if level in _ORDER]
    if not clean:
        return "medium"
    return max(clean, key=lambda item: _ORDER[item])


def score_overall_risk(
    availability: dict[str, Any],
    source_breakdown: dict[str, dict[str, Any]],
    support_report: dict[str, Any] | None,
) -> dict[str, Any]:
    missing = availability.get("missing_reports", [])
    support_quality = ((support_report or {}).get("human_decision_support_quality") or {}).get("status")
    support_levels = (support_report or {}).get("support_levels") or {}
    conflicts = (support_report or {}).get("evidence_conflict_summary") or {}

    if "human_decision_support_report" in missing or support_quality == "FAIL":
        return {
            "overall_risk_level": "severe",
            "risk_confidence": "insufficient",
            "primary_risk_sources": ["decision_support_risk", "evidence_insufficiency_risk"],
            "secondary_risk_sources": [key for key in source_breakdown if key not in {"decision_support_risk"}],
            "human_review_required": True,
            "risk_reason": "V1.5 人工决策辅助证据缺失或失败，V1.6 只能降级解释。",
        }

    levels = {key: value.get("risk_level", "medium") for key, value in source_breakdown.items()}
    overall = worse_level(*levels.values())
    if missing and overall == "low":
        overall = "medium"
    confidence = str(support_levels.get("evidence_strength") or "moderate")
    if missing:
        confidence = "insufficient"
    elif confidence not in {"low", "medium", "high", "insufficient"}:
        confidence = {"weak": "low", "moderate": "medium", "strong": "high"}.get(confidence, "medium")
    primary = [key for key, level in levels.items() if level in {"high", "severe"}] or [key for key, level in levels.items() if level == overall]
    secondary = [key for key in source_breakdown if key not in primary]
    return {
        "overall_risk_level": overall,
        "risk_confidence": confidence,
        "primary_risk_sources": primary,
        "secondary_risk_sources": secondary,
        "human_review_required": bool(support_levels.get("human_review_required") or conflicts.get("evidence_conflict") or missing),
        "risk_reason": "风险等级由数据、特征、模型、路径、回测和人工辅助证据综合得到，仅用于人工复核。",
    }
