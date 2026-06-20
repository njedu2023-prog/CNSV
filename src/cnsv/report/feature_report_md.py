from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from cnsv.utils.io import ensure_parent


def _fmt(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.4f}"
    if isinstance(value, bool):
        return "YES" if value else "NO"
    return str(value)


def build_feature_report_md(payload: dict[str, Any]) -> str:
    gate = payload.get("cnsvdata_gate", {})
    quality = payload.get("feature_quality", {})
    features = payload.get("features", {})
    pv = features.get("price_volume", {})
    minute = features.get("minute_structure", {})
    moneyflow = features.get("moneyflow", {})
    trend = features.get("trend", {})
    volatility = features.get("volatility", {})
    forbidden = payload.get("forbidden_actions", [])
    return "\n".join(
        [
            "# CNSV V1.1 Feature Report",
            "",
            "## CNSVdata Gate",
            f"- Status: {_fmt(gate.get('status'))}",
            f"- Ready: {_fmt(gate.get('ready'))}",
            f"- Can continue: {_fmt(gate.get('can_continue'))}",
            f"- Can generate formal signal: NO",
            "",
            "## Feature Quality",
            f"- Status: {_fmt(quality.get('status'))}",
            f"- Failed count: {_fmt(quality.get('failed_count'))}",
            f"- Warn count: {_fmt(quality.get('warn_count'))}",
            "",
            "## Latest Trade Date",
            f"- {_fmt(payload.get('meta', {}).get('latest_trade_date'))}",
            "",
            "## Price Volume Summary",
            f"- Close: {_fmt(pv.get('latest_close'))}",
            f"- Ret 1D: {_fmt(pv.get('ret_1d'))}",
            f"- MA20: {_fmt(pv.get('ma20'))}",
            f"- Price position 20D: {_fmt(pv.get('price_position_20d'))}",
            "",
            "## Minute Structure Summary",
            f"- Intraday close: {_fmt(minute.get('latest_intraday_close'))}",
            f"- Close position: {_fmt(minute.get('close_position_in_day_range'))}",
            f"- Last 30min return: {_fmt(minute.get('last_30min_return'))}",
            "",
            "## Moneyflow Summary",
            f"- Net moneyflow amount: {_fmt(moneyflow.get('net_mf_amount'))}",
            f"- Main force net: {_fmt(moneyflow.get('main_force_net'))}",
            f"- Flow strength score: {_fmt(moneyflow.get('flow_strength_score'))}",
            f"- Can use as strong factor: {_fmt(moneyflow.get('can_use_as_strong_factor'))}",
            "",
            "## Trend Summary",
            f"- Trend state: {_fmt(trend.get('trend_state'))}",
            f"- Close above MA20: {_fmt(trend.get('close_above_ma20'))}",
            "",
            "## Volatility Summary",
            f"- Realized vol 20D: {_fmt(volatility.get('realized_vol_20d'))}",
            f"- Volatility state: {_fmt(volatility.get('volatility_state'))}",
            "",
            "## Forbidden Actions",
            *(f"- {item}" for item in forbidden),
            "",
            "## Next Stage",
            f"- {_fmt(payload.get('next_stage'))}",
            "",
        ]
    )


def write_feature_report_md(payload: dict[str, Any], latest_path: str | Path, archive_dir: str | Path) -> tuple[Path, Path]:
    text = build_feature_report_md(payload)
    latest = ensure_parent(latest_path)
    latest.write_text(text, encoding="utf-8")
    archive = ensure_parent(Path(archive_dir) / f"{date.today().isoformat()}_feature_report.md")
    archive.write_text(text, encoding="utf-8")
    return latest, archive
