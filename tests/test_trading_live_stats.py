from cnsv.trading.live_stats import build_model_performance, default_live_registry_entry, predicted_direction


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
    payload = {"decision": {"signal": "SELL"}}
    entry = default_live_registry_entry(payload, "2026-06-21")

    assert entry["signal_date"] == "2026-06-21"
    assert entry["verify_date"] == "2026-06-22"
    assert entry["predicted_direction"] == "DOWN"
    assert entry["is_correct"] is None
    assert predicted_direction({"decision": {"signal": "BUY"}}) == "UP"
