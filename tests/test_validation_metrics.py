from cnsv.validation.metrics import compare_b2_vs_b1, pinball_loss, summarize_prediction_rows


def test_validation_metrics_calculate_coverage_brier_and_pinball():
    rows = [
        {"actual_return": 0.05, "p10_return": -0.02, "p50_return": 0.01, "p90_return": 0.08, "positive_prob": 0.7, "fallback_used": False},
        {"actual_return": -0.03, "p10_return": -0.05, "p50_return": 0.00, "p90_return": 0.04, "positive_prob": 0.4, "fallback_used": True},
    ]
    metrics = summarize_prediction_rows(rows)
    assert metrics["sample_size"] == 2
    assert metrics["p10_p90_interval_coverage"] == 1.0
    assert round(metrics["positive_prob_brier"], 4) == 0.125
    assert metrics["fallback_rate"] == 0.5
    assert pinball_loss(0.05, 0.01, 0.5) == 0.02


def test_b2_vs_b1_comparison_uses_observation_language():
    payload = {
        "standard_walk_forward_metrics": {
            "B1_historical_distribution": {"5D": {"positive_prob_brier": 0.25, "pinball_loss_p50": 0.02, "directional_accuracy": 0.5, "p10_p90_interval_coverage": 0.8, "median_error": 0.01}},
            "B2_state_grouped_distribution": {"5D": {"positive_prob_brier": 0.20, "pinball_loss_p50": 0.01, "directional_accuracy": 0.6, "p10_p90_interval_coverage": 0.82, "median_error": 0.005}},
        },
        "purged_walk_forward_metrics": {},
    }
    comparison = compare_b2_vs_b1(payload)["standard_walk_forward_metrics"]["5D"]
    assert comparison["B2_vs_B1_brier_delta"] < 0
    assert comparison["B2_vs_B1_conclusion"] == "B2 shows improvement"
