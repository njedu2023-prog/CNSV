from __future__ import annotations

from typing import Any

import numpy as np

from cnsv.backtest.backtest_metrics import summarize_observation_rows


TOUCH_UP_METRICS = ("touch_up_3pct_prob", "touch_up_5pct_prob", "touch_up_8pct_prob")
TOUCH_DOWN_METRICS = ("touch_down_3pct_prob", "touch_down_5pct_prob", "touch_down_8pct_prob")
DRAWDOWN_METRICS = ("max_drawdown_p50", "max_drawdown_p90", "max_down_return_p10", "max_down_return_p50")
UPSIDE_METRICS = ("max_up_return_p50", "max_up_return_p90", "touch_up_5pct_prob", "positive_terminal_prob")


def build_bucket_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "touch_probability_groups": _bucket_family(rows, TOUCH_UP_METRICS + TOUCH_DOWN_METRICS),
        "drawdown_risk_groups": _bucket_family(rows, DRAWDOWN_METRICS),
        "upside_path_groups": _bucket_family(rows, UPSIDE_METRICS),
        "p2_state_groups": _p2_state_groups(rows),
    }


def build_condition_quality(rows: list[dict[str, Any]]) -> dict[str, Any]:
    quality: dict[str, Any] = {}
    for family, metrics in {
        "touch_probability_groups": TOUCH_UP_METRICS + TOUCH_DOWN_METRICS,
        "drawdown_risk_groups": DRAWDOWN_METRICS,
        "upside_path_groups": UPSIDE_METRICS,
    }.items():
        quality[family] = {}
        for metric in metrics:
            quality[family][metric] = _condition_quality(rows, metric)
    return quality


def bucket_metric(rows: list[dict[str, Any]], metric: str) -> dict[str, Any]:
    clean = [row for row in rows if row.get(metric) is not None]
    if not clean:
        return {"bucket_count": 0, "buckets": {}}
    values = [float(row[metric]) for row in clean]
    q1, q2 = np.quantile(values, [1 / 3, 2 / 3])
    buckets = {
        "low": [row for row in clean if float(row[metric]) <= q1],
        "mid": [row for row in clean if q1 < float(row[metric]) <= q2],
        "high": [row for row in clean if float(row[metric]) > q2],
    }
    return {
        "metric": metric,
        "bucket_count": len([name for name, group in buckets.items() if group]),
        "cut_points": {"low_mid": float(q1), "mid_high": float(q2)},
        "buckets": {name: _bucket_summary(group, metric) for name, group in buckets.items()},
    }


def _bucket_family(rows: list[dict[str, Any]], metrics: tuple[str, ...]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for model_id in sorted({row.get("model_id") for row in rows if row.get("model_id")}):
        out[model_id] = {}
        for horizon in ("5D", "10D", "20D"):
            group = [row for row in rows if row.get("model_id") == model_id and row.get("horizon") == horizon]
            out[model_id][horizon] = {metric: bucket_metric(group, metric) for metric in metrics}
    return out


def _bucket_summary(rows: list[dict[str, Any]], metric: str) -> dict[str, Any]:
    summary = summarize_observation_rows(rows)
    return {
        "sample_size": summary.get("sample_size", 0),
        "metric_mean": _mean(rows, metric),
        "actual_touch_rate": _actual_touch_rate(rows, metric),
        "actual_terminal_positive_rate": summary.get("actual_positive_terminal_rate"),
        "mean_terminal_return": summary.get("mean_terminal_return"),
        "median_terminal_return": summary.get("median_terminal_return"),
        "p10_terminal_return": summary.get("p10_terminal_return"),
        "p90_terminal_return": summary.get("p90_terminal_return"),
        "actual_max_drawdown_median": summary.get("actual_max_drawdown_median"),
        "actual_max_drawdown_p90": summary.get("actual_max_drawdown_p90"),
        "actual_touch_up_5pct_rate": summary.get("actual_touch_up_5pct_rate"),
        "actual_touch_up_8pct_rate": summary.get("actual_touch_up_8pct_rate"),
        "actual_touch_down_5pct_rate": summary.get("actual_touch_down_5pct_rate"),
        "actual_touch_down_8pct_rate": summary.get("actual_touch_down_8pct_rate"),
    }


def _condition_quality(rows: list[dict[str, Any]], metric: str) -> dict[str, Any]:
    grouped = bucket_metric(rows, metric)
    buckets = grouped.get("buckets", {})
    low, high = buckets.get("low", {}), buckets.get("high", {})
    low_n, high_n = low.get("sample_size", 0), high.get("sample_size", 0)
    return_delta = _delta(high.get("mean_terminal_return"), low.get("mean_terminal_return"))
    touch_delta = _delta(high.get("actual_touch_rate"), low.get("actual_touch_rate"))
    drawdown_delta = _delta(high.get("actual_max_drawdown_p90"), low.get("actual_max_drawdown_p90"))
    monotonicity = _monotonicity_score([buckets.get(name, {}).get("mean_terminal_return") for name in ("low", "mid", "high")])
    calibration = _calibration_error(grouped)
    return {
        "bucket_count": grouped.get("bucket_count", 0),
        "high_bucket_sample_size": high_n,
        "low_bucket_sample_size": low_n,
        "high_vs_low_actual_return_delta": return_delta,
        "high_vs_low_actual_touch_delta": touch_delta,
        "high_vs_low_drawdown_delta": drawdown_delta,
        "monotonicity_score": monotonicity,
        "calibration_error": calibration,
        "conclusion": _conclusion(low_n, high_n, return_delta, touch_delta, monotonicity),
    }


def _p2_state_groups(rows: list[dict[str, Any]]) -> dict[str, Any]:
    p2_rows = [row for row in rows if row.get("model_id") == "P2_state_conditional_path"]
    out: dict[str, Any] = {}
    for horizon in ("5D", "10D", "20D"):
        out[horizon] = {}
        h_rows = [row for row in p2_rows if row.get("horizon") == horizon]
        for state in sorted({str(row.get("state_key")) for row in h_rows}):
            group = [row for row in h_rows if str(row.get("state_key")) == state]
            summary = summarize_observation_rows(group)
            out[horizon][state] = {
                "sample_size": summary.get("sample_size"),
                "fallback_rate": summary.get("fallback_rate"),
                "actual_positive_terminal_rate": summary.get("actual_positive_terminal_rate"),
                "actual_touch_up_5pct_rate": summary.get("actual_touch_up_5pct_rate"),
                "actual_touch_down_5pct_rate": summary.get("actual_touch_down_5pct_rate"),
                "actual_max_drawdown_p90": summary.get("actual_max_drawdown_p90"),
            }
    return out


def _actual_touch_rate(rows: list[dict[str, Any]], metric: str) -> float | None:
    if "touch_up_3pct" in metric:
        key = "actual_touch_up_3pct"
    elif "touch_up_5pct" in metric:
        key = "actual_touch_up_5pct"
    elif "touch_up_8pct" in metric:
        key = "actual_touch_up_8pct"
    elif "touch_down_3pct" in metric:
        key = "actual_touch_down_3pct"
    elif "touch_down_5pct" in metric:
        key = "actual_touch_down_5pct"
    elif "touch_down_8pct" in metric:
        key = "actual_touch_down_8pct"
    else:
        key = "actual_positive_terminal"
    values = [bool(row.get(key)) for row in rows if row.get(key) is not None]
    return float(sum(values) / len(values)) if values else None


def _mean(rows: list[dict[str, Any]], key: str) -> float | None:
    values = [float(row[key]) for row in rows if row.get(key) is not None and np.isfinite(float(row[key]))]
    return float(np.mean(values)) if values else None


def _delta(left: Any, right: Any) -> float | None:
    return None if left is None or right is None else float(left) - float(right)


def _monotonicity_score(values: list[Any]) -> float | None:
    clean = [float(v) for v in values if v is not None]
    if len(clean) < 3:
        return None
    up = clean[0] <= clean[1] <= clean[2]
    down = clean[0] >= clean[1] >= clean[2]
    return 1.0 if up or down else 0.0


def _calibration_error(grouped: dict[str, Any]) -> float | None:
    errors = []
    for bucket in grouped.get("buckets", {}).values():
        pred, actual = bucket.get("metric_mean"), bucket.get("actual_touch_rate")
        if pred is not None and actual is not None:
            errors.append(abs(float(pred) - float(actual)))
    return float(np.mean(errors)) if errors else None


def _conclusion(low_n: int, high_n: int, ret_delta: Any, touch_delta: Any, monotonicity: Any) -> str:
    if low_n < 5 or high_n < 5:
        return "insufficient_evidence"
    signal = max(abs(float(ret_delta or 0)), abs(float(touch_delta or 0)))
    if signal >= 0.08 and monotonicity == 1.0:
        return "useful_observation"
    if signal >= 0.04:
        return "neutral_observation"
    if signal >= 0.02:
        return "weak_observation"
    return "unstable_observation"
