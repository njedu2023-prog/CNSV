from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from cnsv.utils.io import ensure_parent


def write_baseline_validation_report_md(payload: dict[str, Any], path: str | Path, archive_dir: str | Path | None = None) -> Path:
    target = ensure_parent(path)
    text = build_markdown(payload)
    target.write_text(text, encoding="utf-8")
    if archive_dir:
        archive = ensure_parent(Path(archive_dir) / f"{date.today().isoformat()}_baseline_validation_report.md")
        archive.write_text(text, encoding="utf-8")
    return target


def build_markdown(payload: dict[str, Any]) -> str:
    quality = payload.get("validation_quality", {})
    scope = payload.get("validation_scope", {})
    lines = [
        "# CNSV V1.2.2 Baseline Validation 报告",
        "",
        "本报告只验证 B0/B1/B2/B3 基准模型的历史分布预测质量，不生成交易信号、不输出买卖建议。",
        "",
        "## 验证质量",
        f"- 状态: {quality.get('status', 'N/A')}",
        f"- FAIL 数量: {quality.get('failed_count', 'N/A')}",
        f"- WARN 数量: {quality.get('warn_count', 'N/A')}",
        "",
        "## 验证范围",
        f"- 模型: {', '.join(scope.get('models', []))}",
        f"- 周期: {scope.get('horizons', [])}",
        "- walk-forward: YES",
        f"- validation_step: {scope.get('validation_step', 'N/A')}",
        f"- purged 模式: {scope.get('purged_sample_mode', 'N/A')}",
        "",
        "## 防未来函数",
    ]
    leakage = payload.get("leakage_checks", {})
    lines += [
        f"- 状态: {leakage.get('status', 'N/A')}",
        f"- 检查次数: {leakage.get('check_count', 'N/A')}",
        f"- 规则: {leakage.get('max_training_date_rule', 'N/A')}",
        f"- 重叠样本说明: {leakage.get('overlap_note', 'N/A')}",
        "",
        "## 模型指标",
    ]
    standard = payload.get("model_metrics", {}).get("standard_walk_forward_metrics", {})
    for model_id, horizons in standard.items():
        lines += ["", f"### {model_id}"]
        for horizon, row in horizons.items():
            lines.append(
                "- "
                f"{horizon}: sample={row.get('sample_size')}, "
                f"coverage={_pct(row.get('p10_p90_interval_coverage'))}, "
                f"brier={_num(row.get('positive_prob_brier'))}, "
                f"directional_accuracy={_pct(row.get('directional_accuracy'))}, "
                f"fallback_rate={_pct(row.get('fallback_rate'))}"
            )
    lines += ["", "## B2 vs B1"]
    for mode, horizons in payload.get("b2_vs_b1", {}).items():
        lines += ["", f"### {mode}"]
        for horizon, row in horizons.items():
            lines.append(
                "- "
                f"{horizon}: conclusion={row.get('B2_vs_B1_conclusion')}, "
                f"coverage_delta={_num(row.get('B2_vs_B1_interval_coverage_delta'))}, "
                f"brier_delta={_num(row.get('B2_vs_B1_brier_delta'))}, "
                f"pinball_delta={_num(row.get('B2_vs_B1_pinball_loss_delta'))}"
            )
    lines += [
        "",
        "## 禁止动作",
        "- 正式交易信号: NO",
        "- 买入/卖出建议: NO",
        "- 目标仓位/股数: NO",
        f"- forbidden_actions: {', '.join(payload.get('forbidden_actions', []))}",
        "",
        "## 下一阶段",
        f"- {payload.get('next_stage', 'N/A')}",
        "",
        "## 生成信息",
        f"- generated_at: {payload.get('meta', {}).get('generated_at', 'N/A')}",
    ]
    return "\n".join(lines) + "\n"


def _num(value: Any) -> str:
    return "N/A" if value is None else f"{float(value):.4f}"


def _pct(value: Any) -> str:
    return "N/A" if value is None else f"{float(value) * 100:.2f}%"
