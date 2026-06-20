from cnsv.backtest.model_comparison import compare_path_models


def test_model_comparison_outputs_legal_conclusions():
    metrics = {
        "P0_historical_path_replay": {"5D": {"terminal_p10_p90_coverage": 0.7, "touch_up_5pct_brier": 0.3, "touch_down_5pct_brier": 0.3, "positive_terminal_brier": 0.3, "drawdown_p10_p90_coverage": 0.6}},
        "P1_volatility_adjusted_path": {"5D": {"terminal_p10_p90_coverage": 0.75, "touch_up_5pct_brier": 0.2, "touch_down_5pct_brier": 0.2, "positive_terminal_brier": 0.2, "drawdown_p10_p90_coverage": 0.65}},
        "P2_state_conditional_path": {"5D": {"terminal_p10_p90_coverage": 0.76, "touch_up_5pct_brier": 0.19, "touch_down_5pct_brier": 0.19, "positive_terminal_brier": 0.19, "drawdown_p10_p90_coverage": 0.66, "fallback_rate": 0.0}},
    }
    out = compare_path_models(metrics)
    assert out["5D"]["P1_vs_P0_conclusion"] == "P1 improves over P0"
    assert out["5D"]["P2_vs_P1_conclusion"] in {"P2 improves over P1", "P2 is neutral versus P1", "P2 underperforms P1"}
