from cnsv.backtest.backtest_evaluator import evaluate_observation_backtest


def test_forbidden_trade_field_fails_observation_backtest():
    payload = {
        "meta": {"is_trade_signal": False},
        "forbidden_actions": ["formal_signal_generation", "auto_order", "broker_api"],
        "backtest_scope": {"standard_sample_size": 1, "purged_sample_size": 1},
        "observation_backtest_leakage_checks": {"status": "PASS"},
        "model_backtest_metrics": {"standard_walk_forward": {}, "purged_walk_forward": {}},
        "observation_bucket_metrics": {},
        "model_comparison": {},
        "observation_condition_quality": {},
        "target_price": 1,
    }
    assert evaluate_observation_backtest(payload)["status"] == "FAIL"
