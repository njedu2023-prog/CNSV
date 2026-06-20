import pandas as pd

from cnsv.models.baseline_b1_historical_distribution import run_b1_historical_distribution


def _daily(rows=90):
    return pd.DataFrame({"trade_date": range(rows), "close": [20 + i * 0.1 for i in range(rows)]})


def test_b1_outputs_empirical_distribution_for_all_horizons():
    result = run_b1_historical_distribution(_daily(), 28.9)
    assert set(result["horizons"]) == {"5D", "10D", "20D"}
    for row in result["horizons"].values():
        assert row["sample_size"] > 30
        assert row["p05_return"] <= row["p10_return"] <= row["p25_return"] <= row["p50_return"] <= row["p75_return"] <= row["p90_return"] <= row["p95_return"]
        assert row["p10_price"] > 0
        assert row["p50_price"] > 0
        assert row["p90_price"] > 0
