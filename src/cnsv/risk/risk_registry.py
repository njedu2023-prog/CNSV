from __future__ import annotations

import json
from pathlib import Path

from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS
from cnsv.risk import RISK_STAGE, RISK_VERSION
from cnsv.risk.risk_evidence_loader import REQUIRED_RISK_REPORTS
from cnsv.utils.io import ensure_parent


def build_risk_explanation_registry() -> list[dict[str, object]]:
    return [
        {
            "registry_type": "risk_explanation",
            "version": RISK_VERSION,
            "stage": RISK_STAGE,
            "inputs": list(REQUIRED_RISK_REPORTS.values()),
            "outputs": [
                "latest_risk_explanation_report.json",
                "latest_risk_explanation_report.md",
                "risk.html",
            ],
            "is_trade_signal": False,
            "forbidden": FORBIDDEN_ACTIONS,
            "next_stage": "V2.0 live manual decision system",
        }
    ]


def write_risk_explanation_registry(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(build_risk_explanation_registry(), ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return target
