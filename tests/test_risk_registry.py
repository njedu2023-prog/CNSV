from cnsv.risk.risk_registry import build_risk_explanation_registry


def test_risk_registry_uses_v1_6_and_no_trade_signal():
    registry = build_risk_explanation_registry()[0]

    assert registry["version"] == "1.6"
    assert registry["stage"] == "V1.6_risk_explanation"
    assert registry["is_trade_signal"] is False
    assert "latest_risk_explanation_report.json" in registry["outputs"]
