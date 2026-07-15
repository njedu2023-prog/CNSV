from __future__ import annotations

from typing import Any

from cnsv.trading.next_day_model import fit_next_day_model


def compute_next_day_probability(reports: dict[str, Any]) -> dict[str, Any]:
    return fit_next_day_model(reports)
