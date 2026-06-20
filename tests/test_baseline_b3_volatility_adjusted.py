import pandas as pd

from cnsv.models.baseline_b3_volatility_adjusted import run_b3_volatility_adjusted


def _daily(rows=90):
    return pd.DataFrame({"trade_date": range(rows), "close": [20 + i * 0.1 for i in range(rows)]})


def _features():
    return {
        "price_volume": {"latest_close": 28.9},
        "trend": {"trend_state": "uptrend"},
        "volatility": {"volatility_state": "normal_vol", "realized_vol_20d": 0.2},
        "moneyflow": {"flow_strength_basic": "positive"},
    }


def test_b3_clips_volatility_scale_and_outputs_positive_prices():
    result = run_b3_volatility_adjusted(_daily(), 28.9, _features())
    assert set(result["horizons"]) == {"5D", "10D", "20D"}
    for row in result["horizons"].values():
        assert 0.5 <= row["volatility_scale"] <= 2.0
        assert row["p10_price"] > 0
        assert row["p50_price"] > 0
        assert row["p90_price"] > 0
