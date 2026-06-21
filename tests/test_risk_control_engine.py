from cnsv.trading.risk_control import evaluate_trading_risk


def test_risk_control_blocks_buy_on_downside_tail():
    reports = {
        "data_report": {"cnsvdata_gate": {"ready": True, "status": "PASS"}},
        "feature_report": {"features": {"volatility": {"volatility_state": "normal_vol"}}},
        "baseline_validation_report": {"validation_quality": {"status": "PASS"}},
        "path_validation_report": {"path_validation_quality": {"status": "PASS"}},
    }
    risk = evaluate_trading_risk(
        reports,
        {"direction_confidence": 0.8},
        {"return_bins_1d": {"lt_minus_5pct": 0.2}, "p10_return_1d": -0.03},
        {"risk_adjusted_ev": 0.02},
    )

    assert risk["buy_blocked"] is True
    assert "大跌概率过高" in risk["buy_block_reasons"]
