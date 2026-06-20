from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from cnsv.utils.io import ensure_parent


def write_path_distribution_report_md(payload: dict[str, Any], path: str | Path, archive_dir: str | Path | None = None) -> Path:
    target = ensure_parent(path)
    text = build_distribution_markdown(payload)
    target.write_text(text, encoding="utf-8")
    if archive_dir:
        archive = ensure_parent(Path(archive_dir) / f"{date.today().isoformat()}_path_distribution_report.md")
        archive.write_text(text, encoding="utf-8")
    return target


def write_path_validation_report_md(payload: dict[str, Any], path: str | Path, archive_dir: str | Path | None = None) -> Path:
    target = ensure_parent(path)
    text = build_validation_markdown(payload)
    target.write_text(text, encoding="utf-8")
    if archive_dir:
        archive = ensure_parent(Path(archive_dir) / f"{date.today().isoformat()}_path_validation_report.md")
        archive.write_text(text, encoding="utf-8")
    return target


def build_distribution_markdown(payload: dict[str, Any]) -> str:
    q = payload.get("path_quality", {})
    lines = [
        "# CNSV V1.3 路径分布报告",
        "",
        "本报告只展示路径分布观察，不生成交易信号、不输出买入/卖出建议、不输出仓位或止盈止损。",
        "",
        "## 路径质量",
        f"- 状态: {q.get('status', 'N/A')}",
        f"- FAIL 数量: {q.get('failed_count', 'N/A')}",
        f"- WARN 数量: {q.get('warn_count', 'N/A')}",
        "",
        "## 当前状态",
        f"- {payload.get('current_state', {})}",
        "",
        "## P0/P1/P2 路径模型",
    ]
    for model_id, model in payload.get("path_models", {}).items():
        lines += ["", f"### {model_id}", f"- 角色: {model.get('role', '路径分布模型')}"]
        for horizon, row in (model.get("horizons") or {}).items():
            lines.append(
                "- "
                f"{horizon}: path_count={row.get('path_count')}, "
                f"终点收益 P10/P50/P90={_pct(row.get('terminal_return_p10'))}/{_pct(row.get('terminal_return_p50'))}/{_pct(row.get('terminal_return_p90'))}, "
                f"最高上行 P90={_pct(row.get('max_up_return_p90'))}, "
                f"最低下行 P10={_pct(row.get('max_down_return_p10'))}, "
                f"最大回撤 P50={_pct(row.get('max_drawdown_p50'))}, "
                f"+5% 触达={_pct(row.get('touch_up_5pct_prob'))}, "
                f"-5% 下穿={_pct(row.get('touch_down_5pct_prob'))}, "
                f"fallback={row.get('fallback_used')}"
            )
            if row.get("fallback_used"):
                lines.append(f"  - fallback_reason: {row.get('fallback_reason')}; source_model: {row.get('source_model')}")
    lines += _guardrail_lines(payload)
    return "\n".join(lines) + "\n"


def build_validation_markdown(payload: dict[str, Any]) -> str:
    q = payload.get("path_validation_quality", {})
    lines = [
        "# CNSV V1.3 路径验证报告",
        "",
        "本报告验证路径分布的历史覆盖、触达概率和防未来函数，不生成交易信号。",
        "",
        "## 验证质量",
        f"- 状态: {q.get('status', 'N/A')}",
        f"- FAIL 数量: {q.get('failed_count', 'N/A')}",
        f"- WARN 数量: {q.get('warn_count', 'N/A')}",
        "",
        "## 防未来函数",
    ]
    leak = payload.get("path_leakage_checks", {})
    lines += [
        f"- 状态: {leak.get('status', 'N/A')}",
        f"- 检查次数: {leak.get('check_count', 'N/A')}",
        f"- purged 模式: {leak.get('purged_sample_mode', 'N/A')}",
        "",
        "## Standard Walk-forward 指标",
    ]
    lines += _validation_metric_lines(payload.get("standard_walk_forward_metrics", {}))
    lines += ["", "## Purged Walk-forward 指标"]
    lines += _validation_metric_lines(payload.get("purged_walk_forward_metrics", {}))
    lines += ["", "## P2 vs P1"]
    for mode, horizons in payload.get("p2_vs_p1", {}).items():
        lines += ["", f"### {mode}"]
        for horizon, row in horizons.items():
            lines.append(f"- {horizon}: conclusion={row.get('P2_vs_P1_conclusion')}, rmse_delta={_num(row.get('P2_vs_P1_terminal_rmse_delta'))}, fallback_rate={_pct(row.get('P2_vs_P1_fallback_rate'))}")
    lines += _guardrail_lines(payload)
    return "\n".join(lines) + "\n"


def _validation_metric_lines(metrics: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for model_id, horizons in metrics.items():
        lines += ["", f"### {model_id}"]
        for horizon, row in horizons.items():
            lines.append(
                "- "
                f"{horizon}: sample={row.get('sample_size')}, "
                f"terminal_coverage={_pct(row.get('terminal_p10_p90_coverage'))}, "
                f"up_coverage={_pct(row.get('max_up_p10_p90_coverage'))}, "
                f"down_coverage={_pct(row.get('max_down_p10_p90_coverage'))}, "
                f"+5% brier={_num(row.get('touch_up_5pct_brier'))}, "
                f"-5% brier={_num(row.get('touch_down_5pct_brier'))}, "
                f"terminal_rmse={_num(row.get('path_rmse_terminal'))}, "
                f"fallback_rate={_pct(row.get('fallback_rate'))}"
            )
    return lines


def _guardrail_lines(payload: dict[str, Any]) -> list[str]:
    return [
        "",
        "## 禁止动作",
        "- 正式交易信号: NO",
        "- 买入/卖出建议: NO",
        "- 目标仓位/目标股数: NO",
        "- 止盈止损: NO",
        f"- forbidden_actions: {', '.join(payload.get('forbidden_actions', []))}",
        "",
        "## 下一阶段",
        f"- {payload.get('next_stage', 'N/A')}",
        "",
        "## 生成信息",
        f"- generated_at: {payload.get('meta', {}).get('generated_at', 'N/A')}",
    ]


def _num(value: Any) -> str:
    return "N/A" if value is None else f"{float(value):.4f}"


def _pct(value: Any) -> str:
    return "N/A" if value is None else f"{float(value) * 100:.2f}%"
