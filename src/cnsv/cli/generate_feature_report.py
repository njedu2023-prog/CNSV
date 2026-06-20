from __future__ import annotations

from cnsv.data.loader import load_all_core_data
from cnsv.features.feature_bundle import build_feature_bundle
from cnsv.features.feature_quality import check_feature_quality
from cnsv.features.feature_registry import build_feature_registry, write_feature_registry
from cnsv.report.feature_report_html import write_feature_report_html
from cnsv.report.feature_report_json import build_feature_report_payload, write_feature_report_json
from cnsv.report.feature_report_md import write_feature_report_md
from cnsv.utils.io import load_default_config, repo_root


def main() -> int:
    cfg = load_default_config()
    source = cfg["data_source"]
    root = repo_root()
    bundle = load_all_core_data(source)
    gate = bundle["gate"]
    features = build_feature_bundle(bundle, gate)
    quality = check_feature_quality(features, bundle, gate)
    registry = build_feature_registry()
    payload = build_feature_report_payload(gate, bundle.get("data_manifest") or {}, features, quality, registry)
    write_feature_report_json(payload, root / "docs/data/latest_feature_report.json")
    write_feature_report_md(payload, root / "reports/latest_feature_report.md", root / "reports/archive")
    write_feature_registry(root / "docs/data/feature_registry.json")
    write_feature_report_html(root / "docs/index.html")
    print(f"feature_quality={quality['status']} failed={quality['failed_count']} warn={quality['warn_count']}")
    return 0 if quality["status"] in {"PASS", "WARN"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
