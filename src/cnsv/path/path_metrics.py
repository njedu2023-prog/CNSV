from __future__ import annotations

from typing import Any

import numpy as np

from cnsv.path.path_replay import max_drawdown


def summarize_path_samples(
    samples: list[dict[str, Any]],
    latest_close: float,
    horizon: int,
    model_id: str,
    fallback_used: bool = False,
    fallback_reason: str = "",
    source_model: str = "",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    metrics: dict[str, Any] = {
        "model_id": model_id,
        "horizon": horizon,
        "sample_size": len(samples),
        "path_count": len(samples),
        "latest_close": latest_close,
        "fallback_used": fallback_used,
        "fallback_reason": fallback_reason,
        "source_model": source_model,
    }
    if extra:
        metrics.update(extra)
    if not samples:
        return metrics
    terminal = np.array([s["close_return_path"][-1] for s in samples], dtype=float)
    max_up = np.array([max(s["high_return_path"]) for s in samples], dtype=float)
    max_down = np.array([min(s["low_return_path"]) for s in samples], dtype=float)
    drawdown = np.array([max_drawdown(s["close_return_path"]) for s in samples], dtype=float)
    path_vol = np.array([np.std(s["close_return_path"], ddof=0) for s in samples], dtype=float)
    metrics.update(_q("terminal_return", terminal))
    metrics.update(_q("terminal_price", latest_close * (1.0 + terminal)))
    metrics.update(_q("max_up_return", max_up))
    metrics.update(_q("max_up_price", latest_close * (1.0 + max_up)))
    metrics.update(_q("max_down_return", max_down))
    metrics.update(_q("max_down_price", latest_close * (1.0 + max_down)))
    metrics.update(_q("max_drawdown", drawdown))
    metrics["path_volatility_p50"] = _quantile(path_vol, 0.50)
    metrics["path_volatility_p90"] = _quantile(path_vol, 0.90)
    metrics["positive_terminal_prob"] = _prob(terminal > 0)
    for pct in (0.03, 0.05, 0.08):
        label = int(pct * 100)
        metrics[f"touch_up_{label}pct_prob"] = _prob(max_up >= pct)
        metrics[f"touch_down_{label}pct_prob"] = _prob(max_down <= -pct)
    metrics["end_above_start_prob"] = metrics["positive_terminal_prob"]
    metrics["intraperiod_any_up_prob"] = _prob(max_up > 0)
    metrics["intraperiod_any_down_prob"] = _prob(max_down < 0)
    return metrics


def actual_path_outcome(close_path: list[float], high_path: list[float], low_path: list[float], base_close: float) -> dict[str, Any]:
    close_ret = np.array(close_path, dtype=float) / base_close - 1.0
    high_ret = np.array(high_path, dtype=float) / base_close - 1.0
    low_ret = np.array(low_path, dtype=float) / base_close - 1.0
    terminal = float(close_ret[-1])
    max_up = float(high_ret.max())
    max_down = float(low_ret.min())
    drawdown = max_drawdown(close_ret.tolist())
    return {
        "actual_terminal_return": terminal,
        "actual_max_up_return": max_up,
        "actual_max_down_return": max_down,
        "actual_max_drawdown": drawdown,
        "actual_positive_terminal": terminal > 0,
        "actual_touch_up_3pct": max_up >= 0.03,
        "actual_touch_up_5pct": max_up >= 0.05,
        "actual_touch_down_3pct": max_down <= -0.03,
        "actual_touch_down_5pct": max_down <= -0.05,
    }


def summarize_validation_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"sample_size": 0}
    return {
        "sample_size": len(rows),
        "terminal_p10_p90_coverage": _mean_bool(_covered(rows, "actual_terminal_return", "terminal_return_p10", "terminal_return_p90")),
        "max_up_p10_p90_coverage": _mean_bool(_covered(rows, "actual_max_up_return", "max_up_return_p10", "max_up_return_p90")),
        "max_down_p10_p90_coverage": _mean_bool(_covered(rows, "actual_max_down_return", "max_down_return_p10", "max_down_return_p90")),
        "drawdown_p10_p90_coverage": _mean_bool(_covered(rows, "actual_max_drawdown", "max_drawdown_p10", "max_drawdown_p90")),
        "touch_up_3pct_brier": _brier(rows, "touch_up_3pct_prob", "actual_touch_up_3pct"),
        "touch_up_5pct_brier": _brier(rows, "touch_up_5pct_prob", "actual_touch_up_5pct"),
        "touch_down_3pct_brier": _brier(rows, "touch_down_3pct_prob", "actual_touch_down_3pct"),
        "touch_down_5pct_brier": _brier(rows, "touch_down_5pct_prob", "actual_touch_down_5pct"),
        "positive_terminal_brier": _brier(rows, "positive_terminal_prob", "actual_positive_terminal"),
        "path_interval_coverage": _mean_bool(_covered(rows, "actual_terminal_return", "max_down_return_p10", "max_up_return_p90")),
        "path_mae_terminal": _mae(rows, "terminal_return_p50", "actual_terminal_return"),
        "path_rmse_terminal": _rmse(rows, "terminal_return_p50", "actual_terminal_return"),
        "fallback_rate": _mean_bool([bool(row.get("fallback_used")) for row in rows]),
    }


def _q(prefix: str, values: np.ndarray) -> dict[str, float | None]:
    return {f"{prefix}_p10": _quantile(values, 0.10), f"{prefix}_p50": _quantile(values, 0.50), f"{prefix}_p90": _quantile(values, 0.90)}


def _quantile(values: np.ndarray, q: float) -> float | None:
    clean = values[np.isfinite(values)]
    if clean.size == 0:
        return None
    return float(np.quantile(clean, q))


def _prob(mask: np.ndarray) -> float | None:
    return float(np.mean(mask)) if mask.size else None


def _covered(rows: list[dict[str, Any]], actual: str, low: str, high: str) -> list[bool]:
    out: list[bool] = []
    for row in rows:
        a, lo, hi = row.get(actual), row.get(low), row.get(high)
        if a is not None and lo is not None and hi is not None:
            out.append(float(lo) <= float(a) <= float(hi))
    return out


def _mean_bool(values: list[bool]) -> float | None:
    return float(sum(values) / len(values)) if values else None


def _brier(rows: list[dict[str, Any]], prob_key: str, actual_key: str) -> float | None:
    errors = [(float(row[prob_key]) - (1.0 if row[actual_key] else 0.0)) ** 2 for row in rows if row.get(prob_key) is not None and row.get(actual_key) is not None]
    return float(np.mean(errors)) if errors else None


def _mae(rows: list[dict[str, Any]], pred_key: str, actual_key: str) -> float | None:
    errors = [abs(float(row[pred_key]) - float(row[actual_key])) for row in rows if row.get(pred_key) is not None and row.get(actual_key) is not None]
    return float(np.mean(errors)) if errors else None


def _rmse(rows: list[dict[str, Any]], pred_key: str, actual_key: str) -> float | None:
    errors = [(float(row[pred_key]) - float(row[actual_key])) ** 2 for row in rows if row.get(pred_key) is not None and row.get(actual_key) is not None]
    return float(np.sqrt(np.mean(errors))) if errors else None
