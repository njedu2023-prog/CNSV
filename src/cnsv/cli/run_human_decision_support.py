from __future__ import annotations

from pathlib import Path
from typing import Any

from cnsv.cli.run_observation_backtest import main as run_observation_backtest_main
from cnsv.report.feature_report_html import write_feature_report_html
from cnsv.support import FORBIDDEN_SUPPORT_FIELDS
from cnsv.support.evidence_fusion import build_human_decision_support_payload
from cnsv.support.evidence_loader import load_support_evidence
from cnsv.support.support_registry import write_human_decision_support_registry
from cnsv.support.support_report import (
    write_human_decision_support_html,
    write_human_decision_support_json,
    write_human_decision_support_md,
)
from cnsv.utils.io import repo_root


def main() -> int:
    root = repo_root()
    _ensure_upstream_reports(root)
    evidence = load_support_evidence(root)
    payload = build_human_decision_support_payload(evidence)
    write_human_decision_support_json(payload, root / "docs/data/latest_human_decision_support_report.json")
    write_human_decision_support_registry(root / "docs/data/human_decision_support_registry.json")
    write_human_decision_support_md(payload, root / "reports/latest_human_decision_support_report.md", root / "reports/archive")
    write_human_decision_support_html(root / "docs/decision_support.html")
    write_feature_report_html(root / "docs/index.html")
    quality = payload["human_decision_support_quality"]
    print(f"human_decision_support_quality={quality['status']} failed={quality['failed_count']} warn={quality['warn_count']}")
    return 0 if quality["status"] in {"PASS", "WARN"} else 1


def _ensure_upstream_reports(root: Path) -> None:
    required = root / "docs/data/latest_observation_backtest_report.json"
    if not required.exists():
        code = run_observation_backtest_main()
        if code != 0:
            raise RuntimeError("failed to generate V1.4 observation backtest evidence")


def _ensure_decision_support_entry(path: Path) -> None:
    _ensure_index_entry(path)


def _ensure_index_entry(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace("CNSV V1.4 主线看板", "CNSV V1.5 主线看板")
    if 'href="decision_support.html"' not in text:
        text = text.replace("</nav>", '<a href="decision_support.html">人工辅助</a></nav>')
    path.write_text(text, encoding="utf-8")


def _contains_forbidden_key(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(k) in FORBIDDEN_SUPPORT_FIELDS or _contains_forbidden_key(v) for k, v in value.items())
    if isinstance(value, list):
        return any(_contains_forbidden_key(v) for v in value)
    return False


if __name__ == "__main__":
    raise SystemExit(main())
