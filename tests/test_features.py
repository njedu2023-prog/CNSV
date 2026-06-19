import pandas as pd

from cnsv.features.feature_bundle import build_feature_bundle
from cnsv.features.minute_structure_features import build_minute_structure_features
from cnsv.features.moneyflow_features import build_moneyflow_features
from cnsv.features.price_volume_features import build_price_volume_features


def test_daily_price_volume_features():
    df = pd.DataFrame(
        {
            "trade_date": [f"2026-06-{day:02d}" for day in range(1, 23)],
            "close": list(range(10, 32)),
            "vol": [100] * 21 + [200],
            "amount": [1000] * 21 + [3000],
        }
    )
    features = build_price_volume_features(df)
    assert features["latest_close"] == 31
    assert features["ma20"] is not None
    assert features["volume_ratio_5d"] == 2


def test_minute_structure_features():
    df = pd.DataFrame(
        {
            "trade_date": ["2026-06-19"] * 61,
            "time": list(range(61)),
            "close": list(range(100, 161)),
            "high": list(range(101, 162)),
            "low": list(range(99, 160)),
            "vol": [10] * 61,
            "amount": [100] * 61,
        }
    )
    features = build_minute_structure_features(df)
    assert features["latest_intraday_close"] == 160
    assert features["last_30min_return"] is not None


def test_moneyflow_strong_factor_disabled_degrades():
    df = pd.DataFrame({"trade_date": ["2026-06-19"], "net_mf_amount": [1000]})
    features = build_moneyflow_features(df, {"can_use_moneyflow_as_strong_factor": False}, "2026-06-19")
    assert features["can_use_as_strong_factor"] is False
    assert "low-confidence" in features["moneyflow_warning"]


def test_feature_bundle_builds():
    daily = pd.DataFrame({"trade_date": ["2026-06-18", "2026-06-19"], "close": [10, 11]})
    minute = pd.DataFrame({"trade_date": ["2026-06-19"], "close": [11]})
    moneyflow = pd.DataFrame({"trade_date": ["2026-06-19"], "net_mf_amount": [100]})
    bundle = {"daily": daily, "one_min": minute, "moneyflow": moneyflow, "data_manifest": {"latest_trade_date": "2026-06-19"}}
    features = build_feature_bundle(bundle, {"can_use_moneyflow_as_strong_factor": True})
    assert features["feature_status"] == "PASS"
