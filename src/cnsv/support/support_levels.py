from __future__ import annotations

from typing import Any


def derive_support_levels(
    evidence_strength: str,
    model_consistency_level: str,
    risk_attention_level: str,
    evidence_conflict: bool,
    missing_reports: list[str],
) -> dict[str, Any]:
    if missing_reports or evidence_strength == "insufficient":
        priority = "low"
    elif evidence_conflict or risk_attention_level == "high":
        priority = "high"
    else:
        priority = "medium"
    return {
        "observation_priority": priority,
        "risk_attention_level": risk_attention_level,
        "evidence_strength": evidence_strength,
        "model_consistency_level": model_consistency_level,
        "human_review_required": True,
    }


def classify_evidence_strength(quality_statuses: dict[str, str], standard_sample_size: int, purged_sample_size: int, high_fallback: bool) -> str:
    if any(status in {"MISSING", "FAIL"} for status in quality_statuses.values()):
        return "insufficient"
    if standard_sample_size < 100 or purged_sample_size < 30:
        return "weak"
    if high_fallback:
        return "moderate"
    if all(status == "PASS" for status in quality_statuses.values()):
        return "strong"
    return "moderate"


def classify_risk_attention(path_models: dict[str, Any]) -> str:
    p1_20d = ((path_models.get("P1_volatility_adjusted_path") or {}).get("horizons") or {}).get("20D") or {}
    touch_down = float(p1_20d.get("touch_down_5pct_prob") or 0)
    drawdown = abs(float(p1_20d.get("max_drawdown_p50") or 0))
    if touch_down >= 0.45 or drawdown >= 0.08:
        return "high"
    if touch_down >= 0.25 or drawdown >= 0.04:
        return "medium"
    return "low"
