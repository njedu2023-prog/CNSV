from cnsv.trading.evidence_loader import load_trading_evidence
from cnsv.trading.fusion import build_trading_decision_payload, _decision_timeline
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
