from __future__ import annotations

from cnsv.data.loader import load_all_core_data
from cnsv.path.path_distribution import run_path_distribution
from cnsv.path.path_registry import write_path_registry
from cnsv.path.path_report import write_path_distribution_json
from cnsv.report.feature_report_html import write_feature_report_html
from cnsv.report.path_report_html import write_path_report_html
from cnsv.report.path_report_md import write_path_distribution_report_md
from cnsv.utils.io import load_default_config, repo_root


def main() -> int:
    cfg = load_default_config()
    root = repo_root()
    bundle = load_all_core_data(cfg["data_source"])
    gate = bundle["gate"]
    payload = run_path_distribution(bundle, gate)
    write_path_distribution_json(payload, root / "docs/data/latest_path_distribution_report.json")
    write_path_registry(root / "docs/data/path_distribution_registry.json")
    write_path_distribution_report_md(payload, root / "reports/latest_path_distribution_report.md", root / "reports/archive")
    write_path_report_html(root / "docs/path.html")
    write_feature_report_html(root / "docs/index.html")
    _ensure_path_entry(root / "docs/index.html")
    quality = payload["path_quality"]
    print(f"path_quality={quality['status']} failed={quality['failed_count']} warn={quality['warn_count']}")
    return 0 if quality["status"] in {"PASS", "WARN"} else 1


def _ensure_path_entry(path) -> None:
    text = path.read_text(encoding="utf-8")
    if 'href="path.html"' not in text:
        marker = '<a href="validation.html">V1.2.2 验证看板</a>'
        if marker in text:
            text = text.replace(marker, marker + '<a href="path.html">V1.3 路径分布看板</a>')
        else:
            text = text.replace("</nav>", '<a href="path.html">V1.3 路径分布看板</a></nav>')
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
