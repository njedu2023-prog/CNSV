from __future__ import annotations

from cnsv.path.path_metrics import actual_path_outcome, summarize_path_samples


def test_summarize_path_samples_quantiles_and_touch_probabilities() -> None:
    samples = [
        {"close_return_path": [0.01, 0.04], "high_return_path": [0.02, 0.06], "low_return_path": [-0.01, 0.01]},
        {"close_return_path": [-0.02, -0.04], "high_return_path": [0.01, 0.02], "low_return_path": [-0.03, -0.06]},
    ]
    row = summarize_path_samples(samples, 10.0, 2, "P0")
    assert row["terminal_return_p10"] <= row["terminal_return_p50"] <= row["terminal_return_p90"]
    assert row["terminal_price_p10"] > 0
    assert row["touch_up_5pct_prob"] == 0.5
    assert row["touch_down_5pct_prob"] == 0.5


def test_actual_path_outcome() -> None:
    out = actual_path_outcome([10.5, 11.0], [10.8, 11.2], [9.8, 10.2], 10.0)
    assert round(out["actual_terminal_return"], 4) == 0.1
    assert round(out["actual_max_up_return"], 4) == 0.12
    assert out["actual_touch_up_5pct"] is True
