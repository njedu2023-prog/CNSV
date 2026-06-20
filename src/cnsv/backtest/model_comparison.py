from __future__ import annotations

from typing import Any


def compare_path_models(metrics: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for horizon in ("5D", "10D", "20D"):
        p0 = metrics.get("P0_historical_path_replay", {}).get(horizon, {})
        p1 = metrics.get("P1_volatility_adjusted_path", {}).get(horizon, {})
        p2 = metrics.get("P2_state_conditional_path", {}).get(horizon, {})
        out[horizon] = {
            "P1_vs_P0_terminal_coverage_delta": _delta(p1.get("terminal_p10_p90_coverage"), p0.get("terminal_p10_p90_coverage")),
            "P1_vs_P0_touch_brier_delta": _delta(_touch_brier(p1), _touch_brier(p0)),
            "P1_vs_P0_drawdown_coverage_delta": _delta(p1.get("drawdown_p10_p90_coverage"), p0.get("drawdown_p10_p90_coverage")),
            "P1_vs_P0_conclusion": _comparison("P1", _touch_brier(p0), _touch_brier(p1)),
            "P2_vs_P1_terminal_coverage_delta": _delta(p2.get("terminal_p10_p90_coverage"), p1.get("terminal_p10_p90_coverage")),
            "P2_vs_P1_touch_brier_delta": _delta(_touch_brier(p2), _touch_brier(p1)),
            "P2_vs_P1_drawdown_coverage_delta": _delta(p2.get("drawdown_p10_p90_coverage"), p1.get("drawdown_p10_p90_coverage")),
            "P2_vs_P1_fallback_rate_delta": _delta(p2.get("fallback_rate"), p1.get("fallback_rate")),
            "P2_vs_P1_conclusion": _comparison("P2", _touch_brier(p1), _touch_brier(p2)),
            "P2_auxiliary_note": "P2 is auxiliary only and must not be used as core decision dependency.",
        }
    return out


def _touch_brier(row: dict[str, Any]) -> float | None:
    values = [row.get(key) for key in ("touch_up_5pct_brier", "touch_down_5pct_brier", "positive_terminal_brier") if row.get(key) is not None]
    return sum(float(v) for v in values) / len(values) if values else None


def _delta(left: Any, right: Any) -> float | None:
    return None if left is None or right is None else float(left) - float(right)


def _comparison(model: str, base_brier: Any, new_brier: Any) -> str:
    if base_brier is None or new_brier is None:
        return "insufficient evidence"
    diff = float(new_brier) - float(base_brier)
    if diff < -0.01:
        return f"{model} improves over {'P0' if model == 'P1' else 'P1'}"
    if diff > 0.01:
        return f"{model} underperforms {'P0' if model == 'P1' else 'P1'}"
    return f"{model} is neutral versus {'P0' if model == 'P1' else 'P1'}"
