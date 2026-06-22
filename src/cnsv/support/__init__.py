from __future__ import annotations

SUPPORT_VERSION = "1.5"
SUPPORT_STAGE = "V1.5_human_decision_support"
SUPPORT_REPORT_TYPE = "human_decision_support_report"

FORBIDDEN_SUPPORT_FIELDS = {
    "buy_signal",
    "sell_signal",
    "target_position",
    "target_shares",
    "stop_loss",
    "take_profit",
    "target_price",
    "formal_signal",
    "trade_recommendation",
    "entry_level",
    "exit_level",
    "position_level",
}
