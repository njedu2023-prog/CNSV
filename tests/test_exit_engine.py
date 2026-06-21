from cnsv.trading.exit_engine import compute_exit_plan


def test_exit_engine_outputs_take_profit_and_stop_loss():
    reports = {"path_distribution_report": {"path_models": {"P2_state_conditional_path": {"horizons": {"5D": {}, "10D": {}}}}}}
    plan = compute_exit_plan(reports, {"p10_return_1d": -0.03}, {"risk_level": "MEDIUM"})

    assert plan["take_profit_range"]
    assert plan["stop_loss_reference"].startswith("-")
    assert plan["time_exit_days"] == 10
