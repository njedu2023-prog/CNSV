from __future__ import annotations


def build_human_review_checklist() -> list[dict[str, str]]:
    return [
        {"id": "data_freshness", "text": "确认 latest_trade_date 与当前人工复核日期是否匹配。"},
        {"id": "market_context", "text": "确认当天市场环境是否存在外部冲击。"},
        {"id": "industry_context", "text": "确认船舶与军工产业链是否存在重大事件。"},
        {"id": "intraday_behavior", "text": "复核分时结构与尾盘强弱是否支持当前观察。"},
        {"id": "path_risk", "text": "复核下穿概率、最大回撤与风险分组。"},
        {"id": "model_conflict", "text": "复核 B/P 模型之间的方向差异和 P2 辅助层不确定性。"},
        {"id": "evidence_quality", "text": "复核上游质量门禁、purged 样本与 fallback 情况。"},
    ]
