import pandas as pd

from cnsv.models.baseline_b2_state_grouped_distribution import run_b2_state_grouped_distribution


def _daily(rows=90):
    return pd.DataFrame({"trade_date": range(rows), "close": [20 + i * 0.1 for i in range(rows)]})


def _features():
    return {
        "price_volume": {"latest_close": 28.9},
        "trend": {"trend_state": "uptrend"},
        "volatility": {"volatility_state": "normal_vol", "realized_vol_20d": 0.2},
        "moneyflow": {"flow_strength_basic": "positive"},
    }


def test_b2_marks_fallback_for_small_state_sample():
    result = run_b2_state_grouped_distribution(_daily(), 28.9, _features())
    assert set(result["horizons"]) == {"5D", "10D", "20D"}
    for row in result["horizons"].values():
        assert row["fallback_used"] is True
        assert row["fallback_reason"] == "missing_historical_state_columns"
        assert row["p10_price"] > 0


def test_b2_uses_state_group_when_historical_state_sample_is_available():
    daily = _daily(120)
    daily["trend_state"] = "uptrend"
    daily["volatility_state"] = "normal_vol"
    daily["flow_strength_basic"] = "positive"
    result = run_b2_state_grouped_distribution(daily, 31.9, _features())
    assert result["state_coverage"]["usable_state_rows"] == 120
    for row in result["horizons"].values():
        assert row["fallback_used"] is False
        assert row["fallback_reason"] == ""
        assert row["state_sample_size"] >= 100
        assert row["p10_price"] > 0
