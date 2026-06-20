import pandas as pd

from cnsv.features.volatility_features import build_volatility_features


def test_volatility_state_and_atr_are_available():
    daily = pd.DataFrame(
        {
            "trade_date": [f"2026-{month:02d}-{day:02d}" for month in range(1, 10) for day in range(1, 29)],
            "high": [100 + index * 0.2 + 1 for index in range(252)],
            "low": [100 + index * 0.2 - 1 for index in range(252)],
            "close": [100 + index * 0.2 for index in range(252)],
        }
    )
    features = build_volatility_features(daily)
    assert features["realized_vol_20d"] is not None
    assert features["atr_14d"] is not None
    assert features["volatility_state"] in {"high_vol", "low_vol", "normal_vol", "unknown"}
