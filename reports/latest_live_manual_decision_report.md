# CNSV V2.0 实盘人工决策系统报告

本系统是人工量化驾驶舱，不是自动交易系统；系统只展示证据、风险、复核流程和人工确认状态。

## 阶段说明
- 版本: 2.0
- 阶段: V2.0_live_manual_decision_system
- latest_trade_date: 2026-06-29
- 质量状态: WARN
- FAIL 数量: 0
- WARN 数量: 4

## 上游证据
- 证据完整: True
- 可用证据: data_report, feature_report, baseline_model_report, baseline_validation_report, path_distribution_report, path_validation_report, observation_backtest_report, human_decision_support_report, risk_explanation_report
- 缺失证据: 无
- FAIL 门禁: 0
- WARN 门禁: 2

## 当前系统状态
- overall_system_status: ready_for_manual_review
- manual_decision_status: review_required
- manual_review_required: True

## 路径观察摘要
- terminal_distribution_summary: {}
- touch_down_summary: {'5D': {'touch_down_5pct_prob': 0.23255208333333333}, '10D': {'touch_down_5pct_prob': 0.3833116036505867}, '20D': {'touch_down_5pct_prob': 0.5377777777777778}}
- drawdown_summary: {'5D': {'max_drawdown_p50': -0.025637097132967746, 'max_drawdown_p90': -0.0073237892032969164}, '10D': {'max_drawdown_p50': -0.0460109123218545, 'max_drawdown_p90': -0.018131560819731395}, '20D': {'max_drawdown_p50': -0.07174125852125945, 'max_drawdown_p90': -0.0336295784050094}}

## 风险解释摘要
- overall_risk_level: high
- primary_risk_sources: p2_auxiliary_risk, evidence_conflict_risk
- secondary_risk_sources: data_risk, feature_risk, baseline_model_risk, path_distribution_risk, path_validation_risk, observation_backtest_risk, decision_support_risk, system_boundary_risk

## 证据冲突摘要
- evidence_conflict: True
- conflict_reasons: 上行触达概率与下行触达概率同时偏高，路径机会与风险并存。, 20D P1 相对 P0 表现偏弱。, P2 fallback_rate 偏高，P2 只能作为辅助观察。

## 人工复核清单
- [check_data_freshness] 确认数据新鲜度与最新交易日。
- [check_latest_trade_date] 确认所有上游报告 latest_trade_date 一致。
- [check_path_downside] 复核路径下穿概率与尾部路径风险。
- [check_drawdown_exposure] 复核最大回撤分布与当前波动状态。
- [check_model_conflict] 复核 B/P 模型之间的证据分歧。
- [check_p2_fallback] 确认 P2 仅为辅助层并复核 fallback 风险。
- [check_evidence_conflict] 复核证据冲突原因。
- [check_risk_level] 确认总体风险等级与主要风险来源。
- [check_manual_notes] 填写人工复核备注。
- [confirm_no_auto_order] 确认系统不执行自动交易动作。
- [check_feature_unknown] 复核趋势、波动率、资金流状态是否存在 unknown 或降级。
- [check_touch_down_risk] 复核 touch_down 概率在观察级回测中的有效性。
- [check_purged_sample_size] 复核 purged 样本量是否足以支撑观察结论。
- [check_human_review_required] 确认所有人工复核项已逐条记录。

## 人工确认区
- decision_session_id: manual-2026-06-29-20260629171656
- decision_snapshot_id: live-2026-06-29-9reports
- manual_review_status: not_started

## 禁止自动交易声明
- is_trade_signal: false
- auto_order_enabled: false
- broker_api_enabled: false
- formal_signal_enabled: false
- forbidden_actions: formal_signal_generation, auto_order, broker_api

## 每日人工使用状态
- 可进入人工复核: True
- 不可使用原因: 无阻断，仅需人工复核
