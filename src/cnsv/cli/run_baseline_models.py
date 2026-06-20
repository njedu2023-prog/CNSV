from __future__ import annotations

from cnsv.data.loader import load_all_core_data
from cnsv.features.feature_bundle import build_feature_bundle
from cnsv.features.feature_quality import check_feature_quality
from cnsv.models.baseline_registry import build_baseline_registry, write_baseline_registry
from cnsv.models.baseline_runner import run_baseline_models
from cnsv.report.baseline_report_html import write_baseline_report_html
from cnsv.report.baseline_report_json import build_baseline_report_payload, write_baseline_report_json
from cnsv.report.baseline_report_md import write_baseline_report_md
from cnsv.report.feature_report_html import write_feature_report_html
from cnsv.utils.io import load_default_config, repo_root


def main() -> int:
    cfg = load_default_config()
    source = cfg["data_source"]
    root = repo_root()
    bundle = load_all_core_data(source)
    gate = bundle["gate"]
    features = build_feature_bundle(bundle, gate)
    feature_quality = check_feature_quality(features, bundle, gate)
    baseline_run = run_baseline_models(bundle, features)
    registry = build_baseline_registry()
    payload = build_baseline_report_payload(
        gate,
        bundle.get("data_manifest") or {},
        features,
        feature_quality,
        baseline_run,
        registry,
    )
    write_baseline_report_json(payload, root / "docs/data/latest_baseline_model_report.json")
    write_baseline_registry(root / "docs/data/baseline_registry.json")
    write_baseline_report_md(payload, root / "reports/latest_baseline_model_report.md", root / "reports/archive")
    write_baseline_report_html(root / "docs/baseline.html")
    write_feature_report_html(root / "docs/index.html")
    print(
        f"baseline_quality={baseline_run['status']} "
        f"failed={baseline_run['failed_count']} warn={baseline_run['warn_count']}"
    )
    return 0 if baseline_run["status"] in {"PASS", "WARN"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
