from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from cnsv.models.baseline_b0_random_walk import run_b0_random_walk
from cnsv.models.baseline_b1_historical_distribution import run_b1_historical_distribution
from cnsv.models.baseline_b2_state_grouped_distribution import run_b2_state_grouped_distribution
from cnsv.models.baseline_b3_volatility_adjusted import run_b3_volatility_adjusted
from cnsv.models.baseline_evaluator import evaluate_baseline_models
from cnsv.models.baseline_schema import HORIZONS, clean_payload, latest_close, sorted_daily


def run_baseline_models(data_bundle: dict[str, Any], features: dict[str, Any], horizons: tuple[int, ...] = HORIZONS) -> dict[str, Any]:
    daily = data_bundle.get("daily")
    daily_df = sorted_daily(daily if isinstance(daily, pd.DataFrame) else pd.DataFrame())
    current_close = latest_close(daily_df, features)
    manifest = data_bundle.get("data_manifest") or {}
    models = {
        "B0_random_walk": run_b0_random_walk(daily_df, current_close, horizons),
        "B1_historical_distribution": run_b1_historical_distribution(daily_df, current_close, horizons),
        "B2_state_grouped_distribution": run_b2_state_grouped_distribution(daily_df, current_close, features, horizons),
        "B3_volatility_adjusted": run_b3_volatility_adjusted(daily_df, current_close, features, horizons),
    }
    quality = evaluate_baseline_models(models, horizons)
    warnings = list(quality.get("warnings", []))
    for model in models.values():
        warnings.extend(model.get("warnings", []))
    return clean_payload(
        {
            "status": quality["status"],
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "latest_trade_date": manifest.get("latest_trade_date", ""),
            "current_close": current_close,
            "horizons": list(horizons),
            "models": models,
            "baseline_quality": quality,
            "warnings": sorted(set(warnings)),
            "failed_count": quality["failed_count"],
            "warn_count": quality["warn_count"],
        }
    )

