from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cnsv import __version__
from cnsv.data.data_manifest import manifest_summary
from cnsv.utils.io import ensure_parent


def loaded_data_summary(bundle: dict[str, Any]) -> dict[str, Any]:
    daily = bundle.get("daily")
    one_min = bundle.get("one_min")
    moneyflow = bundle.get("moneyflow")
    manifest = bundle.get("data_manifest") or {}
    return {
        "daily_rows": int(len(daily)) if daily is not None else 0,
        "one_min_rows": int(len(one_min)) if one_min is not None else 0,
        "moneyflow_rows": int(len(moneyflow)) if moneyflow is not None else 0,
        "latest_trade_date": manifest.get("latest_trade_date", ""),
    }


def build_report_payload(
    gate: dict[str, Any],
    manifest: dict[str, Any] | None = None,
    bundle: dict[str, Any] | None = None,
    validation: dict[str, Any] | None = None,
    features: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "meta": {
            "system": "CNSV",
            "version": __version__,
            "ts_code": "600150.SH",
            "name": "中国船舶",
            "mode": "research_mode",
            "report_type": "data_status_report",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "cnsvdata_gate": gate,
        "data_manifest": manifest_summary(manifest or {}),
        "loaded_data_summary": loaded_data_summary(bundle or {}),
        "validation": validation or {"status": "FAIL", "failed_count": 0, "warn_count": 0, "checks": []},
        "features": {
            "price_volume": (features or {}).get("price_volume", {}),
            "minute_structure": (features or {}).get("minute_structure", {}),
            "moneyflow": (features or {}).get("moneyflow", {}),
        },
        "allowed_actions": {
            "can_develop_cnsv_main_program": bool(gate.get("can_develop_cnsv_main_program") or gate.get("can_develop")),
            "can_run_daily_ingest": bool(gate.get("can_run_daily_ingest")),
            "can_run_backtest": bool(gate.get("can_run_backtest")),
            "can_generate_formal_signal": False,
        },
        "forbidden_actions": ["formal_signal_generation", "auto_order", "broker_api"],
    }


def write_report_json(payload: dict[str, Any], path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target
