from __future__ import annotations

import json
from pathlib import Path

from cnsv.path.path_distribution import build_path_registry
from cnsv.utils.io import ensure_parent


def write_path_registry(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(build_path_registry(), ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return target
