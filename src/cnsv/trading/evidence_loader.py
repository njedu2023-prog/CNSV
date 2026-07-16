from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPORT_FILES = {
    "data_report": "latest_data_report.json",
    "feature_report": "latest_feature_report.json",
    "baseline_model_report": "latest_baseline_model_report.json",
    "baseline_validation_report": "latest_baseline_validation_report.json",
    "path_distribution_report": "latest_path_distribution_report.json",
    "path_validation_report": "latest_path_validation_report.json",
    "observation_backtest_report": "latest_observation_backtest_report.json",
    "live_manual_decision_report": "latest_live_manual_decision_report.json",
    "risk_explanation_report": "latest_risk_explanation_report.json",
}


def load_trading_evidence(root: Path) -> dict[str, Any]:
    base = root / "docs/data"
    reports: dict[str, Any] = {}
    missing: list[str] = []
    for key, filename in REPORT_FILES.items():
        path = base / filename
        if not path.exists():
            missing.append(filename)
            reports[key] = {}
            continue
        reports[key] = json.loads(path.read_text(encoding="utf-8"))
    return {"reports": reports, "missing_reports": missing}
