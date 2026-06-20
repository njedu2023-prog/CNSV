# CNSV V1.5 人工决策辅助报告

本报告是人工决策辅助，不是交易信号；不构成方向性操作建议，不输出交易执行参数或自动交易动作。

## 阶段说明
- 版本: 1.5
- 阶段: V1.5_human_decision_support
- latest_trade_date: 2026-06-18
- 质量状态: WARN
- FAIL 数量: 0
- WARN 数量: 2

## 上游证据可用性
- 全部必需证据可用: True
- 可用证据: data_report, feature_report, baseline_model_report, baseline_validation_report, path_distribution_report, path_validation_report, observation_backtest_report
- 缺失证据: 无

## 当前状态摘要
- latest_trade_date: 2026-06-18
- latest_close: 36.14
- trend_state: downtrend
- volatility_state: normal_vol
- flow_strength_basic: mixed
- data_quality_status: PASS
- feature_quality_status: PASS
- cnsvdata_gate_status: PASS

## 模型证据摘要
- 证据强度: moderate
- 模型一致性: mostly_consistent
- P2 定位: 辅助状态层，不作为核心决策依赖

## 路径机会观察
- upside_path_observation: medium
- touch_up_observation: 0.4684472374967269
- positive_terminal_observation: 0.48939512961508247
- historical_support_level: weak
- evidence_strength: 观察项，仅供人工复核

## 路径风险观察
- downside_path_observation: 0.43309766954700185
- drawdown_observation: -0.05669567924033836
- touch_down_observation: 0.43309766954700185
- risk_evidence_level: weak
- risk_attention_level: medium

## V1.4 观察级回测支持情况
- quality_status: PASS
- standard_sample_size: 648
- purged_sample_size: 81
- leakage_status: PASS

## 模型一致性与分歧
- B1 与 B3 的 20D 中位收益方向不一致，需要人工复核。

## 证据冲突
- 是否存在证据冲突: True
- 20D P1 相对 P0 表现偏弱。
- P2 fallback_rate 偏高，P2 只能作为辅助观察。

## 支持等级
- observation_priority: high
- risk_attention_level: medium
- evidence_strength: moderate
- model_consistency_level: mostly_consistent
- human_review_required: True

## 人工关注点
- [model_items] 需要人工复核证据冲突：20D P1 相对 P0 表现偏弱。
- [model_items] 需要人工复核证据冲突：P2 fallback_rate 偏高，P2 只能作为辅助观察。
- [model_items] B1 与 B3 的 20D 中位收益方向不一致，需要人工复核。

## 人工复核清单
- [data_freshness] 确认 latest_trade_date 与当前人工复核日期是否匹配。
- [market_context] 确认当天市场环境是否存在外部冲击。
- [industry_context] 确认船舶与军工产业链是否存在重大事件。
- [intraday_behavior] 复核分时结构与尾盘强弱是否支持当前观察。
- [path_risk] 复核下穿概率、最大回撤与风险分组。
- [model_conflict] 复核 B/P 模型之间的方向差异和 P2 辅助层不确定性。
- [evidence_quality] 复核上游质量门禁、purged 样本与 fallback 情况。

## 禁止交易信号声明
- 正式交易信号: NO
- 方向性操作建议: NO
- 交易执行参数: NO
- 自动交易动作: NO
- forbidden_actions: formal_signal_generation, auto_order, broker_api

## 下一阶段
- V1.6 risk explanation
