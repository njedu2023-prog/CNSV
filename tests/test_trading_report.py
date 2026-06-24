import pandas as pd

from cnsv.trading.evidence_loader import load_trading_evidence
from cnsv.trading.fusion import build_trading_decision_payload, _decision_timeline
from cnsv.trading.live_stats import update_live_stats_registry
from cnsv.trading.report import build_trading_markdown
from cnsv.utils.io import repo_root


def test_trading_report_payload_contains_required_sections():
    payload = build_trading_decision_payload(load_trading_evidence(repo_root()))
    markdown = build_trading_markdown(payload)

    assert payload["version"] == "CNSV_V3.0"
    assert payload["auto_order_enabled"] is False
    assert payload["broker_api_enabled"] is False
    assert payload["historical_validation"]["baseline_directional_accuracy"]["standard"]["directional_accuracy"] is not None
    assert payload["model_performance"]["historical_stats"]["name"] == "历史统计线"
    assert payload["model_performance"]["live_stats"]["name"] == "实盘统计线"
    assert payload["model_performance"]["live_stats"]["start_date"] == "2026-06-21"
    assert payload["decision_timeline"]["data_trade_date"] == payload["trade_date"]
    assert payload["decision_timeline"]["signal_date"]
    assert payload["decision_timeline"]["prediction_date"]
    assert payload["decision_timeline"]["verify_date"]
    assert payload["market_snapshot"]["latest_trade_date"]
    assert payload["market_snapshot"]["latest_close"] is not None
    assert set(payload["price_prediction_distribution"]) == {"5D", "10D", "20D"}
    assert payload["price_prediction_distribution"]["5D"]["terminal_price_p50"] is not None
    assert payload["decision"]["signal"] in {"STRONG_BUY", "BUY", "HOLD", "WATCH", "REDUCE", "SELL", "STRONG_SELL", "BLOCKED"}
    assert "今日总决策" in markdown
    assert "信号生成日" in markdown
    assert "预测日" in markdown
    assert "收盘价" in markdown
    assert "5D / 10D / 20D 价格预测分布" in markdown
    assert "历史验证与回测" in markdown
    assert "模型表现追踪" in markdown
    assert "实盘统计线方向准确率" in markdown
    assert "人工交易决策参考" in markdown


def test_trading_timeline_uses_trade_calendar_after_data_trade_date():
    timeline = _decision_timeline(
        "2026-06-18",
        {"signal": "SELL"},
        {
            "trade_calendar": ["2026-06-18", "2026-06-22", "2026-06-23"],
            "trade_calendar_source": "unit_test_calendar",
        },
    )

    assert timeline["prediction_date"] == "2026-06-22"
    assert timeline["verify_date"] == "2026-06-22"
    assert timeline["signal_date"] == "2026-06-22"
    assert timeline["prediction_date_source"] == "trade_calendar"
    assert timeline["verify_date_source"] == "trade_calendar"


def test_trading_timeline_fallback_skips_known_a_share_holidays():
    timeline = _decision_timeline("2026-06-18", {"signal": "SELL"}, {})

    assert timeline["prediction_date"] == "2026-06-22"
    assert timeline["verify_date"] == "2026-06-22"


def test_live_stats_verifies_missed_sample_from_daily_history(tmp_path):
    registry_path = tmp_path / "live_stats_registry.json"
    registry_path.write_text(
        """[
  {
    "trade_date": "2026-06-22",
    "data_trade_date": "2026-06-18",
    "signal_date": "2026-06-22",
    "verify_date": "2026-06-22",
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
        "decision_timeline": {
            "signal_date": "2026-06-24",
            "prediction_date": "2026-06-24",
            "verify_date": "2026-06-24",
            "data_trade_date": "2026-06-23",
        },
        "decision": {"signal": "SELL"},
        "market_snapshot": {"latest_trade_date": "2026-06-23", "latest_close": 35.81},
    }
    reports = {
        "daily_price_history": pd.DataFrame(
            {
                "trade_date": ["2026-06-18", "2026-06-22", "2026-06-23"],
                "close": [36.14, 37.0, 35.81],
            }
        ),
        "feature_report": {"features": {"price_volume": {"latest_trade_date": "2026-06-23", "latest_close": 35.81}}},
    }

    registry = update_live_stats_registry(payload, registry_path, reports)

    verified = [item for item in registry if item.get("signal_date") == "2026-06-22"][0]
    assert verified["actual_direction"] == "UP"
    assert verified["is_correct"] is False
