import json
from cnsv.live.live_evidence_loader import REQUIRED_LIVE_REPORTS, load_live_evidence
def test_live_evidence_loader_records_available_and_missing_reports(tmp_path):
 data_dir=tmp_path/"docs/data"; data_dir.mkdir(parents=True)
 for key,fn in REQUIRED_LIVE_REPORTS.items():
  if key!="risk_explanation_report": (data_dir/fn).write_text(json.dumps({"meta":{"latest_trade_date":"2026-06-18"}}),encoding="utf-8")
 av=load_live_evidence(tmp_path)["live_decision_evidence_availability"]
 assert "risk_explanation_report" in av["missing_reports"]; assert av["all_required_available"] is False
def test_live_evidence_loader_quality_warnings(tmp_path):
 data_dir=tmp_path/"docs/data"; data_dir.mkdir(parents=True)
 for fn in REQUIRED_LIVE_REPORTS.values(): (data_dir/fn).write_text(json.dumps({"meta":{"latest_trade_date":"2026-06-18"},"risk_explanation_quality":{"status":"WARN"}}),encoding="utf-8")
 av=load_live_evidence(tmp_path)["live_decision_evidence_availability"]
 assert av["missing_reports"]==[]; assert av["available_reports"]
