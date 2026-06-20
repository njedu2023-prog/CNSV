import pandas as pd

from cnsv.validation.walk_forward import run_walk_forward_validation


def _bundle(rows: int = 340):
    dates = pd.date_range("2025-01-01", periods=rows, freq="B").strftime("%Y%m%d").tolist()
    daily = pd.DataFrame(
        {
            "trade_date": dates,
            "open": [20 + i * 0.01 for i in range(rows)],
            "high": [20.5 + i * 0.01 for i in range(rows)],
            "low": [19.5 + i * 0.01 for i in range(rows)],
            "close": [20 + i * 0.01 for i in range(rows)],
            "amount": [1000 + i for i in range(rows)],
            "vol": [100 + i for i in range(rows)],
        }
    )
    one_min = pd.DataFrame(
        {
            "trade_date": [dates[-1]] * 80,
            "time": range(80),
            "open": range(80),
            "high": [value + 1 for value in range(80)],
            "low": [value - 1 for value in range(80)],
            "close": range(1, 81),
            "amount": [100] * 80,
            "vol": [10] * 80,
        }
    )
    moneyflow = pd.DataFrame(
        {
            "trade_date": dates,
            "buy_lg_amount": [30] * rows,
            "sell_lg_amount": [10] * rows,
            "buy_elg_amount": [40] * rows,
            "sell_elg_amount": [20] * rows,
            "net_mf_amount": [100] * rows,
        }
    )
    return {
        "daily": daily,
        "one_min": one_min,
        "moneyflow": moneyflow,
        "gate": {"status": "PASS", "ready": True, "can_continue": True, "can_use_moneyflow_as_strong_factor": True},
        "data_manifest": {"latest_trade_date": dates[-1], "files": []},
    }


def test_walk_forward_uses_training_data_not_after_as_of_date():
    result = run_walk_forward_validation(_bundle(), _bundle()["gate"], min_history=260, validation_step=20)
    assert result["rows"]
    assert all(check["status"] == "PASS" for check in result["leakage_checks"])
    assert all(row["max_training_date"] <= row["as_of_date"] for row in result["rows"])
