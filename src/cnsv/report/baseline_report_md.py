from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from cnsv.utils.io import ensure_parent


def _fmt(value: Any) -> str:
    if value is None or value == "":
        return "N/A"
    if isinstance(value, bool):
        return "YES" if value else "NO"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def _action(value: str) -> str:
    return {
        "formal_signal_generation": "正式交易动作生成",
        "auto_order": "自动下单",
        "broker_api": "券商接口",
    }.get(value, value)


def _model_lines(models: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for model_id, model in models.items():
        lines.extend(["", f"### {model_id}"])
        for horizon, row in (model.get("horizons") or {}).items():
            lines.append(
                f"- {horizon}: p10={_fmt(row.get('p10_return'))}, p50={_fmt(row.get('p50_return'))}, "
                f"p90={_fmt(row.get('p90_return'))}, p10_price={_fmt(row.get('p10_price'))}, "
                f"p50_price={_fmt(row.get('p50_price'))}, p90_price={_fmt(row.get('p90_price'))}, "
                f"sample={_fmt(row.get('sample_size', row.get('state_sample_size')))}, "
                f"fallback={_fmt(row.get('fallback_used'))}"
            )
    return lines


def _fallback_lines(notes: list[dict[str, Any]]) -> list[str]:
    if not notes:
        return ["- 无"]
    lines = []
    for note in notes:
        coverage = note.get("state_coverage") or {}
        lines.append(
            f"- {note.get('model')} {note.get('horizon')}: state_key={_fmt(note.get('state_key'))}, "
            f"reason={_fmt(note.get('reason'))}, "
            f"state_sample_size={_fmt(note.get('state_sample_size'))}, "
            f"usable_state_rows={_fmt(coverage.get('usable_state_rows'))}, "
            f"fallback_method={_fmt(note.get('fallback_method'))}, gating={_fmt(note.get('gating'))}, "
            f"non_blocking={_fmt(note.get('non_blocking'))}, "
            f"next_coverage_action={_fmt(note.get('next_coverage_action'))}"
        )
    return lines


def build_baseline_report_md(payload: dict[str, Any]) -> str:
    meta = payload.get("meta", {})
    gate = payload.get("cnsvdata_gate", {})
    feature_quality = payload.get("feature_quality", {})
    baseline_quality = payload.get("baseline_quality", {})
    state = payload.get("current_state", {})
    forbidden = payload.get("forbidden_actions", [])
    lines = [
        "# CNSV V1.2 基准模型报告",
        "",
        "本报告仅展示 5D/10D/20D 终端收益分布基准模型，不生成交易动作。",
        "",
        "## CNSVdata 数据门禁",
        f"- 状态: {_fmt(gate.get('status'))}",
        f"- 就绪: {_fmt(gate.get('ready'))}",
        f"- 允许继续: {_fmt(gate.get('can_continue'))}",
        "",
        "## 特征质量",
        f"- 状态: {_fmt(feature_quality.get('status'))}",
        f"- FAIL 数量: {_fmt(feature_quality.get('failed_count'))}",
        f"- WARN 数量: {_fmt(feature_quality.get('warn_count'))}",
        "",
        "## 基准模型质量",
        f"- 状态: {_fmt(baseline_quality.get('status'))}",
        f"- blocking_errors: {_fmt(baseline_quality.get('blocking_error_count', baseline_quality.get('failed_count')))}",
        f"- gating_warnings: {_fmt(baseline_quality.get('gating_warning_count', baseline_quality.get('warn_count')))}",
        f"- non_gating_warnings: {_fmt(baseline_quality.get('non_gating_warning_count'))}",
        f"- fallback_count: {_fmt(baseline_quality.get('fallback_count'))}",
        "",
        "## 受控回退说明",
        "B2 状态分组样本不足时透明回退到 B1 历史分布基准；该回退不生成正式交易信号，也不影响 V1.2 基准模型层验收状态。",
        *_fallback_lines(baseline_quality.get("fallback_notes", [])),
        "",
        "## 当前状态",
        f"- 最新交易日: {_fmt(meta.get('latest_trade_date'))}",
        f"- 最新收盘价: {_fmt(state.get('latest_close'))}",
        f"- 趋势状态: {_fmt(state.get('trend_state'))}",
        f"- 波动率状态: {_fmt(state.get('volatility_state'))}",
        f"- 资金流强弱: {_fmt(state.get('flow_strength_basic'))}",
        "",
        "## 基准模型",
        *_model_lines(payload.get("baseline_models", {})),
        "",
        "## 禁止动作",
        *(f"- {_action(item)}" for item in forbidden),
        f"- is_trade_signal: {_fmt(meta.get('is_trade_signal'))}",
        f"- can_generate_formal_signal: {_fmt(gate.get('can_generate_formal_signal'))}",
        "",
        "## 下一阶段",
        f"- {_fmt(payload.get('next_stage'))}",
        "",
        "## 生成信息",
        f"- generated_at: {_fmt(meta.get('generated_at'))}",
        f"- 数据快照: {_fmt(payload.get('data_manifest', {}).get('snapshot_id'))}",
        "",
    ]
    return "\n".join(lines)


def write_baseline_report_md(payload: dict[str, Any], latest_path: str | Path, archive_dir: str | Path) -> tuple[Path, Path]:
    text = build_baseline_report_md(payload)
    latest = ensure_parent(latest_path)
    latest.write_text(text, encoding="utf-8")
    archive = ensure_parent(Path(archive_dir) / f"{date.today().isoformat()}_baseline_model_report.md")
    archive.write_text(text, encoding="utf-8")
    return latest, archive
