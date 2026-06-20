from cnsv.models.baseline_registry import build_baseline_registry


def test_baseline_registry_declares_non_trade_models():
    registry = build_baseline_registry()
    assert {item["model_id"] for item in registry} == {
        "B0_random_walk",
        "B1_historical_distribution",
        "B2_state_grouped_distribution",
        "B3_volatility_adjusted",
    }
    assert all(item["is_trade_signal"] is False for item in registry)
    assert all(item["horizons"] == [5, 10, 20] for item in registry)
