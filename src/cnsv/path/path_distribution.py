from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from cnsv.features.feature_bundle import build_feature_bundle
from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS, HORIZONS, clean_number, clean_payload, current_state, daily_log_return_std, latest_close, sorted_daily
from cnsv.models.baseline_state_history import build_historical_state_daily, state_coverage
from cnsv.path import PATH_MODEL_IDS
from cnsv.path.path_evaluator import evaluate_path_quality
from cnsv.path.path_metrics import summarize_path_samples
from cnsv.path.path_replay import build_path_samples

STAGE = "V1.3_path_distribution"
VERSION = "1.3"
P2_MIN_SAMPLE_SIZE = 30


def run_path_distribution(data_bundle: dict[str, Any], gate: dict[str, Any], horizons: tuple[int, ...] = HORIZONS) -> dict[str, Any]:
    features = build_feature_bundle(data_bundle, gate)
    return run_path_distribution_from_features(data_bundle, gate, features, horizons)


def run_path_distribution_from_features(
    data_bundle: dict[str, Any],
    gate: dict[str, Any],
    features: dict[str, Any],
    horizons: tuple[int, ...] = HORIZONS,
) -> dict[str, Any]:
    daily = sorted_daily(data_bundle.get("daily") if isinstance(data_bundle.get("daily"), pd.DataFrame) else pd.DataFrame())
    moneyflow = data_bundle.get("moneyflow")
    moneyflow_df = moneyflow if isinstance(moneyflow, pd.DataFrame) else pd.DataFrame()
    state_daily = build_historical_state_daily(daily, moneyflow_df)
    close = latest_close(daily, features)
    manifest = data_bundle.get("data_manifest") or {}
    state = current_state(features)
    models = _build_models(daily, state_daily, close, features, state, horizons)
    quality = evaluate_path_quality(models, close, horizons)
    stage_gate = _stage_gate(gate)
    payload = {
        "meta": {
            "system": "CNSV",
            "version": VERSION,
            "stage": STAGE,
            "report_type": "path_distribution_report",
            "ts_code": "600150.SH",
            "name": "中国船舶",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "latest_trade_date": manifest.get("latest_trade_date", ""),
            "is_trade_signal": False,
        },
        "cnsvdata_gate": stage_gate,
        "path_quality": quality,
        "current_state": state,
        "state_coverage": state_coverage(state_daily),
        "path_models": models,
        "path_registry": build_path_registry(),
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "next_stage": "V1.4 observation backtest after path validation acceptance",
    }
    return clean_payload(payload)


def _stage_gate(gate: dict[str, Any]) -> dict[str, Any]:
    """Expose V1.3 permissions without opening the V1.4 backtest stage early."""
    stage_gate = dict(gate)
    stage_gate["can_run_backtest"] = False
    stage_gate["backtest_permission_stage"] = "V1.4"
    stage_gate["stage_permission_note"] = "V1.3 only supports path distribution and path validation; observation backtest opens in V1.4."
    return stage_gate


def _build_models(
    daily: pd.DataFrame,
    state_daily: pd.DataFrame,
    close: float | None,
    features: dict[str, Any],
    state: dict[str, Any],
    horizons: tuple[int, ...],
) -> dict[str, Any]:
    latest = clean_number(close) or 0.0
    p0 = {"model_id": "P0_historical_path_replay", "model_name": "历史路径回放", "is_trade_signal": False, "horizons": {}}
    p1 = {"model_id": "P1_volatility_adjusted_path", "model_name": "波动率调整路径回放", "is_trade_signal": False, "warnings": [], "horizons": {}}
    p2 = {"model_id": "P2_state_conditional_path", "model_name": "状态条件路径回放", "is_trade_signal": False, "role": "辅助状态层，不作为核心依赖", "horizons": {}}
    scale, scale_warnings = volatility_scale(daily, features)
    p1["volatility_scale"] = scale
    p1["warnings"] = scale_warnings
    for horizon in horizons:
        key = f"{horizon}D"
        p0_samples, p0_meta = build_path_samples(daily, horizon, latest, include_price_paths=False)
        p0["horizons"][key] = summarize_path_samples(p0_samples, latest, horizon, "P0_historical_path_replay", extra=p0_meta)
        p1_samples, p1_meta = build_path_samples(daily, horizon, latest, volatility_scale=scale, include_price_paths=False)
        p1["horizons"][key] = summarize_path_samples(
            p1_samples,
            latest,
            horizon,
            "P1_volatility_adjusted_path",
            source_model="P0_historical_path_replay",
            extra={**p1_meta, "volatility_scale": scale, "volatility_scale_warnings": scale_warnings},
        )
        state_samples, state_meta = build_path_samples(daily, horizon, latest, state_daily=state_daily, state_key=state, include_price_paths=False)
        if len(state_samples) < P2_MIN_SAMPLE_SIZE:
            p2["horizons"][key] = {
                **p1["horizons"][key],
                "model_id": "P2_state_conditional_path",
                "fallback_used": True,
                "fallback_reason": f"state_path_sample_size_lt_{P2_MIN_SAMPLE_SIZE}",
                "source_model": "P1_volatility_adjusted_path",
                "state_key": state,
                "state_sample_size": len(state_samples),
                "fallback_gating": False,
            }
        else:
            p2["horizons"][key] = summarize_path_samples(
                state_samples,
                latest,
                horizon,
                "P2_state_conditional_path",
                source_model="state_matched_history",
                extra={**state_meta, "state_key": state, "state_sample_size": len(state_samples), "fallback_gating": False},
            )
    return {model["model_id"]: model for model in (p0, p1, p2)}


def volatility_scale(daily: pd.DataFrame, features: dict[str, Any]) -> tuple[float, list[str]]:
    warnings: list[str] = []
    realized = clean_number((features.get("volatility", {}) or {}).get("realized_vol_20d"))
    long_term_daily = daily_log_return_std(daily)
    long_term = long_term_daily * (252**0.5) if long_term_daily is not None else None
    if realized is None or long_term in (None, 0):
        return 1.0, ["volatility_scale_defaulted"]
    raw = realized / long_term
    clipped = max(0.5, min(1.8, raw))
    if clipped != raw:
        warnings.append(f"volatility_scale_clipped:{raw:.4f}->{clipped:.4f}")
    return clipped, warnings


def build_path_registry() -> list[dict[str, Any]]:
    return [
        {
            "model_id": "P0_historical_path_replay",
            "model_name": "历史路径回放",
            "stage": STAGE,
            "is_trade_signal": False,
            "horizons": list(HORIZONS),
            "input_data": ["daily.close", "daily.high", "daily.low"],
            "output_fields": ["terminal_return_p10", "terminal_return_p50", "terminal_return_p90", "max_up_return_p90", "max_down_return_p10", "touch_up_5pct_prob", "touch_down_5pct_prob"],
        },
        {
            "model_id": "P1_volatility_adjusted_path",
            "model_name": "波动率调整路径回放",
            "stage": STAGE,
            "is_trade_signal": False,
            "horizons": list(HORIZONS),
            "input_data": ["daily.close", "daily.high", "daily.low", "realized_vol_20d"],
        },
        {
            "model_id": "P2_state_conditional_path",
            "model_name": "状态条件路径回放",
            "stage": STAGE,
            "is_trade_signal": False,
            "horizons": list(HORIZONS),
            "input_data": ["trend_state", "volatility_state", "flow_strength_basic"],
            "role": "辅助状态层，不作为核心依赖",
        },
    ]
