from __future__ import annotations

from cnsv.data.loader import load_all_core_data
from cnsv.report.baseline_validation_report_html import write_baseline_validation_report_html
from cnsv.report.baseline_validation_report_md import write_baseline_validation_report_md
from cnsv.report.feature_report_html import write_feature_report_html
from cnsv.utils.io import load_default_config, repo_root
from cnsv.validation.baseline_validation import run_baseline_validation, write_validation_json, write_validation_registry


def main() -> int:
    cfg = load_default_config()
    root = repo_root()
    bundle = load_all_core_data(cfg["data_source"])
    gate = bundle["gate"]
    payload = run_baseline_validation(bundle, gate)
    write_validation_json(payload, root / "docs/data/latest_baseline_validation_report.json")
    write_validation_registry(root / "docs/data/baseline_validation_registry.json")
    write_baseline_validation_report_md(payload, root / "reports/latest_baseline_validation_report.md", root / "reports/archive")
    write_baseline_validation_report_html(root / "docs/validation.html")
    write_feature_report_html(root / "docs/index.html")
    _ensure_validation_entry(root / "docs/index.html")
    quality = payload["validation_quality"]
    print(f"baseline_validation_quality={quality['status']} failed={quality['failed_count']} warn={quality['warn_count']}")
    return 0 if quality["status"] in {"PASS", "WARN"} else 1


def _ensure_validation_entry(path) -> None:
    text = path.read_text(encoding="utf-8")
    if 'href="validation.html"' in text:
        return
    text = text.replace(
        '<a href="baseline.html">V1.2 基准模型看板</a>',
        '<a href="baseline.html">V1.2.1 基准模型看板</a><a href="validation.html">V1.2.2 验证看板</a>',
    )
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
