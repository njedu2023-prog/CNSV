import pandas as pd

from cnsv.features.feature_quality import check_feature_quality


def _features(value):
    return {
        "price_volume": {"latest_close": 10, "latest_amount": 1000, "ret_1d": 0.01},
        "minute_structure": {"latest_intraday_close": 10, "intraday_range_pct": 0.02},
        "moneyflow": {"net_mf_amount": 10, "main_force_net": 5, "flow_strength_score": value},
        "trend": {"trend_state": "uptrend"},
        "volatility": {"volatility_state": "normal_vol"},
    }


def _bundle():
    dates = [f"2026-06-{day:02d}" for day in range(1, 61)]
    return {
        "daily": pd.DataFrame({"trade_date": dates, "close": range(60)}),
        "one_min": pd.DataFrame({"trade_date": ["2026-06-30"] * 60, "close": range(60)}),
        "moneyflow": pd.DataFrame({"trade_date": [f"2026-06-{day:02d}" for day in range(21, 31)], "net_mf_amount": range(10)}),
    }


def test_feature_quality_detects_inf():
    quality = check_feature_quality(_features(float("inf")), _bundle(), {"can_use_moneyflow_as_strong_factor": True})
    assert quality["status"] == "FAIL"
    assert any(check["status"] == "FAIL" and "infinite" in check["detail"] for check in quality["checks"])


def test_feature_quality_passes_clean_features():
    quality = check_feature_quality(_features(10), _bundle(), {"can_use_moneyflow_as_strong_factor": True})
    assert quality["failed_count"] == 0
