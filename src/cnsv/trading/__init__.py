from __future__ import annotations

TRADING_VERSION = "CNSV_V3.0"
TRADING_STAGE = "V3.0_trading_decision_system"
TRADING_REPORT_TYPE = "trading_decision_report"

ALLOWED_SIGNALS = {
    "STRONG_BUY",
    "BUY",
    "HOLD",
    "WATCH",
    "REDUCE",
    "SELL",
    "STRONG_SELL",
    "BLOCKED",
}

FORBIDDEN_TRADING_AUTOMATION = [
    "auto_order",
    "broker_api",
    "direct_execution",
]

__all__ = [
    "TRADING_VERSION",
    "TRADING_STAGE",
    "TRADING_REPORT_TYPE",
    "ALLOWED_SIGNALS",
    "FORBIDDEN_TRADING_AUTOMATION",
]
