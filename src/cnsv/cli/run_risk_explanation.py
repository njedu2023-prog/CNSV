from __future__ import annotations

from pathlib import Path

from cnsv.cli.run_human_decision_support import main as run_human_decision_support_main
from cnsv.report.feature_report_html import write_feature_report_html
from cnsv.risk.risk_evidence_loader import load_risk_evidence
from cnsv.risk.risk_fusion import build_risk_explanation_payload
from cnsv.risk.risk_registry import write_risk_explanation_registry
from cnsv.risk.risk_report import write_risk_explanation_html, write_risk_explanation_json, write_risk_explanation_md
from cnsv.utils.io import repo_root


def main() -> int:
    root = repo_root()
    _ensure_upstream_reports(root)
    evidence = load_risk_evidence(root)
    payload = build_risk_explanation_payload(evidence)
    write_risk_explanation_json(payload, root / "docs/data/latest_risk_explanation_report.json")
    write_risk_explanation_registry(root / "docs/data/risk_explanation_registry.json")
    write_risk_explanation_md(payload, root / "reports/latest_risk_explanation_report.md", root / "reports/archive")
    write_risk_explanation_html(root / "docs/risk.html")
    write_feature_report_html(root / "docs/index.html")
    quality = payload["risk_explanation_quality"]
    print(f"risk_explanation_quality={quality['status']} failed={quality['failed_count']} warn={quality['warn_count']}")
    return 0 if quality["status"] in {"PASS", "WARN"} else 1


def _ensure_upstream_reports(root: Path) -> None:
    required = root / "docs/data/latest_human_decision_support_report.json"
    if not required.exists():
        code = run_human_decision_support_main()
        if code != 0:
            raise RuntimeError("failed to generate V1.5 human decision support evidence")


if __name__ == "__main__":
    raise SystemExit(main())
