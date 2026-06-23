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
        {"signal_date": "2026-06-20", "is_correct": True},
        {"signal_date": "2026-06-21", "is_correct": None},
        {"signal_date": "2026-06-22", "is_correct": True},
        {"signal_date": "2026-06-23", "is_correct": False},
    ]

    perf = build_model_performance(historical, registry)

    assert perf["historical_stats"]["name"] == "历史统计线"
    assert perf["historical_stats"]["direction_accuracy"] == 0.507
    assert perf["historical_stats"]["sample_count"] == 712
    assert perf["live_stats"]["name"] == "实盘统计线"
    assert perf["live_stats"]["start_date"] == "2026-06-21"
    assert perf["live_stats"]["sample_count"] == 2
    assert perf["live_stats"]["correct_count"] == 1
    assert perf["live_stats"]["wrong_count"] == 1
    assert perf["live_stats"]["direction_accuracy"] == 0.5


def test_default_live_registry_entry_uses_v3_signal_date_and_direction():
    payload = {
        "decision": {"signal": "SELL"},
        "decision_timeline": {"data_trade_date": "2026-06-22"},
    }
    entry = default_live_registry_entry(payload, "2026-06-21")

    assert entry["data_trade_date"] == "2026-06-22"
    assert entry["signal_date"] == "2026-06-21"
    assert entry["verify_date"] == "2026-06-22"
    assert entry["predicted_direction"] == "DOWN"
    assert entry["is_correct"] is None
    assert predicted_direction({"decision": {"signal": "BUY"}}) == "UP"


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
        "decision_timeline": {
            "data_trade_date": "2026-06-22",
            "signal_date": "2026-06-23",
            "prediction_date": "2026-06-23",
            "verify_date": "2026-06-24",
        },
        "market_snapshot": {"latest_trade_date": "2026-06-22", "latest_close": 37.33},
    }

    registry = update_live_stats_registry(payload, path, {"feature_report": {}})

    assert len(registry) == 1
    assert registry[0]["signal_date"] == "2026-06-23"
    assert registry[0]["data_trade_date"] == "2026-06-22"
    assert registry[0]["close_t"] == 37.33
