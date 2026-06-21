from cnsv.trading.evidence_loader import load_trading_evidence
from cnsv.trading.fusion import build_trading_decision_payload
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
    assert payload["decision"]["signal"] in {"STRONG_BUY", "BUY", "HOLD", "WATCH", "REDUCE", "SELL", "STRONG_SELL", "BLOCKED"}
    assert "今日总决策" in markdown
    assert "历史验证与回测" in markdown
    assert "模型表现追踪" in markdown
    assert "实盘统计线方向准确率" in markdown
    assert "人工交易决策参考" in markdown
