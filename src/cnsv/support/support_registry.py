from __future__ import annotations

import json
from pathlib import Path

from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS
from cnsv.support import SUPPORT_STAGE, SUPPORT_VERSION
from cnsv.utils.io import ensure_parent


def build_human_decision_support_registry() -> list[dict[str, object]]:
    return [{
        "registry_type": "human_decision_support",
        "version": SUPPORT_VERSION,
        "stage": SUPPORT_STAGE,
        "outputs": ["latest_human_decision_support_report.json", "latest_human_decision_support_report.md", "decision_support.html"],
        "is_trade_signal": False,
        "forbidden": FORBIDDEN_ACTIONS,
        "next_stage": "V1.6 risk explanation",
    }]


def write_human_decision_support_registry(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(build_human_decision_support_registry(), ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return target
