from __future__ import annotations

from typing import Any

from cnsv.trading.utils import clamp, get_path, normal_cdf, safe_float


BIN_MIDPOINTS = {
    "gt_5pct": 0.065,
    "plus_2_to_5pct": 0.035,
    "zero_to_plus_2pct": 0.01,
    "zero_to_minus_2pct": -0.01,
    "minus_2_to_5pct": -0.035,
    "lt_minus_5pct": -0.065,
}


def compute_return_distribution(reports: dict[str, Any], probability: dict[str, Any]) -> dict[str, Any]:
    baseline = reports.get("baseline_model_report") or {}
    b3 = get_path(baseline, "baseline_models", "B3_volatility_adjusted", "horizons", "5D", default={})
    b2 = get_path(baseline, "baseline_models", "B2_state_grouped_distribution", "horizons", "5D", default={})

    mean_5d = safe_float(b2.get("mean_return"), safe_float(b3.get("mean_return"), 0.0))
    p10_5d = safe_float(b2.get("p10_return"), safe_float(b3.get("p10_return"), -0.05))
    p50_5d = safe_float(b2.get("p50_return"), safe_float(b3.get("p50_return"), 0.0))
    p90_5d = safe_float(b2.get("p90_return"), safe_float(b3.get("p90_return"), 0.05))

    # Convert a 5D distribution into a conservative 1D proxy.
    mean_1d = mean_5d / 5.0
    p10_1d = p10_5d / (5.0 ** 0.5)
    p50_1d = p50_5d / 5.0
    p90_1d = p90_5d / (5.0 ** 0.5)
    sigma = max((p90_1d - p10_1d) / 2.563, 0.005)

    gt_5 = 1.0 - normal_cdf(0.05, mean_1d, sigma)
    plus_2_5 = normal_cdf(0.05, mean_1d, sigma) - normal_cdf(0.02, mean_1d, sigma)
    zero_plus_2 = normal_cdf(0.02, mean_1d, sigma) - normal_cdf(0.0, mean_1d, sigma)
    zero_minus_2 = normal_cdf(0.0, mean_1d, sigma) - normal_cdf(-0.02, mean_1d, sigma)
    minus_2_5 = normal_cdf(-0.02, mean_1d, sigma) - normal_cdf(-0.05, mean_1d, sigma)
    lt_minus_5 = normal_cdf(-0.05, mean_1d, sigma)
    bins = {
        "gt_5pct": clamp(gt_5),
        "plus_2_to_5pct": clamp(plus_2_5),
        "zero_to_plus_2pct": clamp(zero_plus_2),
        "zero_to_minus_2pct": clamp(zero_minus_2),
        "minus_2_to_5pct": clamp(minus_2_5),
        "lt_minus_5pct": clamp(lt_minus_5),
    }
    total = sum(bins.values()) or 1.0
    bins = {key: value / total for key, value in bins.items()}
    expected = sum(BIN_MIDPOINTS[key] * value for key, value in bins.items())
    if probability.get("prob_up_1d", 0.0) > probability.get("prob_down_1d", 0.0):
        expected = max(expected, mean_1d)
    else:
        expected = min(expected, mean_1d)

    return {
        "return_bins_1d": bins,
        "expected_return_1d": expected,
        "median_return_1d": p50_1d,
        "p10_return_1d": p10_1d,
        "p90_return_1d": p90_1d,
        "distribution_source": "B2_state_grouped_distribution_5D_scaled_to_1D",
    }
