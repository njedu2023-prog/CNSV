import json

from cnsv.cli.run_risk_explanation import main
from cnsv.utils.io import repo_root


def test_risk_explanation_cli_generates_outputs():
    assert main() == 0
    root = repo_root()
    report_path = root / "docs/data/latest_risk_explanation_report.json"
    assert report_path.exists()
    assert (root / "docs/data/risk_explanation_registry.json").exists()
    assert (root / "reports/latest_risk_explanation_report.md").exists()
    assert (root / "docs/risk.html").exists()
    assert 'href="risk.html"' in (root / "docs/index.html").read_text(encoding="utf-8")
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["meta"]["version"] == "1.6"
    assert payload["meta"]["is_trade_signal"] is False
    assert payload["risk_explanation_quality"]["status"] in {"PASS", "WARN"}
