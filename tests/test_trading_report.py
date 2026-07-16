import pandas as pd

from cnsv.trading.evidence_loader import load_trading_evidence
from cnsv.trading.fusion import build_trading_decision_payload, _decision_timeline
from cnsv.trading.live_stats import update_live_stats_registry
from cnsv.trading.report import build_trading_markdown, write_trading_markdown
from cnsv.utils.io import repo_root


def test_trading_report_payload_contains_required_sections():
    payload = build_trading_decision_payload(load_trading_evidence(repo_root()))
    markdown = build_trading_markdown(payload)

    assert payload["version"] == "CNSV_V3.0"
    assert payload["auto_order_enabled"] is False
    assert payload["broker_api_enabled"] is False
    assert "next_day_directional_accuracy" in payload["historical_validation"]
    assert payload["model_performance"]["historical_stats"]["name"] == "历史统计线"
    assert payload["model_performance"]["live_stats"]["name"] == "实盘统计线"
    assert payload["model_performance"]["live_stats"]["start_date"] == "2026-07-15"
    assert payload["decision_timeline"]["data_trade_date"] == payload["trade_date"]
    assert payload["decision_timeline"]["signal_date"]
    assert payload["decision_timeline"]["prediction_date"]
    assert payload["decision_timeline"]["verify_date"]
    assert payload["timezone"] == "Asia/Shanghai"
    assert payload["generated_at_beijing"].endswith("+08:00")
    assert payload["freshness"]["data_trade_date"] == payload["trade_date"]
    assert payload["freshness"]["decision_trade_date"] == payload["decision_timeline"]["prediction_date"]
    assert payload["freshness"]["valid_until_beijing"].endswith("T15:00:00+08:00")
    assert payload["freshness"]["runtime_status_required"] is True
    assert payload["probability"]["model_id"] == "T1_HGB_ENSEMBLE_V1"
    assert payload["probability"]["prob_flat_1d"] == 0.0
    assert payload["market_snapshot"]["latest_trade_date"]
    assert payload["market_snapshot"]["latest_close"] is not None
    assert set(payload["price_prediction_distribution"]) == {"5D", "10D", "20D"}
    assert payload["price_prediction_distribution"]["5D"]["terminal_price_p50"] is not None
    assert payload["decision"]["signal"] in {"STRONG_BUY", "BUY", "HOLD", "WATCH", "REDUCE", "SELL", "STRONG_SELL", "BLOCKED"}
    assert "今日总决策" in markdown
    assert "信号生成日" in markdown
    assert "预测日" in markdown
    assert "行情基准价" in markdown
    assert "行情截止时间" in markdown
    assert "预测口径" in markdown
    assert "5D / 10D / 20D 价格预测分布" in markdown
    assert "历史验证与回测" in markdown
    assert "T+1 扩展窗口方向准确率" in markdown
    assert "模型表现追踪" in markdown
    assert "实盘统计线方向准确率" in markdown
    assert "人工交易决策参考" in markdown


def test_trading_timeline_uses_trade_calendar_after_data_trade_date():
    timeline = _decision_timeline(
        "2026-06-18",
        {"predicted_direction": "DOWN"},
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


def test_realtime_probability_controls_data_date_and_market_basis(monkeypatch):
    import cnsv.trading.fusion as fusion

    evidence = load_trading_evidence(repo_root())
    monkeypatch.setattr(
        fusion,
        "compute_next_day_probability",
        lambda reports: {
            "model_ready": True,
            "model_id": "T1_INTRADAY_20M_HGB_V2",
            "predicted_direction": "UP",
            "prob_up_1d": 0.56,
            "prob_down_1d": 0.44,
            "prob_flat_1d": 0.0,
            "direction_confidence": 0.56,
            "latest_data_trade_date": "2026-07-16",
            "asof_time": "14:10:00",
            "asof_price": 33.12,
            "asof_amount": 2_000_000_000,
            "asof_pct_chg": -0.4,
            "prediction_basis": "next_trading_day_close_vs_current_trade_day_close",
            "direction_label_anchor": "current_trade_day_official_close",
            "feature_price_anchor": "latest_valid_intraday_trade_at_checkpoint",
            "uses_intraday_snapshot": True,
            "reliability_gate": {"passed": True, "reasons": []},
            "validation": {},
            "model_return_distribution": {},
        },
    )
    evidence["trade_calendar"] = ["2026-07-16", "2026-07-17"]

    payload = fusion.build_trading_decision_payload(evidence)

    assert payload["trade_date"] == "2026-07-16"
    assert payload["decision_timeline"]["prediction_date"] == "2026-07-17"
    assert payload["market_snapshot"]["latest_close"] == 33.12
    assert payload["market_snapshot"]["asof_time"] == "14:10:00"
    assert payload["market_snapshot"]["price_kind"] == "intraday_asof"
    assert payload["market_snapshot"]["direction_label_anchor"] == "current_trade_day_official_close"
    assert payload["market_snapshot"]["feature_price_anchor"] == "latest_valid_intraday_trade_at_checkpoint"
    assert payload["model_sources"]["next_day_model"] == "T1_INTRADAY_20M_HGB_V2"


def test_trading_timeline_fallback_skips_known_a_share_holidays():
    timeline = _decision_timeline("2026-06-18", {"predicted_direction": "DOWN"}, {})

    assert timeline["prediction_date"] == "2026-06-22"
    assert timeline["verify_date"] == "2026-06-22"


def test_realtime_timeline_fails_closed_without_trade_calendar():
    timeline = _decision_timeline(
        "2026-07-17",
        {"predicted_direction": "UP"},
        {"reports": {"intraday_realtime_ready": {"ready": True}}},
    )

    assert timeline["prediction_date"] == ""
    assert timeline["verify_date"] == ""
    assert timeline["prediction_date_source"] == "trade_calendar_unavailable"


def test_realtime_model_date_mismatch_is_blocked(monkeypatch):
    import cnsv.trading.fusion as fusion

    evidence = load_trading_evidence(repo_root())
    evidence["reports"]["intraday_realtime_ready"] = {
        "status": "PASS",
        "ready": True,
        "trade_date": "2026-07-17",
        "asof_time": "14:22:00",
        "asof_price": 33.25,
    }
    evidence["trade_calendar"] = ["2026-07-17", "2026-07-20"]
    monkeypatch.setattr(
        fusion,
        "compute_next_day_probability",
        lambda reports: {
            "model_ready": True,
            "model_id": "T1_INTRADAY_TEST",
            "predicted_direction": "UP",
            "prob_up_1d": 0.56,
            "prob_down_1d": 0.44,
            "direction_confidence": 0.56,
            "latest_data_trade_date": "2026-07-16",
            "uses_intraday_snapshot": True,
            "reliability_gate": {"passed": True, "reasons": []},
            "validation": {},
            "model_return_distribution": {},
        },
    )

    payload = fusion.build_trading_decision_payload(evidence)

    assert payload["trade_date"] == "2026-07-17"
    assert payload["decision"]["signal"] == "BLOCKED"
    assert any("实时交易日不一致" in reason for reason in payload["risk"]["block_reasons"])


def test_trading_archive_uses_beijing_generation_date(tmp_path):
    payload = build_trading_decision_payload(load_trading_evidence(repo_root()))
    payload["generated_at_beijing"] = "2026-07-14T00:05:00+08:00"

    write_trading_markdown(payload, tmp_path / "latest.md", tmp_path / "archive")

    assert (tmp_path / "archive/2026-07-14_trading_decision_report.md").exists()


def test_live_stats_verifies_missed_sample_from_daily_history(tmp_path):
    registry_path = tmp_path / "live_stats_registry.json"
    registry_path.write_text(
        """[
  {
    "trade_date": "2026-07-16",
    "data_trade_date": "2026-07-15",
    "signal_date": "2026-07-16",
    "verify_date": "2026-07-16",
    "predicted_direction": "DOWN",
    "model_id": "T1_HGB_ENSEMBLE_V1",
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
            "signal_date": "2026-07-17",
            "prediction_date": "2026-07-17",
            "verify_date": "2026-07-17",
            "data_trade_date": "2026-07-16",
        },
        "decision": {"signal": "SELL"},
        "probability": {
            "model_ready": True,
            "model_id": "T1_HGB_ENSEMBLE_V1",
            "predicted_direction": "DOWN",
            "prob_up_1d": 0.47,
            "prob_down_1d": 0.53,
        },
        "market_snapshot": {"latest_trade_date": "2026-06-23", "latest_close": 35.81},
    }
    reports = {
        "daily_price_history": pd.DataFrame(
            {
                "trade_date": ["2026-07-15", "2026-07-16", "2026-07-17"],
                "close": [36.14, 37.0, 35.81],
            }
        ),
        "feature_report": {"features": {"price_volume": {"latest_trade_date": "2026-06-23", "latest_close": 35.81}}},
    }

    registry = update_live_stats_registry(payload, registry_path, reports)

    verified = [item for item in registry if item.get("signal_date") == "2026-07-16"][0]
    assert verified["actual_direction"] == "UP"
    assert verified["is_correct"] is False
