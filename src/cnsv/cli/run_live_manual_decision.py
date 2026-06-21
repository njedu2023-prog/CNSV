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
    _ensure_live_entry(root / "docs/index.html")
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


def _ensure_live_entry(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace("<title>CNSV V1.4 主线看板</title>", "<title>CNSV V2.0 主线看板</title>")
    text = text.replace("<title>CNSV V1.5 主线看板</title>", "<title>CNSV V2.0 主线看板</title>")
    text = text.replace("CNSV V1.4 主线看板", "CNSV V2.0 主线看板")
    text = text.replace("CNSV V1.5 主线看板", "CNSV V2.0 主线看板")
    text = text.replace(
        "展示 CNSVdata 准入、数据覆盖、特征质量、路径分布、观察级回测与 V1.5 人工决策辅助入口。页面不生成交易动作。",
        "展示 CNSVdata 准入、数据覆盖、特征质量、路径分布、观察级回测、V1.6 风控解释与 V2.0 实盘人工决策入口。页面不生成交易动作。",
    )
    if 'href="risk.html"' not in text:
        text = text.replace("</nav>", '<a href="risk.html">V1.6 风控解释</a></nav>')
    if 'href="live.html"' not in text:
        text = text.replace("</nav>", '<a href="live.html">V2.0 实盘人工决策</a></nav>')
    text = text.replace("Live Manual Decision Report", "V2.0 实盘人工决策")
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
