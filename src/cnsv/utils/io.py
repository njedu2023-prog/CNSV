from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_yaml(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def ensure_parent(path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def load_default_config() -> dict[str, Any]:
    root = repo_root()
    return {
        "data_source": load_yaml(root / "config" / "data_source.yml"),
        "runtime": load_yaml(root / "config" / "runtime.yml"),
        "report": load_yaml(root / "config" / "report.yml"),
    }
