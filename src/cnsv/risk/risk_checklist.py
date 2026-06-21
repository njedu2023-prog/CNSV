from __future__ import annotations


def build_risk_review_checklist() -> list[dict[str, str]]:
    return [
        {"id": "check_data_freshness", "text": "确认 latest_trade_date 与人工复核日期是否匹配。"},
        {"id": "check_feature_unknown", "text": "复核趋势、波动率、资金流状态是否存在 unknown 或降级。"},
        {"id": "check_model_conflict", "text": "复核 B1/B3、P0/P1/P2 之间的方向差异。"},
        {"id": "check_path_downside", "text": "复核 20D 下穿概率与路径尾部风险。"},
        {"id": "check_drawdown_exposure", "text": "复核历史最大回撤分布与当前波动状态。"},
        {"id": "check_touch_down_risk", "text": "复核 touch_down 概率在观察级回测中的有效性。"},
        {"id": "check_p2_fallback", "text": "复核 P2 fallback_rate 与状态样本覆盖。"},
        {"id": "check_purged_sample_size", "text": "复核 purged 样本量是否足以支撑观察结论。"},
        {"id": "check_evidence_conflict", "text": "复核证据冲突来源，不得转化为操作动作。"},
        {"id": "check_human_review_required", "text": "确认所有人工复核项已逐条记录。"},
    ]
