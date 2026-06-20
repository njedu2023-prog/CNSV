import pandas as pd

from cnsv.backtest.observation_backtest import run_observation_backtest
from cnsv.path.path_metrics import actual_path_outcome
from cnsv.path.path_validation import run_path_walk_forward_validation


def test_actual_path_outcome_has_v14_fields():
    out = actual_path_outcome([10.5, 10.8], [10.7, 11.0], [9.8, 10.0], 10.0)
    assert out["actual_terminal_return"] == 0.08000000000000007
    assert out["actual_touch_up_5pct"] is True
    assert out["actual_touch_down_5pct"] is False
    assert "actual_touch_up_8pct" in out
    assert "actual_path_volatility" in out


def test_observation_backtest_builds_rows_without_future_leakage():
    bundle = _bundle(340)
    report = run_observation_backtest(bundle, _gate(), min_history=260, validation_step=50)
    assert report["meta"]["version"] == "1.4"
    assert report["meta"]["is_trade_signal"] is False
    assert report["observation_backtest_leakage_checks"]["status"] == "PASS"
    assert report["backtest_scope"]["standard_sample_size"] > 0
    assert set(report["backtest_scope"]["models"]) == {"P0_historical_path_replay", "P1_volatility_adjusted_path", "P2_state_conditional_path"}


def test_walk_forward_row_dates_are_ordered():
    wf = run_path_walk_forward_validation(_bundle(330), _gate(), min_history=260, validation_step=50)
    row = wf["rows"][0]
    assert row["max_prediction_input_date"] <= row["as_of_date"]
    assert row["truth_start_date"] > row["as_of_date"]
    assert row["truth_end_date"] > row["as_of_date"]


def _bundle(n: int):
    dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y%m%d")
    close = [10 + i * 0.01 for i in range(n)]
    daily = pd.DataFrame({"trade_date": dates, "open": close, "high": [v * 1.01 for v in close], "low": [v * 0.99 for v in close], "close": close, "vol": 1000, "amount": 10000})
    moneyflow = pd.DataFrame({
        "trade_date": dates,
        "net_mf_amount": [(-1) ** i * 100 for i in range(n)],
        "buy_lg_amount": [100 + i for i in range(n)],
        "sell_lg_amount": [80 + i for i in range(n)],
        "buy_elg_amount": [50 + i for i in range(n)],
        "sell_elg_amount": [40 + i for i in range(n)],
    })
    return {"daily": daily, "moneyflow": moneyflow, "data_manifest": {"latest_trade_date": str(dates[-1])}}


def _gate():
    return {"ready": True, "status": "PASS", "can_generate_formal_signal": False}
