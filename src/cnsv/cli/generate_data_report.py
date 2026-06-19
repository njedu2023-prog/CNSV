from __future__ import annotations

from cnsv.data.data_manifest import load_data_manifest
from cnsv.data.downstream_ready import evaluate_downstream_gate, load_downstream_ready
from cnsv.data.loader import load_all_core_data
from cnsv.data.validator import validate_loaded_data
from cnsv.features.feature_bundle import build_feature_bundle
from cnsv.report.report_html import write_report_html
from cnsv.report.report_json import build_report_payload, write_report_json
from cnsv.report.report_md import write_report_md
from cnsv.utils.errors import DownstreamGateError
from cnsv.utils.io import load_default_config, repo_root


def main() -> int:
    cfg = load_default_config()
    source = cfg["data_source"]
    report = cfg["report"]["report"]
    root = repo_root()

    ready = load_downstream_ready(source)
    gate = evaluate_downstream_gate(ready)
    manifest = load_data_manifest(source) if gate["can_develop"] else {}
    bundle = None
    validation = None
    features = None
    exit_code = 0
    if gate["can_continue"]:
        try:
            bundle = load_all_core_data(source)
            manifest = bundle["data_manifest"]
            validation = validate_loaded_data(bundle)
            features = build_feature_bundle(bundle, gate)
            exit_code = 0 if validation["status"] in {"PASS", "WARN"} else 1
        except DownstreamGateError:
            exit_code = 1
        except Exception as exc:
            gate = {**gate, "can_continue": False, "blocking_reason": str(exc)}
            validation = {"status": "FAIL", "failed_count": 1, "warn_count": 0, "checks": [{"name": "report_generation", "status": "FAIL", "detail": str(exc)}]}
            exit_code = 1
    else:
        exit_code = 1

    payload = build_report_payload(gate, manifest, bundle, validation, features)
    write_report_json(payload, root / report["output_json"])
    write_report_md(payload, root / report["output_md"], root / report["archive_dir"])
    write_report_html(root / report["html_index"])
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
