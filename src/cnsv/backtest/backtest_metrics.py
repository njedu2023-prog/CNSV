from __future__ import annotations

from typing import Any

import numpy as np


def summarize_observation_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"sample_size": 0}
    return {
        "sample_size": len(rows),
        "actual_positive_terminal_rate": _bool_rate(rows, "actual_positive_terminal"),
        "mean_terminal_return": _mean(rows, "actual_terminal_return"),
        "median_terminal_return": _quantile(rows, "actual_terminal_return", 0.50),
        "p10_terminal_return": _quantile(rows, "actual_terminal_return", 0.10),
        "p90_terminal_return": _quantile(rows, "actual_terminal_return", 0.90),
        "actual_touch_up_3pct_rate": _bool_rate(rows, "actual_touch_up_3pct"),
        "actual_touch_up_5pct_rate": _bool_rate(rows, "actual_touch_up_5pct"),
        "actual_touch_up_8pct_rate": _bool_rate(rows, "actual_touch_up_8pct"),
        "actual_touch_down_3pct_rate": _bool_rate(rows, "actual_touch_down_3pct"),
        "actual_touch_down_5pct_rate": _bool_rate(rows, "actual_touch_down_5pct"),
        "actual_touch_down_8pct_rate": _bool_rate(rows, "actual_touch_down_8pct"),
        "actual_max_up_return_mean": _mean(rows, "actual_max_up_return"),
        "actual_max_up_return_median": _quantile(rows, "actual_max_up_return", 0.50),
        "actual_max_down_return_mean": _mean(rows, "actual_max_down_return"),
        "actual_max_down_return_median": _quantile(rows, "actual_max_down_return", 0.50),
        "actual_max_drawdown_mean": _mean(rows, "actual_max_drawdown"),
        "actual_max_drawdown_median": _quantile(rows, "actual_max_drawdown", 0.50),
        "actual_max_drawdown_p90": _quantile(rows, "actual_max_drawdown", 0.90),
        "terminal_return_mae_vs_p50": _mae(rows, "terminal_return_p50", "actual_terminal_return"),
        "terminal_return_rmse_vs_p50": _rmse(rows, "terminal_return_p50", "actual_terminal_return"),
        "terminal_p10_p90_coverage": _coverage(rows, "actual_terminal_return", "terminal_return_p10", "terminal_return_p90"),
        "max_up_p10_p90_coverage": _coverage(rows, "actual_max_up_return", "max_up_return_p10", "max_up_return_p90"),
        "max_down_p10_p90_coverage": _coverage(rows, "actual_max_down_return", "max_down_return_p10", "max_down_return_p90"),
        "drawdown_p10_p90_coverage": _coverage(rows, "actual_max_drawdown", "max_drawdown_p10", "max_drawdown_p90"),
        "touch_up_3pct_brier": _brier(rows, "touch_up_3pct_prob", "actual_touch_up_3pct"),
        "touch_up_5pct_brier": _brier(rows, "touch_up_5pct_prob", "actual_touch_up_5pct"),
        "touch_up_8pct_brier": _brier(rows, "touch_up_8pct_prob", "actual_touch_up_8pct"),
        "touch_down_3pct_brier": _brier(rows, "touch_down_3pct_prob", "actual_touch_down_3pct"),
        "touch_down_5pct_brier": _brier(rows, "touch_down_5pct_prob", "actual_touch_down_5pct"),
        "touch_down_8pct_brier": _brier(rows, "touch_down_8pct_prob", "actual_touch_down_8pct"),
        "positive_terminal_brier": _brier(rows, "positive_terminal_prob", "actual_positive_terminal"),
        "fallback_rate": _bool_rate(rows, "fallback_used"),
        "avg_state_sample_size": _mean(rows, "state_sample_size"),
        "model_coverage_rate": _coverage_rate(rows),
    }


def metrics_by_model_horizon(rows: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for model_id in sorted({row.get("model_id") for row in rows if row.get("model_id")}):
        out[model_id] = {}
        for horizon in ("5D", "10D", "20D"):
            out[model_id][horizon] = summarize_observation_rows([row for row in rows if row.get("model_id") == model_id and row.get("horizon") == horizon])
    return out


def _values(rows: list[dict[str, Any]], key: str) -> list[float]:
    values = []
    for row in rows:
        value = row.get(key)
        if value is None:
            continue
        try:
            f = float(value)
        except (TypeError, ValueError):
            continue
        if np.isfinite(f):
            values.append(f)
    return values


def _mean(rows: list[dict[str, Any]], key: str) -> float | None:
    values = _values(rows, key)
    return float(np.mean(values)) if values else None


def _quantile(rows: list[dict[str, Any]], key: str, q: float) -> float | None:
    values = _values(rows, key)
    return float(np.quantile(values, q)) if values else None


def _bool_rate(rows: list[dict[str, Any]], key: str) -> float | None:
    values = [bool(row.get(key)) for row in rows if row.get(key) is not None]
    return float(sum(values) / len(values)) if values else None


def _coverage(rows: list[dict[str, Any]], actual: str, low: str, high: str) -> float | None:
    values = []
    for row in rows:
        a, lo, hi = row.get(actual), row.get(low), row.get(high)
        if a is not None and lo is not None and hi is not None:
            values.append(float(lo) <= float(a) <= float(hi))
    return float(sum(values) / len(values)) if values else None


def _brier(rows: list[dict[str, Any]], prob_key: str, actual_key: str) -> float | None:
    errors = []
    for row in rows:
        prob, actual = row.get(prob_key), row.get(actual_key)
        if prob is not None and actual is not None:
            errors.append((float(prob) - (1.0 if actual else 0.0)) ** 2)
    return float(np.mean(errors)) if errors else None


def _mae(rows: list[dict[str, Any]], pred: str, actual: str) -> float | None:
    errors = [abs(float(row[pred]) - float(row[actual])) for row in rows if row.get(pred) is not None and row.get(actual) is not None]
    return float(np.mean(errors)) if errors else None


def _rmse(rows: list[dict[str, Any]], pred: str, actual: str) -> float | None:
    errors = [(float(row[pred]) - float(row[actual])) ** 2 for row in rows if row.get(pred) is not None and row.get(actual) is not None]
    return float(np.sqrt(np.mean(errors))) if errors else None


def _coverage_rate(rows: list[dict[str, Any]]) -> float | None:
    if not rows:
        return None
    ok = [row.get("terminal_return_p50") is not None and row.get("actual_terminal_return") is not None for row in rows]
    return float(sum(ok) / len(ok))
