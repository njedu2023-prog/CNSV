from __future__ import annotations

import math
from typing import Any

import pandas as pd


def pinball_loss(actual: float, predicted: float, quantile: float) -> float:
    error = actual - predicted
    return max(quantile * error, (quantile - 1) * error)


def summarize_prediction_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "sample_size": 0,
            "valid_prediction_count": 0,
            "actual_positive_rate": None,
            "mean_actual_return": None,
            "median_actual_return": None,
            "p10_coverage": None,
            "p90_coverage": None,
            "p10_p90_interval_coverage": None,
            "median_error": None,
            "mean_error": None,
            "mae_median": None,
            "rmse_median": None,
            "positive_prob_brier": None,
            "directional_accuracy": None,
            "pinball_loss_p10": None,
            "pinball_loss_p50": None,
            "pinball_loss_p90": None,
            "fallback_rate": None,
            "avg_state_sample_size": None,
            "min_state_sample_size": None,
            "state_coverage_rate": None,
        }
    frame = pd.DataFrame(rows)
    valid = frame.dropna(subset=["actual_return", "p10_return", "p50_return", "p90_return"])
    if valid.empty:
        return summarize_prediction_rows([])
    actual = pd.to_numeric(valid["actual_return"], errors="coerce")
    p10 = pd.to_numeric(valid["p10_return"], errors="coerce")
    p50 = pd.to_numeric(valid["p50_return"], errors="coerce")
    p90 = pd.to_numeric(valid["p90_return"], errors="coerce")
    positive_prob = pd.to_numeric(valid.get("positive_prob"), errors="coerce")
    actual_positive = actual > 0
    median_error_series = p50 - actual
    fallback = valid.get("fallback_used", pd.Series(False, index=valid.index)).fillna(False).astype(bool)
    if "state_sample_size" in valid.columns:
        state_sample = pd.to_numeric(valid["state_sample_size"], errors="coerce")
    else:
        state_sample = pd.Series([float("nan")] * valid.shape[0], index=valid.index)
    state_known = state_sample.notna()
    pinball_p10 = [pinball_loss(a, p, 0.10) for a, p in zip(actual, p10, strict=False)]
    pinball_p50 = [pinball_loss(a, p, 0.50) for a, p in zip(actual, p50, strict=False)]
    pinball_p90 = [pinball_loss(a, p, 0.90) for a, p in zip(actual, p90, strict=False)]
    return {
        "sample_size": int(frame.shape[0]),
        "valid_prediction_count": int(valid.shape[0]),
        "actual_positive_rate": float(actual_positive.mean()),
        "mean_actual_return": float(actual.mean()),
        "median_actual_return": float(actual.median()),
        "p10_coverage": float((actual >= p10).mean()),
        "p90_coverage": float((actual <= p90).mean()),
        "p10_p90_interval_coverage": float(((actual >= p10) & (actual <= p90)).mean()),
        "median_error": float(median_error_series.median()),
        "mean_error": float(median_error_series.mean()),
        "mae_median": float(median_error_series.abs().mean()),
        "rmse_median": float(math.sqrt((median_error_series**2).mean())),
        "positive_prob_brier": float(((positive_prob - actual_positive.astype(float)) ** 2).mean())
        if positive_prob.notna().any()
        else None,
        "directional_accuracy": float(((p50 >= 0) == actual_positive).mean()),
        "pinball_loss_p10": float(pd.Series(pinball_p10).mean()),
        "pinball_loss_p50": float(pd.Series(pinball_p50).mean()),
        "pinball_loss_p90": float(pd.Series(pinball_p90).mean()),
        "fallback_rate": float(fallback.mean()),
        "avg_state_sample_size": float(state_sample[state_known].mean()) if state_known.any() else None,
        "min_state_sample_size": float(state_sample[state_known].min()) if state_known.any() else None,
        "state_coverage_rate": float(state_known.mean()) if state_known.any() else None,
    }


def compare_b2_vs_b1(metrics: dict[str, Any]) -> dict[str, Any]:
    comparisons: dict[str, Any] = {}
    for mode in ("standard_walk_forward_metrics", "purged_walk_forward_metrics"):
        mode_metrics = metrics.get(mode, {})
        rows: dict[str, Any] = {}
        horizons = sorted({h for model in mode_metrics.values() for h in model})
        for horizon in horizons:
            b1 = mode_metrics.get("B1_historical_distribution", {}).get(horizon, {})
            b2 = mode_metrics.get("B2_state_grouped_distribution", {}).get(horizon, {})
            if not b1 or not b2:
                rows[horizon] = {"conclusion": "insufficient evidence"}
                continue
            brier_delta = _delta(b2.get("positive_prob_brier"), b1.get("positive_prob_brier"))
            pinball_delta = _delta(b2.get("pinball_loss_p50"), b1.get("pinball_loss_p50"))
            coverage_delta = _delta(b2.get("p10_p90_interval_coverage"), b1.get("p10_p90_interval_coverage"))
            accuracy_delta = _delta(b2.get("directional_accuracy"), b1.get("directional_accuracy"))
            median_error_delta = _delta(abs_or_none(b2.get("median_error")), abs_or_none(b1.get("median_error")))
            rows[horizon] = {
                "B2_vs_B1_interval_coverage_delta": coverage_delta,
                "B2_vs_B1_brier_delta": brier_delta,
                "B2_vs_B1_pinball_loss_delta": pinball_delta,
                "B2_vs_B1_directional_accuracy_delta": accuracy_delta,
                "B2_vs_B1_median_error_delta": median_error_delta,
                "B2_vs_B1_conclusion": _comparison_conclusion(brier_delta, pinball_delta, accuracy_delta),
            }
        comparisons[mode] = rows
    return comparisons


def abs_or_none(value: Any) -> float | None:
    if value is None:
        return None
    return abs(float(value))


def _delta(left: Any, right: Any) -> float | None:
    if left is None or right is None:
        return None
    return float(left) - float(right)


def _comparison_conclusion(brier_delta: float | None, pinball_delta: float | None, accuracy_delta: float | None) -> str:
    if brier_delta is None or pinball_delta is None or accuracy_delta is None:
        return "insufficient evidence"
    score = 0
    score += 1 if brier_delta < 0 else -1 if brier_delta > 0 else 0
    score += 1 if pinball_delta < 0 else -1 if pinball_delta > 0 else 0
    score += 1 if accuracy_delta > 0 else -1 if accuracy_delta < 0 else 0
    if score >= 2:
        return "B2 shows improvement"
    if score <= -2:
        return "B2 underperforms B1"
    return "B2 is neutral versus B1"
