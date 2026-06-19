from __future__ import annotations

import json

from cnsv.data.data_manifest import load_data_manifest, validate_manifest
from cnsv.data.downstream_ready import evaluate_downstream_gate, load_downstream_ready
from cnsv.utils.io import load_default_config


def main() -> int:
    config = load_default_config()["data_source"]
    ready = load_downstream_ready(config)
    gate = evaluate_downstream_gate(ready)
    result = {"gate": gate}
    if gate["can_continue"]:
        manifest = load_data_manifest(config)
        result["manifest_validation"] = validate_manifest(manifest, config)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if gate["can_continue"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
