import json

from cnsv.risk.risk_evidence_loader import load_risk_evidence


def test_risk_evidence_loader_records_missing_reports(tmp_path):
    data_dir = tmp_path / "docs" / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "latest_human_decision_support_report.json").write_text(json.dumps({"meta": {"version": "1.5"}}), encoding="utf-8")

    evidence = load_risk_evidence(tmp_path)

    assert evidence["risk_evidence_availability"]["all_required_available"] is False
    assert "data_report" in evidence["risk_evidence_availability"]["missing_reports"]
    assert evidence["reports"]["data_report"] is None
