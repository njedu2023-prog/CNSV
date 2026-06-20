import pandas as pd

from cnsv.models.baseline_b0_random_walk import run_b0_random_walk


def _daily(rows=90):
    return pd.DataFrame({"trade_date": range(rows), "close": [20 + i * 0.1 for i in range(rows)]})


def test_b0_outputs_all_horizons_and_keeps_median_price_near_close():
    result = run_b0_random_walk(_daily(), 28.9)
    assert set(result["horizons"]) == {"5D", "10D", "20D"}
    for row in result["horizons"].values():
        assert row["expected_return"] == 0
        assert row["p50_price"] == 28.9
        assert row["p10_price"] > 0
        assert row["p90_price"] > 0
