import pandas as pd

from cnsv.models.baseline_runner import run_baseline_models


def test_baseline_runner_returns_all_models_with_non_gating_fallback():
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
    assert result["status"] == "PASS"
    assert result["baseline_quality"]["fallback_count"] == 3
    assert result["baseline_quality"]["gating_warning_count"] == 0
    assert result["models"]["B2_state_grouped_distribution"]["horizons"]["5D"]["fallback_used"] is True


def test_baseline_runner_builds_historical_state_sample_for_b2():
    rows = 360
    daily = pd.DataFrame(
        {
            "trade_date": list(range(rows)),
            "close": [10 + i * 0.03 for i in range(rows)],
            "high": [10.2 + i * 0.03 for i in range(rows)],
            "low": [9.8 + i * 0.03 for i in range(rows)],
            "amount": [100000 + i for i in range(rows)],
        }
    )
    moneyflow = pd.DataFrame(
        {
            "trade_date": daily["trade_date"],
            "net_mf_amount": [1000.0] * rows,
            "buy_lg_amount": [800.0] * rows,
            "sell_lg_amount": [100.0] * rows,
            "buy_elg_amount": [600.0] * rows,
            "sell_elg_amount": [100.0] * rows,
        }
    )
    bundle = {"daily": daily, "moneyflow": moneyflow, "data_manifest": {"latest_trade_date": "2025-01-24"}}
    features = {
        "price_volume": {"latest_close": float(daily["close"].iloc[-1])},
        "trend": {"trend_state": "strong_uptrend"},
        "volatility": {"volatility_state": "low_vol", "realized_vol_20d": 0.2},
        "moneyflow": {"flow_strength_basic": "positive"},
    }
    result = run_baseline_models(bundle, features)
    b2 = result["models"]["B2_state_grouped_distribution"]
    assert b2["state_coverage"]["has_state_columns"] is True
    assert b2["state_coverage"]["usable_state_rows"] > 30
    assert b2["horizons"]["5D"]["fallback_used"] is False
