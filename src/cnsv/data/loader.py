from __future__ import annotations

from typing import Any

from cnsv.data.data_manifest import load_data_manifest
from cnsv.data.downloader import fetch_parquet, fetch_text
from cnsv.data.downstream_ready import evaluate_downstream_gate, load_downstream_ready
from cnsv.utils.errors import DownstreamGateError

CORE_DATA_KEYS = (
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


def remote_url(source_config: dict[str, Any], key: str) -> str:
    base = source_config["cnsvdata"]["raw_base_url"].rstrip("/")
    path = source_config["required_remote_files"][key].lstrip("/")
    return f"{base}/{path}"


def load_failure_summary(source_config: dict[str, Any]) -> str:
    return fetch_text(remote_url(source_config, "failure_summary"))


def load_all_core_data(source_config: dict[str, Any]) -> dict[str, Any]:
    downstream_ready = load_downstream_ready(source_config)
    gate = evaluate_downstream_gate(downstream_ready)
    if not gate["can_continue"]:
        raise DownstreamGateError(gate["blocking_reason"] or "CNSVdata gate blocked loading")

    data_manifest = load_data_manifest(source_config)
    bundle: dict[str, Any] = {"downstream_ready": downstream_ready, "gate": gate, "data_manifest": data_manifest}
    for key in CORE_DATA_KEYS:
        bundle[key] = fetch_parquet(remote_url(source_config, key))
    return bundle
