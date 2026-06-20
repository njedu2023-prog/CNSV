from __future__ import annotations

import pandas as pd

from cnsv.path.path_distribution import run_path_distribution_from_features, volatility_scale


def _daily(rows: int = 80) -> pd.DataFrame:
    close = [10 + i * 0.05 for i in range(rows)]
    return pd.DataFrame(
        {
            "trade_date": [f"2026-01-{(i % 28) + 1:02d}" for i in range(rows)],
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


def test_run_path_distribution_outputs_p0_p1_p2_all_horizons() -> None:
    payload = run_path_distribution_from_features({"daily": _daily(), "moneyflow": pd.DataFrame(), "data_manifest": {}}, {"status": "PASS"}, _features())
    assert payload["path_quality"]["status"] in {"PASS", "WARN"}
    assert set(payload["path_models"]) == {"P0_historical_path_replay", "P1_volatility_adjusted_path", "P2_state_conditional_path"}
    for model in payload["path_models"].values():
        assert set(model["horizons"]) == {"5D", "10D", "20D"}
    assert payload["meta"]["is_trade_signal"] is False


def test_p2_falls_back_when_state_sample_is_insufficient() -> None:
    payload = run_path_distribution_from_features({"daily": _daily(), "moneyflow": pd.DataFrame(), "data_manifest": {}}, {"status": "PASS"}, _features())
    row = payload["path_models"]["P2_state_conditional_path"]["horizons"]["5D"]
    assert row["fallback_used"] is True
    assert row["fallback_reason"]
    assert row["source_model"] == "P1_volatility_adjusted_path"


def test_volatility_scale_clipping_records_warning() -> None:
    scale, warnings = volatility_scale(_daily(), {"volatility": {"realized_vol_20d": 999}})
    assert scale == 1.8
    assert warnings
