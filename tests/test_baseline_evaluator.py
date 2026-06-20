from cnsv.models.baseline_evaluator import evaluate_baseline_models


def test_baseline_evaluator_rejects_forbidden_field_names():
    models = {
        "B0_random_walk": {"horizons": {"5D": {"p10_return": -0.1, "p50_return": 0, "p90_return": 0.1, "bad_signal": 1}}},
        "B1_historical_distribution": {"horizons": {}},
        "B2_state_grouped_distribution": {"horizons": {}},
        "B3_volatility_adjusted": {"horizons": {}},
    }
    quality = evaluate_baseline_models(models, horizons=(5,))
    assert quality["status"] == "FAIL"
    assert any(check["name"] == "forbidden_fields_absent" for check in quality["checks"])

