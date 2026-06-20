from __future__ import annotations

import math
from typing import Any

import pandas as pd

from cnsv.features.feature_bundle import build_feature_bundle
from cnsv.models.baseline_runner import run_baseline_models
from cnsv.models.baseline_schema import HORIZONS, sorted_daily
from cnsv.validation.leakage_checks import check_training_window

MODEL_IDS = ("B0_random_walk", "B1_historical_distribution", "B2_state_grouped_distribution", "B3_volatility_adjusted")


def run_walk_forward_validation(
    data_bundle: dict[str, Any],
    gate: dict[str, Any],
    horizons: tuple[int, ...] = HORIZONS,
    min_history: int = 260,
    validation_step: int = 5,
) -> dict[str, Any]:
    daily = sorted_daily(data_bundle.get("daily") if isinstance(data_bundle.get("daily"), pd.DataFrame) else pd.DataFrame())
    if daily.empty or "close" not in daily.columns:
        return {"rows": [], "leakage_checks": [], "skipped_reason": "missing_daily_close"}
    rows: list[dict[str, Any]] = []
    leakage_checks: list[dict[str, Any]] = []
    close = pd.to_numeric(daily["close"], errors="coerce")
    trade_dates = daily["trade_date"].astype(str).tolist() if "trade_date" in daily.columns else [str(i) for i in daily.index]
    max_horizon = max(horizons)
    last_start = len(daily) - max_horizon - 1
    for idx in range(min_history, max(min_history, last_start + 1), max(1, validation_step)):
        as_of_date = trade_dates[idx]
        train_bundle = _slice_bundle_as_of(data_bundle, as_of_date)
        training_frames = [frame for frame in train_bundle.values() if isinstance(frame, pd.DataFrame)]
        leakage_checks.append(check_training_window(as_of_date, training_frames))
        features = build_feature_bundle(train_bundle, gate)
        prediction = run_baseline_models(train_bundle, features, horizons)
        for horizon in horizons:
            future_idx = idx + horizon
            if future_idx >= len(daily):
                continue
            current_close = close.iloc[idx]
            future_close = close.iloc[future_idx]
            if pd.isna(current_close) or pd.isna(future_close) or current_close <= 0 or future_close <= 0:
                continue
            actual_return = math.log(float(future_close) / float(current_close))
            for model_id in MODEL_IDS:
                horizon_row = (prediction.get("models", {}).get(model_id, {}).get("horizons", {}) or {}).get(f"{horizon}D", {})
                rows.append(
                    {
                        "as_of_date": as_of_date,
                        "target_date": trade_dates[future_idx],
                        "horizon": f"{horizon}D",
                        "horizon_days": horizon,
                        "model_id": model_id,
                        "p10_return": horizon_row.get("p10_return"),
                        "p50_return": horizon_row.get("p50_return"),
                        "p90_return": horizon_row.get("p90_return"),
                        "positive_prob": horizon_row.get("positive_prob"),
                        "actual_return": actual_return,
                        "actual_positive": actual_return > 0,
                        "state_key": horizon_row.get("state_key"),
                        "state_sample_size": horizon_row.get("state_sample_size"),
                        "fallback_used": bool(horizon_row.get("fallback_used", False)),
                        "max_training_date": max(check.get("max_training_date", "") for check in leakage_checks[-1:]),
                    }
                )
    return {"rows": rows, "leakage_checks": leakage_checks, "skipped_reason": "", "validation_step": validation_step}


def purged_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for model_id in MODEL_IDS:
        for horizon in sorted({row["horizon_days"] for row in rows}):
            group = [row for row in rows if row["model_id"] == model_id and row["horizon_days"] == horizon]
            group = sorted(group, key=lambda row: row["as_of_date"])
            selected.extend(group[::horizon])
    return selected


def _slice_bundle_as_of(data_bundle: dict[str, Any], as_of_date: str) -> dict[str, Any]:
    sliced: dict[str, Any] = {}
    for key, value in data_bundle.items():
        if isinstance(value, pd.DataFrame):
            sliced[key] = _slice_frame_as_of(value, as_of_date)
        elif key == "data_manifest" and isinstance(value, dict):
            sliced[key] = {**value, "latest_trade_date": as_of_date}
        else:
            sliced[key] = value
    return sliced


def _slice_frame_as_of(frame: pd.DataFrame, as_of_date: str) -> pd.DataFrame:
    if frame.empty or "trade_date" not in frame.columns:
        return frame.copy()
    out = frame.loc[frame["trade_date"].astype(str) <= str(as_of_date)].copy()
    return out.sort_values("trade_date").reset_index(drop=True)
