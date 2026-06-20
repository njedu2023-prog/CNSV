import pandas as pd

from cnsv.models.baseline_b0_random_walk import run_b0_random_walk
from cnsv.models.baseline_b1_historical_distribution import run_b1_historical_distribution
from cnsv.models.baseline_b2_state_grouped_distribution import run_b2_state_grouped_distribution
from cnsv.models.baseline_b3_volatility_adjusted import run_b3_volatility_adjusted


def _daily(rows=90):
    return pd.DataFrame(
        {
            "trade_date": [f"2026-03-{(i % 28) + 1:02d}" for i in range(rows)],
            "close": [20 + i * 0.1 for i in range(rows)],
            "high": [20.5 + i * 0.1 for i in range(rows)],
            "low": [19.5 + i * 0.1 for i in range(rows)],
            "amount": [1000 + i for i in range(rows)],
        }
    )


def _features():
    return {
        "price_volume": {"latest_close": 28.9},
        "trend": {"trend_state": "uptrend"},
        "volatility": {"volatility_state": "normal_vol", "realized_vol_20d": 0.2},
        "moneyflow": {"flow_strength_basic": "positive"},
    }


def test_b0_random_walk_p50_matches_current_close():
    result = run_b0_random_walk(_daily(), 28.9)
    row = result["horizons"]["5D"]
    assert row["p50_return"] == 0
    assert row["p50_price"] == 28.9
    assert row["p10_price"] > 0


def test_b1_historical_quantiles_are_ordered():
    result = run_b1_historical_distribution(_daily(), 28.9)
    row = result["horizons"]["20D"]
    assert row["sample_size"] > 30
    assert row["p05_return"] <= row["p10_return"] <= row["p50_return"] <= row["p90_return"] <= row["p95_return"]
    assert 0 <= row["positive_prob"] <= 1


def test_b2_falls_back_when_state_sample_is_too_small():
    result = run_b2_state_grouped_distribution(_daily(), 28.9, _features())
    row = result["horizons"]["10D"]
    assert row["fallback_used"] is True
    assert row["fallback_reason"] == "missing_historical_state_columns"
    assert row["p50_price"] > 0


def test_b3_volatility_adjusted_prices_are_positive():
    result = run_b3_volatility_adjusted(_daily(), 28.9, _features())
    row = result["horizons"]["5D"]
    assert 0.5 <= row["volatility_scale"] <= 2.0
    assert row["p10_price"] > 0
    assert row["p90_price"] > 0
