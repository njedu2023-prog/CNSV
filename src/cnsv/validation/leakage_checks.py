from __future__ import annotations

from typing import Any

import pandas as pd

FORBIDDEN_VALIDATION_KEYS = (
    "buy_signal",
    "sell_signal",
    "target_position",
    "target_shares",
    "stop_loss",
    "take_profit",
    "formal_signal",
    "trade_recommendation",
)


def max_training_date(frame: pd.DataFrame) -> str:
    if frame.empty or "trade_date" not in frame.columns:
        return ""
    return str(frame["trade_date"].astype(str).max())


def check_training_window(as_of_date: str, training_frames: list[pd.DataFrame]) -> dict[str, Any]:
    max_dates = [max_training_date(frame) for frame in training_frames if isinstance(frame, pd.DataFrame) and not frame.empty]
    latest = max(max_dates) if max_dates else ""
    passed = not latest or latest <= str(as_of_date)
    return {"name": "training_data_not_after_as_of_date", "status": "PASS" if passed else "FAIL", "max_training_date": latest, "as_of_date": as_of_date}


def contains_forbidden_validation_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, inner in value.items():
            if key in FORBIDDEN_VALIDATION_KEYS:
                return True
            if contains_forbidden_validation_key(inner):
                return True
    elif isinstance(value, list):
        return any(contains_forbidden_validation_key(item) for item in value)
    return False
