from __future__ import annotations

from typing import Any

from cnsv.data.downloader import fetch_json
from cnsv.data.downstream_ready import _remote_url

REQUIRED_PARQUET_KEYS = (
    "trade_calendar",
    "daily",
    "one_min",
    "five_min",
    "fifteen_min",
    "thirty_min",
    "sixty_min",
    "moneyflow",
    "corporate_actions",
    "structural_breaks",
)


def load_data_manifest(source_config: dict[str, Any]) -> dict[str, Any]:
    return fetch_json(_remote_url(source_config, "data_manifest"))


def _file_items(files: Any) -> list[dict[str, Any]]:
    if isinstance(files, dict):
        return [{"path": key, **(value if isinstance(value, dict) else {})} for key, value in files.items()]
    if isinstance(files, list):
        return [item for item in files if isinstance(item, dict)]
    return []


def validate_manifest(manifest: dict[str, Any], source_config: dict[str, Any] | None = None) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "status": "PASS" if ok else "FAIL", "detail": detail})

    add("snapshot_id", bool(manifest.get("snapshot_id")), "snapshot_id is required")
    add("generated_at", bool(manifest.get("generated_at")), "generated_at is required")
    add("latest_trade_date", bool(manifest.get("latest_trade_date")), "latest_trade_date is required")
    files = _file_items(manifest.get("files"))
    add("files", bool(files), "files is required and must not be empty")

    file_paths = {str(item.get("path") or item.get("file") or item.get("name") or "") for item in files}
    required_paths: list[str] = []
    if source_config:
        required_map = source_config.get("required_remote_files", {})
        required_paths = [required_map[key] for key in REQUIRED_PARQUET_KEYS if key in required_map]
    for path in required_paths:
        add(f"required_file:{path}", path in file_paths, f"{path} must be present in manifest")

    for item in files:
        label = str(item.get("path") or item.get("file") or item.get("name") or "unknown")
        add(f"sha256:{label}", bool(item.get("sha256") or item.get("hash")), f"{label} sha256/hash is required")
        rows = item.get("rows")
        add(f"rows:{label}", isinstance(rows, int) and rows >= 0, f"{label} rows must be a non-negative integer")

    failed_count = sum(1 for check in checks if check["status"] == "FAIL")
    return {"status": "FAIL" if failed_count else "PASS", "failed_count": failed_count, "checks": checks}


def manifest_summary(manifest: dict[str, Any]) -> dict[str, Any]:
    files = _file_items(manifest.get("files"))
    return {
        "snapshot_id": manifest.get("snapshot_id", ""),
        "latest_trade_date": manifest.get("latest_trade_date", ""),
        "generated_at": manifest.get("generated_at", ""),
        "file_count": len(files),
    }
