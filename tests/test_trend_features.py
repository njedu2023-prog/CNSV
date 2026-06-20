import pandas as pd

from cnsv.features.price_volume_features import build_price_volume_features
from cnsv.features.trend_features import build_trend_features


def test_trend_state_detects_uptrend():
    daily = pd.DataFrame(
        {
            "trade_date": [f"2026-04-{day:02d}" for day in range(1, 61)],
            "open": range(1, 61),
            "high": range(2, 62),
            "low": range(0, 60),
            "close": range(1, 61),
            "amount": [1000] * 60,
            "vol": [100] * 60,
        }
    )
    price = build_price_volume_features(daily)
    trend = build_trend_features(price, daily)
    assert trend["trend_state"] == "strong_uptrend"
    assert trend["close_above_ma20"] is True
