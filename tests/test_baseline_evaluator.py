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
    assert any(check["name"] == "no_trade_signal_fields" for check in quality["checks"])


def test_baseline_evaluator_treats_controlled_b2_fallback_as_non_gating():
    models = {
        "B0_random_walk": {
            "horizons": {"5D": {"p10_return": -0.1, "p50_return": 0, "p90_return": 0.1, "p10_price": 9, "p50_price": 10, "p90_price": 11}}
        },
        "B1_historical_distribution": {
            "horizons": {"5D": {"p05_return": -0.2, "p10_return": -0.1, "p25_return": -0.05, "p50_return": 0, "p75_return": 0.05, "p90_return": 0.1, "p95_return": 0.2, "p10_price": 9, "p50_price": 10, "p90_price": 11}}
        },
        "B2_state_grouped_distribution": {
            "horizons": {
                "5D": {
                    "state_sample_size": 0,
                    "fallback_used": True,
                    "fallback_reason": "state_sample_size_lt_30",
                    "p10_return": -0.1,
                    "p50_return": 0,
                    "p90_return": 0.1,
                    "p10_price": 9,
                    "p50_price": 10,
                    "p90_price": 11,
                }
            }
        },
        "B3_volatility_adjusted": {
            "horizons": {"5D": {"p10_return": -0.1, "p50_return": 0, "p90_return": 0.1, "p10_price": 9, "p50_price": 10, "p90_price": 11}}
        },
    }
    quality = evaluate_baseline_models(models, horizons=(5,))
    assert quality["status"] == "PASS"
    assert quality["warn_count"] == 0
    assert quality["gating_warning_count"] == 0
    assert quality["non_gating_warning_count"] == 1
    assert quality["fallback_count"] == 1
    assert quality["fallback_notes"][0]["gating"] is False
