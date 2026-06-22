from __future__ import annotations

from typing import Any


def build_human_attention_items(
    availability: dict[str, Any],
    support_levels: dict[str, Any],
    consistency_summary: dict[str, Any],
    evidence_conflict_reasons: list[str],
) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for missing in availability.get("missing_reports", []):
        items.append({"category": "data_items", "text": f"需要人工确认上游证据缺失：{missing}。"})
    if support_levels.get("risk_attention_level") == "high":
        items.append({"category": "risk_items", "text": "路径下行或回撤观察偏高，需要人工优先关注风险证据。"})
    if support_levels.get("evidence_strength") in {"weak", "insufficient"}:
        items.append({"category": "evidence_items", "text": "证据强度不足，需要人工降低对单次观察结论的依赖。"})
    for reason in evidence_conflict_reasons:
        items.append({"category": "model_items", "text": f"需要人工复核证据冲突：{reason}"})
    for point in consistency_summary.get("model_disagreement_points", []):
        items.append({"category": "model_items", "text": point})
    if not items:
        items.append({"category": "evidence_items", "text": "上游证据可用，但仍需人工结合市场与行业背景复核。"})
    return items
