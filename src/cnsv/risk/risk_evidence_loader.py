from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_RISK_REPORTS = {
    "data_report": "latest_data_report.json",
    "feature_report": "latest_feature_report.json",
    "baseline_model_report": "latest_baseline_model_report.json",
    "baseline_validation_report": "latest_baseline_validation_report.json",
    "path_distribution_report": "latest_path_distribution_report.json",
    "path_validation_report": "latest_path_validation_report.json",
    "observation_backtest_report": "latest_observation_backtest_report.json",
    "human_decision_support_report": "latest_human_decision_support_report.json",
}


def load_risk_evidence(root: str | Path) -> dict[str, Any]:
    data_dir = Path(root) / "docs" / "data"
    reports: dict[str, Any] = {}
    availability: dict[str, Any] = {
        "all_required_available": True,
        "available_reports": [],
        "missing_reports": [],
        "reports": {},
    }
    for key, filename in REQUIRED_RISK_REPORTS.items():
        path = data_dir / filename
        if not path.exists():
            availability["all_required_available"] = False
            availability["missing_reports"].append(key)
            availability["reports"][key] = {"available": False, "path": str(path), "reason": "missing_report"}
            reports[key] = None
            continue
        try:
            reports[key] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            availability["all_required_available"] = False
            availability["missing_reports"].append(key)
            availability["reports"][key] = {"available": False, "path": str(path), "reason": f"invalid_json: {exc}"}
            reports[key] = None
            continue
        availability["available_reports"].append(key)
        availability["reports"][key] = {"available": True, "path": str(path)}
    return {"reports": reports, "risk_evidence_availability": availability}


def quality_status(report: dict[str, Any] | None, key: str) -> str:
    if not isinstance(report, dict):
        return "MISSING"
    if key == "cnsvdata_gate":
        gate = report.get("cnsvdata_gate") or {}
        return str(gate.get("gate_status") or gate.get("status") or "N/A")
    return str((report.get(key) or {}).get("status") or "N/A")
