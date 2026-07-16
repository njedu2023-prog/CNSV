import numpy as np
import pandas as pd

import cnsv.trading.intraday_next_day_model as model
import cnsv.trading.probability as probability


def _histories(days: int = 170):
    rng = np.random.default_rng(17)
    dates = pd.bdate_range("2026-01-05", periods=days)
    returns = rng.normal(0.0008, 0.018, days)
    closes = 32.0 * np.cumprod(1.0 + returns)
    pre_close = np.r_[32.0, closes[:-1]]
    opens = pre_close * (1.0 + rng.normal(0.0, 0.004, days))
    highs = np.maximum(opens, closes) * 1.01
    lows = np.minimum(opens, closes) * 0.99
    volumes = rng.uniform(700_000, 1_600_000, days)
    daily = pd.DataFrame({
        "trade_date": dates.strftime("%Y-%m-%d"),
        "open": opens,
        "high": highs,
        "low": lows,
        "close": closes,
        "pre_close": pre_close,
        "pct_chg": (closes / pre_close - 1.0) * 100.0,
        "vol": volumes,
        "amount": volumes * closes,
    })
    moneyflow = pd.DataFrame({
        "trade_date": dates.strftime("%Y-%m-%d"),
        "buy_lg_amount": rng.uniform(20_000, 80_000, days),
        "sell_lg_amount": rng.uniform(20_000, 80_000, days),
        "buy_elg_amount": rng.uniform(10_000, 50_000, days),
        "sell_elg_amount": rng.uniform(10_000, 50_000, days),
        "net_mf_amount": rng.normal(0, 30_000, days),
    })
    rows = []
    clocks = ("09:30:00", *model.CHECKPOINT_TIMES)
    for day_index, (date, close, open_price) in enumerate(zip(dates, closes, opens)):
        day_signal = returns[day_index] * 0.4
        for minute_index, clock in enumerate(clocks):
            progress = minute_index / (len(clocks) - 1)
            price = open_price + (close - open_price) * progress + close * day_signal * 0.02
            rows.append({
                "trade_time": f"{date.date().isoformat()} {clock}",
                "ts_code": "600150.SH",
                "open": open_price,
                "high": price * 1.002,
                "low": price * 0.998,
                "close": price,
                "volume": 100_000 + minute_index * 2_000,
                "amount": price * (100_000 + minute_index * 2_000),
            })
    return pd.DataFrame(rows), daily, moneyflow


def test_intraday_model_runs_trade_date_grouped_walk_forward(monkeypatch):
    minutes, daily, moneyflow = _histories()
    monkeypatch.setattr(model, "MIN_TRAIN_ROWS", 30)
    monkeypatch.setattr(model, "TRAIN_WINDOW_ROWS", 100)
    monkeypatch.setattr(model, "VALIDATION_DAYS", 20)
    latest_date = daily.iloc[-1]["trade_date"]

    output = model.fit_intraday_next_day_model({
        "intraday_realtime_ready": {
            "ready": True,
            "can_predict_intraday": True,
            "trade_date": latest_date,
            "asof_time": "15:00:00",
            "data_source": "Tushare direct realtime",
            "data_endpoint": "rt_min_daily",
        },
        "intraday_minute_history": minutes,
        "daily_price_history": daily,
        "moneyflow_history": moneyflow,
    })

    assert output["model_ready"] is True
    assert output["model_id"] == model.MODEL_ID
    assert output["latest_data_trade_date"] == latest_date
    assert output["asof_time"] == "15:00:00"
    assert output["prediction_basis"] == "next_trading_day_close_vs_current_trade_day_close"
    assert output["direction_label_anchor"] == "current_trade_day_official_close"
    assert output["feature_price_anchor"] == "latest_valid_intraday_trade_at_checkpoint"
    assert output["uses_intraday_snapshot"] is True
    assert output["inputs"]["realtime_endpoint"] == "rt_min_daily"
    assert output["training"]["trading_day_count"] >= 80
    assert output["validation"]["trading_day_count"] == 20
    assert "T-2" in output["validation"]["leakage_guard"]
    assert output["prob_up_1d"] + output["prob_down_1d"] == 1.0
    assert output["calibration_method"] == "none_small_sample"
    assert output["calibration_slope"] is None
    assert output["reliability_gate"]["passed"] is False
    assert "validation_sample_lt_50" in output["reliability_gate"]["reasons"]


def test_current_prediction_ignores_minutes_after_reported_asof():
    minutes, daily, moneyflow = _histories(80)
    current_date = daily.iloc[-1]["trade_date"]
    mask = (minutes["trade_time"].str.startswith(current_date)) & minutes["trade_time"].str.endswith("15:00:00")
    minutes.loc[mask, ["open", "high", "low", "close"]] = 999.0

    frame = model.build_intraday_feature_frame(minutes, daily, current_date, "10:15:00", moneyflow)
    current = frame[(frame["trade_date"] == current_date) & (frame["asof_time"] == "10:15:00")].iloc[0]

    assert current["asof_price"] < 100.0


def test_target_is_next_day_close_vs_current_day_close():
    minutes, daily, moneyflow = _histories(90)
    trade_date = daily.iloc[70]["trade_date"]
    next_trade_date = daily.iloc[71]["trade_date"]
    daily.loc[daily["trade_date"] == trade_date, "close"] = 100.0
    daily.loc[daily["trade_date"] == next_trade_date, "close"] = 101.0
    mask = minutes["trade_time"].str.startswith(trade_date)
    minutes.loc[mask, ["open", "high", "low", "close"]] = [102.0, 103.0, 101.5, 102.0]

    frame = model.build_intraday_feature_frame(minutes, daily, trade_date, "15:00:00", moneyflow)
    row = frame[(frame["trade_date"] == trade_date) & (frame["asof_time"] == "15:00:00")].iloc[0]

    assert row["asof_price"] == 102.0
    assert row["target"] == 1.0


def test_probability_prefers_ready_intraday_model(monkeypatch):
    intraday = {
        "model_ready": True,
        "model_id": model.MODEL_ID,
        "prob_up_1d": 0.57,
        "prob_down_1d": 0.43,
    }
    monkeypatch.setattr(probability, "fit_intraday_next_day_model", lambda reports: intraday)
    monkeypatch.setattr(probability, "fit_next_day_model", lambda reports: (_ for _ in ()).throw(AssertionError("daily fallback called")))

    assert probability.compute_next_day_probability({}) is intraday


def test_probability_never_uses_daily_fallback_during_realtime_run(monkeypatch):
    intraday = model.unavailable_model("validation_failed")
    monkeypatch.setattr(probability, "fit_intraday_next_day_model", lambda reports: intraday)
    monkeypatch.setattr(
        probability,
        "fit_next_day_model",
        lambda reports: (_ for _ in ()).throw(AssertionError("daily fallback called")),
    )

    output = probability.compute_next_day_probability({
        "intraday_realtime_ready": {
            "status": "PASS",
            "ready": True,
            "trade_date": "2026-07-17",
            "asof_time": "14:22:00",
            "asof_price": 33.25,
        }
    })

    assert output["model_ready"] is False
    assert output["latest_data_trade_date"] == "2026-07-17"
    assert output["uses_intraday_snapshot"] is True
    assert output["fallback_reason"] == "validation_failed"
