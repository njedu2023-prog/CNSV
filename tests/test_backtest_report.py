from cnsv.backtest.backtest_report import build_observation_backtest_markdown


def test_backtest_markdown_declares_not_trade_signal():
    text = build_observation_backtest_markdown({
        "meta": {"version": "1.4", "stage": "V1.4_observation_backtest", "latest_trade_date": "20260618"},
        "backtest_scope": {"horizons": [5, 10, 20], "models": [], "standard_sample_size": 1, "purged_sample_size": 1},
        "observation_backtest_quality": {"status": "PASS", "failed_count": 0, "warn_count": 0},
        "model_backtest_metrics": {"standard_walk_forward": {}, "purged_walk_forward": {}},
        "model_comparison": {"standard_walk_forward": {}},
        "observation_condition_quality": {},
        "observation_backtest_leakage_checks": {"status": "PASS", "check_count": 1, "purged_sample_mode": "every_horizon_step"},
        "forbidden_actions": ["formal_signal_generation", "auto_order", "broker_api"],
        "next_stage": "V1.5 human decision support",
    })
    assert "观察级回测" in text
    assert "不生成交易信号" in text
