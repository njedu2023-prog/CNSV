from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from cnsv.utils.io import ensure_parent


def render_report_md(payload: dict[str, Any]) -> str:
    gate = payload["cnsvdata_gate"]
    manifest = payload["data_manifest"]
    summary = payload["loaded_data_summary"]
    validation = payload["validation"]
    lines = [
        "# CNSV Data Status Report",
        "",
        "## CNSVdata Gate",
        f"- ready: {gate.get('ready')}",
        f"- status: {gate.get('status')}",
        f"- can_continue: {gate.get('can_continue')}",
        f"- can_run_backtest: {gate.get('can_run_backtest')}",
        f"- can_use_moneyflow_as_strong_factor: {gate.get('can_use_moneyflow_as_strong_factor')}",
        f"- can_generate_formal_signal: False",
        f"- blocking_reason: {gate.get('blocking_reason')}",
        "",
        "## Data Manifest",
        f"- snapshot_id: {manifest.get('snapshot_id')}",
        f"- latest_trade_date: {manifest.get('latest_trade_date')}",
        f"- generated_at: {manifest.get('generated_at')}",
        f"- file_count: {manifest.get('file_count')}",
        "",
        "## Loaded Data",
        f"- daily_rows: {summary.get('daily_rows')}",
        f"- one_min_rows: {summary.get('one_min_rows')}",
        f"- moneyflow_rows: {summary.get('moneyflow_rows')}",
        f"- latest_trade_date: {summary.get('latest_trade_date')}",
        "",
        "## Validation",
        f"- status: {validation.get('status')}",
        f"- failed_count: {validation.get('failed_count')}",
        f"- warn_count: {validation.get('warn_count')}",
        "",
        "## Feature Summary",
        f"- price_volume: {payload['features'].get('price_volume')}",
        f"- minute_structure: {payload['features'].get('minute_structure')}",
        f"- moneyflow: {payload['features'].get('moneyflow')}",
        "",
        "## Forbidden Actions",
    ]
    lines.extend(f"- {item}" for item in payload.get("forbidden_actions", []))
    lines.extend(["", "## Next Step", "- Continue V1.1 feature enhancement only after V1.0 data gate remains stable."])
    return "\n".join(lines) + "\n"


def write_report_md(payload: dict[str, Any], output_md: str | Path, archive_dir: str | Path | None = None) -> list[Path]:
    content = render_report_md(payload)
    targets = [ensure_parent(output_md)]
    if archive_dir:
        archive = Path(archive_dir) / f"{date.today().isoformat()}_data_report.md"
        targets.append(ensure_parent(archive))
    for target in targets:
        target.write_text(content, encoding="utf-8")
    return targets
