import pandas as pd

from cnsv.models.baseline_runner import run_baseline_models


def test_baseline_runner_returns_all_models_with_warn_fallback():
    daily = pd.DataFrame({"trade_date": range(80), "close": [10 + i * 0.05 for i in range(80)]})
    bundle = {"daily": daily, "data_manifest": {"latest_trade_date": "2026-06-18"}}
    features = {
        "price_volume": {"latest_close": 13.95},
        "trend": {"trend_state": "uptrend"},
        "volatility": {"volatility_state": "normal_vol", "realized_vol_20d": 0.2},
        "moneyflow": {"flow_strength_basic": "mixed"},
    }
    result = run_baseline_models(bundle, features)
    assert set(result["models"]) == {
        "B0_random_walk",
        "B1_historical_distribution",
        "B2_state_grouped_distribution",
        "B3_volatility_adjusted",
    }
    assert result["status"] in {"PASS", "WARN"}
    assert result["models"]["B2_state_grouped_distribution"]["horizons"]["5D"]["fallback_used"] is True

