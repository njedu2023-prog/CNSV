from cnsv.trading.position_engine import compute_position


def test_position_engine_sets_zero_for_blocked():
    position = compute_position(
        {"signal": "BLOCKED"},
        {"prob_up_1d": 0.7, "prob_down_1d": 0.2},
        {"risk_adjusted_ev": 0.02},
        {"risk_level": "HIGH"},
    )

    assert position["suggested_position_pct"] == 0.0
    assert position["manual_reference_only"] is True
