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


def main() -> int:
    root = repo_root()
    _ensure_upstream_reports(root)
    evidence = load_live_evidence(root)
    payload = build_live_manual_decision_payload(evidence)
    write_live_json(payload, root / "docs/data/latest_live_manual_decision_report.json")
    write_live_manual_decision_registry(root / "docs/data/live_manual_decision_registry.json")
    write_live_markdown(payload, root / "reports/latest_live_manual_decision_report.md", root / "reports/archive")
    write_live_html(root / "docs/live.html")
    write_manual_logs(payload, root / "reports/manual_logs")
    write_feature_report_html(root / "docs/index.html")
    quality = payload["live_manual_decision_quality"]
    print(
        "live_manual_decision_quality="
        f"{quality['status']} failed={quality['failed_count']} warn={quality['warn_count']} "
        f"manual_decision_status={payload['manual_decision_status']}"
    )
    return 0 if quality["status"] in {"PASS", "WARN"} else 1


def _ensure_upstream_reports(root: Path) -> None:
    required = root / "docs/data/latest_risk_explanation_report.json"
    if not required.exists():
        code = run_risk_explanation_main()
        if code != 0:
            raise RuntimeError("failed to generate V1.6 risk explanation evidence")


if __name__ == "__main__":
    raise SystemExit(main())
