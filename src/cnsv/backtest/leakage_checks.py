from __future__ import annotations

from typing import Any


def summarize_observation_leakage(checks: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [check for check in checks if check.get("status") != "PASS"]
    return {
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failed_count": len(failed),
        "checks": checks[:50],
        "purged_sample_mode": "every_horizon_step",
        "standard_walk_forward_enabled": True,
        "purged_walk_forward_enabled": True,
        "rules": [
            "max_prediction_input_date <= as_of_date",
            "state_date <= as_of_date",
            "truth_start_date > as_of_date",
            "truth_end_date > as_of_date",
            "purged rows use every horizon step to reduce overlap",
        ],
    }
