from __future__ import annotations

from typing import Any

from cnsv.data.downloader import fetch_json


ALLOWED_USAGE_KEYS = (
    "can_develop_cnsv_main_program",
    "can_run_daily_ingest",
    "can_run_backtest",
    "can_use_moneyflow_as_strong_factor",
    "can_generate_formal_signal",
)


def _remote_url(source_config: dict[str, Any], key: str) -> str:
    base = source_config["cnsvdata"]["raw_base_url"].rstrip("/")
    path = source_config["required_remote_files"][key].lstrip("/")
    return f"{base}/{path}"


def load_downstream_ready(source_config: dict[str, Any]) -> dict[str, Any]:
    return fetch_json(_remote_url(source_config, "downstream_ready"))


def evaluate_downstream_gate(payload: dict[str, Any]) -> dict[str, Any]:
    ready = bool(payload.get("ready", False))
    status = str(payload.get("status", "FAIL")).upper()
    allowed_usage = payload.get("allowed_usage") or {}
    warnings: list[str] = []
    blocking_reason = payload.get("blocking_reason")

    if status not in {"PASS", "WARN", "FAIL"}:
        warnings.append(f"unknown status {status}; treated as FAIL")
        status = "FAIL"

    usage = {key: bool(allowed_usage.get(key, False)) for key in ALLOWED_USAGE_KEYS}

    can_continue = True
    if not ready:
        can_continue = False
        blocking_reason = blocking_reason or "CNSVdata downstream_ready.ready is false"
    if status == "FAIL":
        can_continue = False
        blocking_reason = blocking_reason or "CNSVdata downstream_ready.status is FAIL"
    if not usage["can_develop_cnsv_main_program"]:
        can_continue = False
        blocking_reason = blocking_reason or "CNSVdata does not allow CNSV main program development"
    if status == "WARN":
        warnings.append("CNSVdata status is WARN; only degraded data-status work is allowed")
    if not usage["can_generate_formal_signal"]:
        warnings.append("formal signal generation is forbidden by CNSVdata allowed_usage")
    if not usage["can_use_moneyflow_as_strong_factor"]:
        warnings.append("moneyflow strong-factor usage is forbidden; use low confidence only")

    return {
        "ready": ready,
        "status": status,
        "can_continue": can_continue,
        "can_develop": usage["can_develop_cnsv_main_program"],
        "can_develop_cnsv_main_program": usage["can_develop_cnsv_main_program"],
        "can_run_daily_ingest": usage["can_run_daily_ingest"],
        "can_run_backtest": usage["can_run_backtest"],
        "can_use_moneyflow_as_strong_factor": usage["can_use_moneyflow_as_strong_factor"],
        "can_generate_formal_signal": usage["can_generate_formal_signal"],
        "blocking_reason": blocking_reason,
        "warnings": warnings,
    }
