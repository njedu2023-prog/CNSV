from __future__ import annotations

from typing import Any

from cnsv.trading.utils import clamp, get_path, mean, safe_float


def compute_next_day_probability(reports: dict[str, Any]) -> dict[str, Any]:
    baseline = reports.get("baseline_model_report") or {}
    path = reports.get("path_distribution_report") or {}
    features = (reports.get("feature_report") or {}).get("features") or {}
    price = features.get("price_volume") or {}
    moneyflow = features.get("moneyflow") or {}

    b1_5d = get_path(baseline, "baseline_models", "B1_historical_distribution", "horizons", "5D", default={})
    b2_5d = get_path(baseline, "baseline_models", "B2_state_grouped_distribution", "horizons", "5D", default={})
    p2_5d = get_path(path, "path_models", "P2_state_conditional_path", "horizons", "5D", default={})
    p1_5d = get_path(path, "path_models", "P1_volatility_adjusted_path", "horizons", "5D", default={})

    up_base = mean(
        [
            safe_float(b1_5d.get("positive_prob"), 0.5),
            safe_float(b2_5d.get("positive_prob"), safe_float(b1_5d.get("positive_prob"), 0.5)),
            safe_float(p2_5d.get("positive_terminal_prob"), safe_float(p1_5d.get("positive_terminal_prob"), 0.5)),
        ],
        0.5,
    )
    down_base = mean(
        [
            safe_float(b1_5d.get("negative_prob"), 1.0 - up_base),
            1.0 - safe_float(b2_5d.get("positive_prob"), up_base),
            1.0 - safe_float(p2_5d.get("positive_terminal_prob"), up_base),
        ],
        1.0 - up_base,
    )

    ret_1d = safe_float(price.get("ret_1d"))
    flow_score = safe_float(moneyflow.get("flow_strength_score"))
    main_force = safe_float(moneyflow.get("main_force_net"))
    adjustment = 0.0
    adjustment += clamp(ret_1d, -0.03, 0.03) * 0.7
    adjustment += clamp(flow_score / 100.0, -0.05, 0.05)
    adjustment += 0.015 if main_force > 0 else -0.01 if main_force < 0 else 0.0

    prob_up = clamp(up_base + adjustment, 0.05, 0.9)
    prob_down = clamp(down_base - adjustment * 0.6, 0.05, 0.9)
    total = prob_up + prob_down
    if total > 0.96:
        scale = 0.96 / total
        prob_up *= scale
        prob_down *= scale
    prob_flat = clamp(1.0 - prob_up - prob_down, 0.0, 0.2)
    confidence = clamp(0.5 + abs(prob_up - prob_down) * 0.7 + min(abs(adjustment), 0.08), 0.35, 0.85)

    fallback_used = not bool(b2_5d) or bool(b2_5d.get("fallback_used"))
    fallback_reason = b2_5d.get("fallback_reason") if fallback_used else None
    return {
        "prob_up_1d": prob_up,
        "prob_down_1d": prob_down,
        "prob_flat_1d": prob_flat,
        "direction_confidence": confidence,
        "primary_model": "B2_state_grouped_distribution+P2_state_conditional_path",
        "fallback_used": fallback_used,
        "fallback_reason": fallback_reason,
        "inputs": {
            "b1_positive_prob_5d": b1_5d.get("positive_prob"),
            "b2_positive_prob_5d": b2_5d.get("positive_prob"),
            "p2_positive_terminal_prob_5d": p2_5d.get("positive_terminal_prob"),
            "ret_1d": ret_1d,
            "flow_strength_score": flow_score,
            "main_force_net": main_force,
        },
    }
