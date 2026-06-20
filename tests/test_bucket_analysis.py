from cnsv.backtest.bucket_analysis import bucket_metric, build_condition_quality


def test_bucket_metric_splits_low_mid_high_and_delta():
    rows = [
        {"touch_up_5pct_prob": i / 10, "actual_terminal_return": i / 100, "actual_touch_up_5pct": i >= 6, "actual_positive_terminal": True, "actual_max_drawdown": -0.01 * i}
        for i in range(1, 10)
    ]
    grouped = bucket_metric(rows, "touch_up_5pct_prob")
    assert grouped["bucket_count"] == 3
    assert grouped["buckets"]["low"]["sample_size"] == 3
    assert grouped["buckets"]["high"]["sample_size"] == 3
    quality = build_condition_quality(rows)
    assert quality["touch_probability_groups"]["touch_up_5pct_prob"]["high_bucket_sample_size"] == 3
