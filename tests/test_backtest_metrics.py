from cnsv.backtest.backtest_metrics import summarize_observation_rows


def test_observation_metrics_include_brier_and_actual_rates():
    rows = [
        {"actual_positive_terminal": True, "actual_terminal_return": 0.1, "actual_touch_up_5pct": True, "actual_touch_down_5pct": False, "actual_touch_up_3pct": True, "actual_touch_up_8pct": True, "actual_touch_down_3pct": False, "actual_touch_down_8pct": False, "actual_max_up_return": 0.12, "actual_max_down_return": -0.02, "actual_max_drawdown": -0.03, "terminal_return_p50": 0.08, "terminal_return_p10": -0.02, "terminal_return_p90": 0.12, "max_up_return_p10": 0.02, "max_up_return_p90": 0.15, "max_down_return_p10": -0.05, "max_down_return_p90": 0.01, "max_drawdown_p10": -0.08, "max_drawdown_p90": -0.01, "touch_up_5pct_prob": 0.8, "touch_down_5pct_prob": 0.2, "touch_up_3pct_prob": 0.9, "touch_up_8pct_prob": 0.7, "touch_down_3pct_prob": 0.1, "touch_down_8pct_prob": 0.05, "positive_terminal_prob": 0.75, "fallback_used": False},
        {"actual_positive_terminal": False, "actual_terminal_return": -0.04, "actual_touch_up_5pct": False, "actual_touch_down_5pct": True, "actual_touch_up_3pct": False, "actual_touch_up_8pct": False, "actual_touch_down_3pct": True, "actual_touch_down_8pct": False, "actual_max_up_return": 0.02, "actual_max_down_return": -0.07, "actual_max_drawdown": -0.08, "terminal_return_p50": -0.01, "terminal_return_p10": -0.08, "terminal_return_p90": 0.05, "max_up_return_p10": 0.0, "max_up_return_p90": 0.08, "max_down_return_p10": -0.1, "max_down_return_p90": -0.01, "max_drawdown_p10": -0.12, "max_drawdown_p90": -0.02, "touch_up_5pct_prob": 0.3, "touch_down_5pct_prob": 0.6, "touch_up_3pct_prob": 0.4, "touch_up_8pct_prob": 0.1, "touch_down_3pct_prob": 0.7, "touch_down_8pct_prob": 0.2, "positive_terminal_prob": 0.4, "fallback_used": True},
    ]
    out = summarize_observation_rows(rows)
    assert out["sample_size"] == 2
    assert out["actual_touch_up_5pct_rate"] == 0.5
    assert out["actual_touch_down_5pct_rate"] == 0.5
    assert out["touch_up_5pct_brier"] is not None
    assert out["fallback_rate"] == 0.5
