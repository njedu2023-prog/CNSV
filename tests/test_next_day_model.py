import numpy as np
import pandas as pd

import cnsv.trading.next_day_model as model


def _history(rows: int = 260) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(42)
    dates = pd.bdate_range("2024-01-02", periods=rows)
    returns = np.where(np.arange(rows) % 3 == 0, 0.012, -0.006) + rng.normal(0, 0.006, rows)
    close = 30.0 * np.cumprod(1.0 + returns)
    pre_close = np.r_[close[0] / (1.0 + returns[0]), close[:-1]]
    open_price = pre_close * (1.0 + rng.normal(0, 0.003, rows))
    high = np.maximum(open_price, close) * (1.0 + rng.uniform(0.001, 0.012, rows))
    low = np.minimum(open_price, close) * (1.0 - rng.uniform(0.001, 0.012, rows))
    amount = rng.uniform(1_000_000, 5_000_000, rows)
    daily = pd.DataFrame(
        {
            "trade_date": dates.strftime("%Y-%m-%d"),
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "pre_close": pre_close,
            "pct_chg": returns * 100.0,
            "vol": rng.uniform(100_000, 900_000, rows),
            "amount": amount,
        }
    )
    net = np.sign(returns) * amount * 0.02
    moneyflow = pd.DataFrame(
        {
            "trade_date": dates.strftime("%Y-%m-%d"),
            "buy_lg_amount": amount * 0.07 + net,
            "sell_lg_amount": amount * 0.07,
            "buy_elg_amount": amount * 0.03 + net / 2.0,
            "sell_elg_amount": amount * 0.03,
            "net_mf_amount": net,
        }
    )
    return daily, moneyflow


def test_feature_target_is_the_next_trade_day_without_lookahead():
    daily, moneyflow = _history(100)
    frame = model.build_feature_frame(daily, moneyflow)
    source = daily.set_index("trade_date")
    row = frame.iloc[5]
    source_position = source.index.get_loc(row["trade_date"])
    expected = source.iloc[source_position + 1]["pct_chg"] / 100.0

    assert row["target_return"] == expected
    assert row["target"] == (1.0 if expected > 0 else 0.0)
    assert frame.iloc[-1]["trade_date"] == daily.iloc[-1]["trade_date"]
    assert pd.isna(frame.iloc[-1]["target"])


def test_next_day_model_returns_binary_prediction_and_walk_forward_metrics(monkeypatch):
    daily, moneyflow = _history()
    monkeypatch.setattr(model, "MIN_TRAIN_ROWS", 120)
    monkeypatch.setattr(model, "VALIDATION_MAX_ROWS", 80)
    monkeypatch.setattr(model, "REFIT_INTERVAL_DAYS", 20)
    monkeypatch.setattr(
        model,
        "MODEL_SPECS",
        (model.ModelSpec(25, 0.05, 7, 2, 20, 2.0),),
    )

    output = model.fit_next_day_model(
        {"daily_price_history": daily, "moneyflow_history": moneyflow}
    )

    assert output["model_ready"] is True
    assert output["predicted_direction"] in {"UP", "DOWN"}
    assert output["prob_up_1d"] + output["prob_down_1d"] == 1.0
    assert output["prob_flat_1d"] == 0.0
    assert output["training"]["end_date"] == daily.iloc[-2]["trade_date"]
    assert output["latest_data_trade_date"] == daily.iloc[-1]["trade_date"]
    assert 75 <= output["validation"]["sample_size"] <= 80
    assert output["validation"]["leakage_guard"].startswith("every validation prediction")
    assert "scaled_to_1D" not in output["model_return_distribution"]["distribution_source"]
