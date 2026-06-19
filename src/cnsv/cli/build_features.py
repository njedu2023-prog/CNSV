from __future__ import annotations

import json

from cnsv.data.loader import load_all_core_data
from cnsv.features.feature_bundle import build_feature_bundle
from cnsv.utils.io import load_default_config


def main() -> int:
    config = load_default_config()["data_source"]
    bundle = load_all_core_data(config)
    features = build_feature_bundle(bundle, bundle["gate"])
    print(json.dumps(features, ensure_ascii=False, indent=2))
    return 0 if features.get("feature_status") in {"PASS", "WARN"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
