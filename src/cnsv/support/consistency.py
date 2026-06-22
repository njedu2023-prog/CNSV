from __future__ import annotations

from typing import Any


def build_model_consistency_summary(
    baseline_models: dict[str, Any],
    path_models: dict[str, Any],
    model_comparison: dict[str, Any],
) -> dict[str, Any]:
    disagreements: list[str] = []
    consistency_notes: list[str] = []
    b1 = _horizon(baseline_models, "B1_historical_distribution", "20D")
    b3 = _horizon(baseline_models, "B3_volatility_adjusted", "20D")
    p0 = _horizon(path_models, "P0_historical_path_replay", "20D")
    p1 = _horizon(path_models, "P1_volatility_adjusted_path", "20D")
    if b1 and b3:
        if _direction(b1.get("median_return")) != _direction(b3.get("median_return")):
            disagreements.append("B1 与 B3 的 20D 中位收益方向不一致，需要人工复核。")
        else:
            consistency_notes.append("B1 与 B3 的 20D 中位收益方向基本一致。")
    else:
        disagreements.append("B1/B3 20D 证据不足，无法判断基准模型一致性。")
    if p0 and p1:
        if _direction(p0.get("terminal_return_p50")) != _direction(p1.get("terminal_return_p50")):
            disagreements.append("P0 与 P1 的 20D 路径中位收益方向不一致，需要人工复核。")
        else:
            consistency_notes.append("P0 与 P1 的 20D 路径中位收益方向基本一致。")
    else:
        disagreements.append("P0/P1 20D 路径证据不足，无法判断路径模型一致性。")
    for horizon, row in (model_comparison or {}).items():
        p2_conclusion = str(row.get("P2_vs_P1_conclusion") or "")
        p2_note = str(row.get("P2_auxiliary_note") or "")
        if "underperform" in p2_conclusion or "fallback" in p2_note.lower():
            disagreements.append(f"{horizon} P2 与 P1 存在辅助层不确定性，P2 只能作为辅助观察。")
        else:
            consistency_notes.append(f"{horizon} P2 对比 P1 未显示阻断性分歧。")
    if not consistency_notes and disagreements:
        level = "insufficient_evidence"
    elif len(disagreements) >= 3:
        level = "mixed"
    elif disagreements:
        level = "mostly_consistent"
    else:
        level = "consistent"
    return {
        "model_consistency_status": level,
        "model_consistency_level": level,
        "model_disagreement_points": disagreements,
        "evidence_conflict_summary": consistency_notes,
        "p2_role": "辅助状态层，不作为核心决策依赖",
    }


def _horizon(models: dict[str, Any], model_id: str, horizon: str) -> dict[str, Any]:
    return ((models.get(model_id) or {}).get("horizons") or {}).get(horizon) or {}


def _direction(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "unknown"
    if number > 0:
        return "positive"
    if number < 0:
        return "negative"
    return "flat"
