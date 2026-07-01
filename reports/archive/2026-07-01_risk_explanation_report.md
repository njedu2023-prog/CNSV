# CNSV V1.6 风控解释报告

本报告是风控解释，不是交易信号；不构成方向性操作建议，不输出交易执行参数或自动交易动作。

## 阶段说明
- 版本: 1.6
- 阶段: V1.6_risk_explanation
- latest_trade_date: 2026-07-01
- 质量状态: WARN
- FAIL 数量: 0
- WARN 数量: 2

## 上游证据可用性
- 全部必需证据可用: True
- 可用证据: data_report, feature_report, baseline_model_report, baseline_validation_report, path_distribution_report, path_validation_report, observation_backtest_report, human_decision_support_report
- 缺失证据: 无

## 风险总览
- 总体风险等级: high
- 风险置信度: medium
- 主要风险来源: path_distribution_risk, p2_auxiliary_risk, evidence_conflict_risk
- 次要风险来源: data_risk, feature_risk, baseline_model_risk, path_validation_risk, observation_backtest_risk, decision_support_risk, system_boundary_risk
- 需要人工复核: True
- 风险原因: 风险等级由数据、特征、模型、路径、回测和人工辅助证据综合得到，仅用于人工复核。

## 风险来源拆解
- data_risk: low；数据门禁、数据新鲜度与 manifest 一致性需要人工确认。
- feature_risk: low；趋势、波动率、资金流状态共同决定特征风险；unknown 状态需要降级复核。
- baseline_model_risk: medium；基准模型分布与验证结果用于识别 B 模型之间的方向分歧。
- path_distribution_risk: high；路径下穿概率、最大回撤与路径波动率共同构成路径分布风险。
- path_validation_risk: low；路径验证质量用于判断路径分布证据是否需要降级。
- observation_backtest_risk: medium；观察级回测只提供历史观察证据，purged 样本偏少时需要提高复核强度。
- decision_support_risk: medium；V1.5 WARN 代表人工复核要求，不是阻断错误，但需要在 V1.6 明确解释。
- p2_auxiliary_risk: high；P2 是辅助状态层，状态样本空间可能碎片化，不能作为核心依赖。
- evidence_conflict_risk: high；多模型证据存在方向差异时必须人工复核，不得转化为交易动作。
- system_boundary_risk: low；当前阶段仅允许风险解释，禁止正式交易信号、自动交易和外部执行接口。

## 数据风险解释
- risk_level: low
- data_freshness_risk: medium；需要确认最新交易日是否仍然有效。
- data_gate_risk: low；CNSVdata gate 必须保持可用。
- missing_data_risk: low；缺失报告会导致 V1.6 降级解释。
- quality_check_risk: low；数据质量检查用于确认基础输入完整性。
- manifest_consistency_risk: low；manifest 与报告快照需人工抽查。

## 特征风险解释
- risk_level: low
- trend_state_risk: medium；趋势状态为 downtrend，需要结合路径风险复核。
- volatility_state_risk: medium；波动率状态为 high_vol。
- flow_strength_basic_risk: low；资金流强弱状态为 positive。
- moneyflow_reliability_risk: medium；moneyflow 只能作为强因子观察，不是单独结论。
- feature_unknown_risk: low；unknown 状态会降低风险解释置信度。
- feature_conflict_risk: low；趋势与资金流可能出现解释冲突。

## 基准模型风险解释
- risk_level: medium
- baseline_distribution_risk: medium；基准分布仅为历史/状态分布观察。
- B1_B3_conflict_risk: medium；B1 与 B3 分布方向差异需要人工复核。
- B2_state_sample_risk: medium；B2 最小状态样本数为 79。
- positive_prob_calibration_risk: medium；正向概率校准只能用于观察，不代表确定结果。
- quantile_coverage_risk: low；分位覆盖需要结合验证层。

## 路径风险解释
- risk_level: high
- downside_path_risk: high；20D 下行路径概率需要人工复核。
- touch_down_risk: high；20D touch_down_5pct_prob=0.5602。
- max_drawdown_risk: medium；20D max_drawdown_p50=-0.0772。
- path_volatility_risk: medium；路径波动率放大时需要额外复核。
- terminal_distribution_risk: medium；终端分布为历史路径观察，不代表未来承诺。

## 观察级回测风险解释
- risk_level: medium
- observation_backtest_evidence_risk: medium；观察级回测不是正式回测引擎。
- bucket_stability_risk: medium；分桶稳定性需要结合 condition quality。
- purged_sample_risk: medium；purged_sample_size=81。
- condition_effectiveness_risk: medium；条件有效性仅支持观察复核。
- P1_vs_P0_risk: medium；P1 相对 P0 表现偏弱时需要复核。
- P2_vs_P1_risk: medium；P2 为辅助层，不作为核心比较结论。

## 人工辅助证据风险解释
- risk_level: high
- evidence_strength_risk: medium；evidence_strength=moderate
- model_consistency_risk: medium；model_consistency_level=mostly_consistent
- evidence_conflict_risk: high；V1.5 证据冲突必须进入风险解释。
- human_review_required_risk: medium；人工复核为风险控制要求。
- attention_item_risk: medium；人工关注点需要逐条复核。

## P2 辅助层风险解释
- p2_auxiliary_risk_level: high
- p2_fallback_risk: high；P2 max_fallback_rate=0.3194。
- p2_state_sample_risk: medium；P2 min_state_sample_size=79。
- p2_state_space_fragmentation_risk: medium；状态空间分组容易碎片化，需要避免核心依赖。
- p2_core_dependency_forbidden: True
- p2_role: 辅助状态层，不作为核心决策依赖

## 证据冲突风险解释
- risk_level: high
- evidence_conflict: True
- risk_reason: 证据冲突需要人工复核，不得转化为交易动作。
- risk_evidence: 上行触达概率与下行触达概率同时偏高，路径机会与风险并存。, 20D P1 相对 P0 表现偏弱。, P2 fallback_rate 偏高，P2 只能作为辅助观察。
- source_reports: latest_human_decision_support_report.json
- human_review_required: True

## 风险情景卡片
- [downside_touch_risk_card] 下穿路径风险: high；下穿概率升高时，风险解释层要求人工复核路径尾部。
- [max_drawdown_risk_card] 最大回撤风险: medium；历史路径回撤仅表示观察风险，不构成执行参数。
- [model_conflict_risk_card] 模型分歧风险: high；模型分歧表示证据不一致，需要人工复核。
- [p2_instability_risk_card] P2 辅助层不稳定风险: high；P2 只作为辅助状态层，禁止作为核心依赖。
- [data_quality_risk_card] 数据质量风险: low；数据缺失或门禁异常时，风险解释必须降级。
- [evidence_insufficiency_risk_card] 证据不足风险: low；上游证据缺失时不得输出高置信解释。

## 风险复核清单
- [check_data_freshness] 确认 latest_trade_date 与人工复核日期是否匹配。
- [check_feature_unknown] 复核趋势、波动率、资金流状态是否存在 unknown 或降级。
- [check_model_conflict] 复核 B1/B3、P0/P1/P2 之间的方向差异。
- [check_path_downside] 复核 20D 下穿概率与路径尾部风险。
- [check_drawdown_exposure] 复核历史最大回撤分布与当前波动状态。
- [check_touch_down_risk] 复核 touch_down 概率在观察级回测中的有效性。
- [check_p2_fallback] 复核 P2 fallback_rate 与状态样本覆盖。
- [check_purged_sample_size] 复核 purged 样本量是否足以支撑观察结论。
- [check_evidence_conflict] 复核证据冲突来源，不得转化为操作动作。
- [check_human_review_required] 确认所有人工复核项已逐条记录。

## 禁止交易信号声明
- 正式交易信号: NO
- 方向性操作建议: NO
- 交易执行参数: NO
- 自动交易动作: NO
- forbidden_actions: formal_signal_generation, auto_order, broker_api

## 是否允许进入 V2.0
- next_stage: V2.0 live manual decision system
- V2.0 前置准备: allowed_for_preparation_only_after_human_review
