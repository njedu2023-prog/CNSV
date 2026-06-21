from __future__ import annotations
LIVE_VERSION="2.0"
LIVE_STAGE="V2.0_live_manual_decision_system"
LIVE_REPORT_TYPE="live_manual_decision_report"
ALLOWED_MANUAL_DECISION_STATUS={"review_required","risk_blocked","evidence_incomplete","ready_for_manual_review","manual_review_completed","no_decision_due_to_risk"}
ALLOWED_MANUAL_REVIEW_STATUS={"not_started","in_review","completed","blocked_by_risk","blocked_by_missing_evidence"}
FORBIDDEN_LIVE_FIELDS={"buy_signal","sell_signal","target_position","target_shares","stop_loss","take_profit","target_price","broker_order","trade_command","formal_signal"}
