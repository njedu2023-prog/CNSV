from __future__ import annotations

from typing import Any

BIN_MIDPOINTS = {
    "gt_5pct": 0.065,
    "plus_2_to_5pct": 0.035,
    "zero_to_plus_2pct": 0.01,
    "zero_to_minus_2pct": -0.01,
    "minus_2_to_5pct": -0.035,
    "lt_minus_5pct": -0.065,
}


def compute_return_distribution(reports: dict[str, Any], probability: dict[str, Any]) -> dict[str, Any]:
    distribution = probability.get("model_return_distribution") or {}
    if distribution:
        return dict(distribution)
    return {
        "return_bins_1d": {
            "gt_5pct": 0.0,
            "plus_2_to_5pct": 0.0,
            "zero_to_plus_2pct": 0.5,
            "zero_to_minus_2pct": 0.5,
            "minus_2_to_5pct": 0.0,
            "lt_minus_5pct": 0.0,
        },
        "expected_return_1d": 0.0,
        "median_return_1d": 0.0,
        "p10_return_1d": -0.01,
        "p90_return_1d": 0.01,
        "distribution_source": "T1_model_unavailable_neutral_fallback",
        "sample_size": 0,
    }
