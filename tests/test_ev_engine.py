from cnsv.trading.ev_engine import compute_ev


def test_ev_engine_penalizes_tail_risk():
    base = {
        "return_bins_1d": {
            "gt_5pct": 0.1,
            "plus_2_to_5pct": 0.2,
            "zero_to_plus_2pct": 0.25,
            "zero_to_minus_2pct": 0.2,
            "minus_2_to_5pct": 0.15,
            "lt_minus_5pct": 0.1,
        },
        "p10_return_1d": -0.04,
    }
    ev = compute_ev(base)

    assert ev["cost_adjusted_ev"] < ev["raw_ev"]
    assert ev["risk_adjusted_ev"] < ev["cost_adjusted_ev"]
    assert ev["ev_rating"] in {"strong_positive", "positive", "neutral", "negative", "strong_negative"}
