import pandas as pd

from cnsv.trading.live_stats import build_model_performance, default_live_registry_entry, predicted_direction, update_live_stats_registry


def test_live_stats_are_separated_from_historical_stats():
    historical = {
        "baseline_directional_accuracy": {
            "standard": {
                "directional_accuracy": 0.507,
                "sample_size": 712,
            }
        }
    }
    registry = [
        {"signal_date": "2026-07-14", "model_id": "T1_HGB_ENSEMBLE_V1", "is_correct": True},
        {"signal_date": "2026-07-15", "model_id": "T1_HGB_ENSEMBLE_V1", "is_correct": None},
        {"signal_date": "2026-07-16", "model_id": "T1_HGB_ENSEMBLE_V1", "is_correct": True},
        {"signal_date": "2026-07-17", "model_id": "T1_HGB_ENSEMBLE_V1", "is_correct": False},
    ]

    perf = build_model_performance(historical, registry)

    assert perf["historical_stats"]["name"] == "历史统计线"
    assert perf["historical_stats"]["direction_accuracy"] == 0.507
    assert perf["historical_stats"]["sample_count"] == 712
    assert perf["live_stats"]["name"] == "实盘统计线"
    assert perf["live_stats"]["start_date"] == "2026-07-15"
    assert perf["live_stats"]["sample_count"] == 2
    assert perf["live_stats"]["correct_count"] == 1
    assert perf["live_stats"]["wrong_count"] == 1
    assert perf["live_stats"]["direction_accuracy"] == 0.5


def test_default_live_registry_entry_uses_v3_signal_date_and_direction():
    payload = {
        "decision": {"signal": "SELL"},
        "probability": {
            "model_id": "T1_HGB_ENSEMBLE_V1",
            "predicted_direction": "UP",
            "prob_up_1d": 0.53,
            "prob_down_1d": 0.47,
        },
        "decision_timeline": {"data_trade_date": "2026-07-15"},
    }
    entry = default_live_registry_entry(payload, "2026-07-16")

    assert entry["data_trade_date"] == "2026-07-15"
    assert entry["signal_date"] == "2026-07-16"
    assert entry["verify_date"] == "2026-07-17"
    assert entry["predicted_direction"] == "UP"
    assert entry["model_id"] == "T1_HGB_ENSEMBLE_V1"
    assert entry["is_correct"] is None
    assert predicted_direction({"decision": {"signal": "BUY"}}) is None
    assert predicted_direction({"decision": {"signal": "HOLD"}}) is None


def test_live_registry_skips_blocked_or_unverifiable_entries(tmp_path):
    path = tmp_path / "live_stats_registry.json"
    path.write_text(
        """[
  {
    "trade_date": "2026-06-21",
    "signal_date": "2026-06-21",
    "verify_date": "2026-06-22",
    "predicted_direction": "DOWN",
    "actual_direction": null,
    "is_correct": null,
    "close_t": null,
    "close_t1": null,
    "return_1d": null
  }
]
""",
        encoding="utf-8",
    )
    payload = {
        "decision": {"signal": "BLOCKED"},
        "decision_timeline": {"signal_date": "2026-06-23", "prediction_date": "2026-06-23", "verify_date": "2026-06-24"},
        "market_snapshot": {"latest_close": 36.14},
    }

    registry = update_live_stats_registry(payload, path, {"feature_report": {}})

    assert registry == []


def test_live_registry_drops_non_finite_base_close(tmp_path):
    path = tmp_path / "live_stats_registry.json"
    path.write_text(
        """[
  {
    "trade_date": "2026-06-22",
    "data_trade_date": "2026-06-18",
    "signal_date": "2026-06-21",
    "verify_date": "2026-06-22",
    "predicted_direction": "DOWN",
    "actual_direction": null,
    "is_correct": null,
    "close_t": NaN,
    "close_t1": null,
    "return_1d": null
  }
]
""",
        encoding="utf-8",
    )
    payload = {
        "decision": {"signal": "SELL"},
        "probability": {
            "model_ready": True,
            "model_id": "T1_HGB_ENSEMBLE_V1",
            "predicted_direction": "DOWN",
            "prob_up_1d": 0.47,
            "prob_down_1d": 0.53,
        },
        "decision_timeline": {
            "data_trade_date": "2026-07-15",
            "signal_date": "2026-07-16",
            "prediction_date": "2026-07-16",
            "verify_date": "2026-07-16",
        },
        "market_snapshot": {"latest_trade_date": "2026-07-15", "latest_close": 35.81},
    }

    registry = update_live_stats_registry(payload, path, {"feature_report": {}})

    assert len(registry) == 1
    assert registry[0]["signal_date"] == "2026-07-16"
    assert registry[0]["close_t"] == 35.81
    assert "NaN" not in path.read_text(encoding="utf-8")


def test_live_registry_drops_legacy_unverified_entries_without_base_date(tmp_path):
    path = tmp_path / "live_stats_registry.json"
    path.write_text(
        """[
  {
    "trade_date": "2026-06-22",
    "signal_date": "2026-06-22",
    "verify_date": "2026-06-23",
    "predicted_direction": "DOWN",
    "actual_direction": null,
    "is_correct": null,
    "close_t": 36.14,
    "close_t1": null,
    "return_1d": null
  }
]
""",
        encoding="utf-8",
    )
    payload = {
        "decision": {"signal": "SELL"},
        "probability": {
            "model_ready": True,
            "model_id": "T1_HGB_ENSEMBLE_V1",
            "predicted_direction": "DOWN",
            "prob_up_1d": 0.47,
            "prob_down_1d": 0.53,
        },
        "decision_timeline": {
            "data_trade_date": "2026-07-15",
            "signal_date": "2026-07-16",
            "prediction_date": "2026-07-16",
            "verify_date": "2026-07-16",
        },
        "market_snapshot": {"latest_trade_date": "2026-07-15", "latest_close": 37.33},
    }

    registry = update_live_stats_registry(payload, path, {"feature_report": {}})

    assert len(registry) == 1
    assert registry[0]["signal_date"] == "2026-07-16"
    assert registry[0]["data_trade_date"] == "2026-07-15"
    assert registry[0]["close_t"] == 37.33


def test_live_registry_backfills_verified_archive_entry(tmp_path):
    root = tmp_path
    archive = root / "reports/archive"
    archive.mkdir(parents=True)
    (archive / "2026-07-15_trading_decision_report.md").write_text(
        """# CNSV V3.0 交易决策系统报告

## 今日总决策
- 交易日: 2026-07-14
- 信号: SELL / 建议卖出
- 数据交易日: 2026-07-14
- 信号生成日: 2026-07-15
- 预测日: 2026-07-15
- 验证日: 2026-07-15
- 预测方向: DOWN
- 模型ID: T1_HGB_ENSEMBLE_V1
- 收盘价: 36.1400
""",
        encoding="utf-8",
    )
    (archive / "2026-07-16_trading_decision_report.md").write_text(
        """# CNSV V3.0 交易决策系统报告

## 今日总决策
- 交易日: 2026-07-14
- 信号: SELL / 建议卖出
- 数据交易日: 2026-07-14
- 信号生成日: 2026-07-16
- 预测日: 2026-07-15
- 验证日: 2026-07-15
- 预测方向: DOWN
- 模型ID: T1_HGB_ENSEMBLE_V1
- 收盘价: 36.1400
""",
        encoding="utf-8",
    )
    path = root / "docs/data/live_stats_registry.json"
    path.parent.mkdir(parents=True)
    path.write_text("[]\n", encoding="utf-8")
    payload = {
        "decision": {"signal": "SELL"},
        "probability": {
            "model_ready": True,
            "model_id": "T1_HGB_ENSEMBLE_V1",
            "predicted_direction": "DOWN",
            "prob_up_1d": 0.47,
            "prob_down_1d": 0.53,
        },
        "decision_timeline": {
            "data_trade_date": "2026-07-15",
            "signal_date": "2026-07-16",
            "prediction_date": "2026-07-16",
            "verify_date": "2026-07-16",
        },
        "market_snapshot": {"latest_trade_date": "2026-07-15", "latest_close": 37.33},
    }

    registry = update_live_stats_registry(
        payload,
        path,
        {"feature_report": {"features": {"price_volume": {"latest_trade_date": "2026-07-15", "latest_close": 37.33}}}},
    )
    performance = build_model_performance({"baseline_directional_accuracy": {"standard": {}}}, registry)

    verified = [item for item in registry if item["signal_date"] == "2026-07-15"][0]
    assert verified["actual_direction"] == "UP"
    assert verified["predicted_direction"] == "DOWN"
    assert verified["is_correct"] is False
    assert verified["close_t1"] == 37.33
    assert [item["trade_date"] for item in registry].count("2026-07-15") == 1
    assert performance["live_stats"]["sample_count"] == 1
    assert performance["live_stats"]["wrong_count"] == 1


def test_intraday_prediction_is_verified_with_two_official_daily_closes(tmp_path):
    path = tmp_path / "live_stats_registry.json"
    path.write_text("[]\n", encoding="utf-8")
    payload = {
        "decision": {"signal": "WATCH"},
        "probability": {
            "model_ready": True,
            "model_id": "T1_INTRADAY_20M_HGB_V3",
            "predicted_direction": "UP",
            "prob_up_1d": 0.56,
            "prob_down_1d": 0.44,
        },
        "decision_timeline": {
            "data_trade_date": "2026-07-17",
            "signal_date": "2026-07-20",
            "prediction_date": "2026-07-20",
            "verify_date": "2026-07-20",
        },
        "market_snapshot": {
            "latest_trade_date": "2026-07-17",
            "latest_close": 33.25,
            "asof_time": "14:22:00",
            "price_kind": "intraday_asof",
        },
    }

    first = update_live_stats_registry(payload, path, {"feature_report": {}})

    assert first[0]["asof_price"] == 33.25
    assert first[0]["close_t"] is None

    reports = {
        "daily_price_history": pd.DataFrame({
            "trade_date": ["2026-07-17", "2026-07-20"],
            "close": [33.0, 33.33],
            "pct_chg": [-3.0, 99.0],
        }),
        "feature_report": {},
    }
    verified = update_live_stats_registry(payload, path, reports)

    assert verified[0]["close_t"] == 33.0
    assert verified[0]["close_t1"] == 33.33
    assert verified[0]["return_1d"] == 33.33 / 33.0 - 1.0
    assert verified[0]["actual_direction"] == "UP"
    assert verified[0]["is_correct"] is True


def test_registry_preserves_prior_t1_model_versions(tmp_path):
    path = tmp_path / "live_stats_registry.json"
    path.write_text(
        """[
  {
    "trade_date": "2026-07-16",
    "data_trade_date": "2026-07-15",
    "signal_date": "2026-07-16",
    "verify_date": "2026-07-16",
    "predicted_direction": "DOWN",
    "model_id": "T1_INTRADAY_20M_HGB_V2",
    "asof_price": 36.14,
    "close_t": null,
    "is_correct": null
  }
]
""",
        encoding="utf-8",
    )

    registry = update_live_stats_registry({}, path, {"feature_report": {}})

    assert len(registry) == 1
    assert registry[0]["model_id"] == "T1_INTRADAY_20M_HGB_V2"
