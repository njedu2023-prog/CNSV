from __future__ import annotations

from pathlib import Path

from cnsv.backtest.backtest_registry import write_observation_backtest_registry
from cnsv.backtest.backtest_report import write_observation_backtest_html, write_observation_backtest_json, write_observation_backtest_md
from cnsv.backtest.observation_backtest import run_observation_backtest
from cnsv.data.loader import load_all_core_data
from cnsv.path.path_distribution import run_path_distribution
from cnsv.path.path_registry import write_path_registry
from cnsv.path.path_report import write_path_distribution_json, write_path_validation_json
from cnsv.path.path_validation import run_path_validation
from cnsv.report.feature_report_html import write_feature_report_html
from cnsv.report.path_report_html import write_path_report_html
from cnsv.report.path_report_md import write_path_distribution_report_md, write_path_validation_report_md
from cnsv.utils.io import load_default_config, repo_root


def main() -> int:
    cfg = load_default_config()
    root = repo_root()
    bundle = load_all_core_data(cfg["data_source"])
    gate = bundle["gate"]
    _ensure_path_artifacts(root, bundle, gate)
    payload = run_observation_backtest(bundle, gate)
    write_observation_backtest_json(payload, root / "docs/data/latest_observation_backtest_report.json")
    write_observation_backtest_registry(root / "docs/data/observation_backtest_registry.json")
    write_observation_backtest_md(payload, root / "reports/latest_observation_backtest_report.md", root / "reports/archive")
    write_observation_backtest_html(root / "docs/backtest.html")
    write_feature_report_html(root / "docs/index.html")
    _ensure_backtest_entry(root / "docs/index.html")
    quality = payload["observation_backtest_quality"]
    print(f"observation_backtest_quality={quality['status']} failed={quality['failed_count']} warn={quality['warn_count']}")
    return 0 if quality["status"] in {"PASS", "WARN"} else 1


def _ensure_path_artifacts(root: Path, bundle: dict, gate: dict) -> None:
    distribution_path = root / "docs/data/latest_path_distribution_report.json"
    validation_path = root / "docs/data/latest_path_validation_report.json"
    if distribution_path.exists() and validation_path.exists():
        return
    distribution = run_path_distribution(bundle, gate)
    validation = run_path_validation(bundle, gate)
    write_path_distribution_json(distribution, distribution_path)
    write_path_validation_json(validation, validation_path)
    write_path_registry(root / "docs/data/path_distribution_registry.json")
    write_path_distribution_report_md(distribution, root / "reports/latest_path_distribution_report.md", root / "reports/archive")
    write_path_validation_report_md(validation, root / "reports/latest_path_validation_report.md", root / "reports/archive")
    write_path_report_html(root / "docs/path.html")


def _ensure_backtest_entry(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if 'href="backtest.html"' not in text:
        text = text.replace("</nav>", '<a href="backtest.html">Observation Backtest Report</a></nav>')
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
