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


def test_intraday_model_must_pass_reliability_gate_before_actions():
    reports = {
        "data_report": {"cnsvdata_gate": {"ready": True, "status": "PASS"}},
        "feature_report": {"features": {"volatility": {"volatility_state": "normal_vol"}}},
        "baseline_validation_report": {"validation_quality": {"status": "PASS"}},
        "path_validation_report": {"path_validation_quality": {"status": "PASS"}},
    }

    risk = evaluate_trading_risk(
        reports,
        {
            "model_ready": True,
            "uses_intraday_snapshot": True,
            "direction_confidence": 0.8,
            "reliability_gate": {"passed": False, "reasons": ["high_confidence_sample_lt_20"]},
        },
        {"return_bins_1d": {"lt_minus_5pct": 0.01}, "p10_return_1d": -0.01},
        {"risk_adjusted_ev": 0.02},
    )

    assert risk["blocked"] is True
    assert any("可靠性门禁未通过" in reason for reason in risk["block_reasons"])
