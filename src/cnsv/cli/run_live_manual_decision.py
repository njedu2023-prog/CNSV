from __future__ import annotations
from pathlib import Path
from cnsv.cli.run_risk_explanation import main as run_risk_explanation_main
from cnsv.live.live_evidence_loader import load_live_evidence
from cnsv.live.live_fusion import build_live_manual_decision_payload
from cnsv.live.live_registry import write_live_manual_decision_registry
from cnsv.live.live_report import write_live_html, write_live_json, write_live_markdown
from cnsv.live.manual_log import write_manual_logs
from cnsv.report.feature_report_html import write_feature_report_html
from cnsv.utils.io import repo_root
def main()->int:
 root=repo_root(); _ensure_upstream_reports(root); evidence=load_live_evidence(root); payload=build_live_manual_decision_payload(evidence)
 write_live_json(payload,root/"docs/data/latest_live_manual_decision_report.json"); write_live_manual_decision_registry(root/"docs/data/live_manual_decision_registry.json"); write_live_markdown(payload,root/"reports/latest_live_manual_decision_report.md",root/"reports/archive"); write_live_html(root/"docs/live.html"); write_manual_logs(payload,root/"reports/manual_logs"); write_feature_report_html(root/"docs/index.html"); _ensure_live_entry(root/"docs/index.html")
 q=payload["live_manual_decision_quality"]; print(f"live_manual_decision_quality={q['status']} failed={q['failed_count']} warn={q['warn_count']} manual_decision_status={payload['manual_decision_status']}"); return 0 if q["status"] in {"PASS","WARN"} else 1
def _ensure_upstream_reports(root:Path)->None:
 if not (root/"docs/data/latest_risk_explanation_report.json").exists():
  code=run_risk_explanation_main()
  if code!=0: raise RuntimeError("failed to generate V1.6 risk explanation evidence")
def _ensure_live_entry(path:Path)->None:
 text=path.read_text(encoding="utf-8")
 if 'href="risk.html"' not in text: text=text.replace("</nav>",'<a href="risk.html">V1.6 风控解释</a></nav>')
 if 'href="live.html"' not in text: text=text.replace("</nav>",'<a href="live.html">Live Manual Decision Report</a></nav>')
 path.write_text(text,encoding="utf-8")
if __name__=="__main__": raise SystemExit(main())
