from __future__ import annotations

import pandas as pd

from cnsv.path.path_distribution import run_path_distribution_from_features
from cnsv.path.path_evaluator import contains_forbidden_path_key, evaluate_path_quality


def _daily(rows: int = 80) -> pd.DataFrame:
    close = [10 + i * 0.05 for i in range(rows)]
    return pd.DataFrame(
        {
            "trade_date": [f"202601{i + 1:02d}" for i in range(rows)],
            "close": close,
            "high": [x * 1.01 for x in close],
            "low": [x * 0.99 for x in close],
        }
    )


def _features() -> dict:
    return {
        "price_volume": {"latest_close": 14.0},
        "trend": {"trend_state": "uptrend"},
        "volatility": {"volatility_state": "normal_vol", "realized_vol_20d": 0.2},
        "moneyflow": {"flow_strength_basic": "positive"},
    }


def test_path_quality_fails_for_forbidden_trade_fields() -> None:
    assert contains_forbidden_path_key({"buy_signal": True})
    quality = evaluate_path_quality({"buy_signal": True}, 10.0)
    assert quality["status"] == "FAIL"


def test_path_quality_does_not_fail_transparent_p2_fallback() -> None:
    payload = run_path_distribution_from_features({"daily": _daily(), "data_manifest": {}}, {"status": "PASS"}, _features())
    assert payload["path_quality"]["status"] in {"PASS", "WARN"}
