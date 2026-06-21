from __future__ import annotations

from typing import Any

from cnsv.trading.utils import get_path, pct, safe_float


def compute_exit_plan(reports: dict[str, Any], distribution: dict[str, Any], risk: dict[str, Any]) -> dict[str, Any]:
    path = reports.get("path_distribution_report") or {}
    p2_5d = get_path(path, "path_models", "P2_state_conditional_path", "horizons", "5D", default={})
    p2_10d = get_path(path, "path_models", "P2_state_conditional_path", "horizons", "10D", default={})
    up_5d = safe_float(p2_5d.get("max_up_return_p90"), safe_float(p2_5d.get("terminal_return_p90"), 0.06))
    up_10d = safe_float(p2_10d.get("max_up_return_p90"), safe_float(p2_10d.get("terminal_return_p90"), 0.09))
    p10_1d = safe_float(distribution.get("p10_return_1d"), -0.03)
    stop = -0.02 if risk.get("risk_level") in {"MEDIUM_HIGH", "HIGH"} else max(-0.04, min(-0.025, p10_1d))
    return {
        "take_profit_range": f"{pct(max(0.03, up_5d * 0.7), 1)}~{pct(max(0.05, up_10d * 0.7), 1)}",
        "stop_loss_reference": pct(stop, 1),
        "time_exit_days": 10,
        "signal_exit_rule": "若信号降级为 SELL 或 STRONG_SELL，应重新评估并降低仓位。",
        "risk_exit_rule": "若风控转为高风险或大跌概率显著上升，应优先保护本金。",
    }
