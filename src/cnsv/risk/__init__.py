from __future__ import annotations

RISK_VERSION = "1.6"
RISK_STAGE = "V1.6_risk_explanation"
RISK_REPORT_TYPE = "risk_explanation_report"

FORBIDDEN_RISK_FIELDS = {
    "buy_signal",
    "sell_signal",
    "target_position",
    "target_shares",
    "stop_loss",
    "take_profit",
    "target_price",
    "formal_signal",
    "trade_recommendation",
    "position_level",
    "entry_level",
    "exit_level",
    "buy_level",
    "sell_level",
}

__all__ = ["RISK_VERSION", "RISK_STAGE", "RISK_REPORT_TYPE", "FORBIDDEN_RISK_FIELDS"]
