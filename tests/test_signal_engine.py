from cnsv.trading.signal_engine import decide_signal


def test_signal_engine_blocks_when_risk_blocked():
    result = decide_signal(
        {"prob_up_1d": 0.8, "prob_down_1d": 0.1, "direction_confidence": 0.9},
        {"return_bins_1d": {"lt_minus_5pct": 0.01}},
        {"risk_adjusted_ev": 0.03},
        {"blocked": True, "block_reasons": ["数据门禁失败"]},
    )

    assert result["signal"] == "BLOCKED"


def test_signal_engine_does_not_buy_when_ev_negative():
    result = decide_signal(
        {"prob_up_1d": 0.7, "prob_down_1d": 0.2, "direction_confidence": 0.8},
        {"return_bins_1d": {"lt_minus_5pct": 0.05}},
        {"risk_adjusted_ev": -0.01},
        {"blocked": False, "buy_blocked": True, "buy_block_reasons": ["风险调整 EV 为负"], "risk_level": "MEDIUM"},
    )

    assert result["signal"] != "BUY"
