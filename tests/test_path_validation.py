from __future__ import annotations

import pandas as pd

from cnsv.path.path_validation import run_path_validation, run_path_walk_forward_validation


def _bundle(rows: int = 310) -> dict:
    close = [10 + i * 0.02 + ((i % 7) - 3) * 0.01 for i in range(rows)]
    daily = pd.DataFrame(
        {
            "trade_date": [f"2026{(i // 28) + 1:02d}{(i % 28) + 1:02d}" for i in range(rows)],
            "close": close,
            "high": [x * 1.01 for x in close],
            "low": [x * 0.99 for x in close],
        }
    )
    return {"daily": daily, "moneyflow": pd.DataFrame(), "data_manifest": {"latest_trade_date": daily["trade_date"].iloc[-1]}}


def test_path_walk_forward_validation_no_future_training_data() -> None:
    out = run_path_walk_forward_validation(_bundle(), {"status": "PASS"}, validation_step=20)
    assert out["rows"]
    assert all(check["status"] == "PASS" for check in out["leakage_checks"])
    assert all(row["max_training_date"] <= row["as_of_date"] for row in out["rows"])
    assert all(row["truth_start_date"] > row["as_of_date"] for row in out["rows"])


def test_run_path_validation_outputs_quality_and_metrics() -> None:
    payload = run_path_validation(_bundle(), {"status": "PASS"}, validation_step=20)
    assert payload["path_validation_quality"]["status"] in {"PASS", "WARN"}
    assert payload["path_leakage_checks"]["status"] == "PASS"
    assert payload["meta"]["is_trade_signal"] is False
