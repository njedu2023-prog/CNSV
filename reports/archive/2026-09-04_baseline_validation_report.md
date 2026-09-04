# CNSV V1.2.2 Baseline Validation 报告

本报告只验证 B0/B1/B2/B3 基准模型的历史分布预测质量，不生成交易信号、不输出买卖建议。

## 验证质量
- 状态: PASS
- FAIL 数量: 0
- WARN 数量: 0

## 验证范围
- 模型: B0_random_walk, B1_historical_distribution, B2_state_grouped_distribution, B3_volatility_adjusted
- 周期: [5, 10, 20]
- walk-forward: YES
- validation_step: 5
- purged 模式: every_horizon_step

## 防未来函数
- 状态: PASS
- 检查次数: 723
- 规则: training data must be <= as_of_date
- 重叠样本说明: 20D validation includes overlapping samples; purged metrics use every_horizon_step.

## 模型指标

### B0_random_walk
- 5D: sample=723, coverage=81.19%, brier=N/A, directional_accuracy=48.55%, fallback_rate=0.00%
- 10D: sample=723, coverage=78.84%, brier=N/A, directional_accuracy=46.47%, fallback_rate=0.00%
- 20D: sample=723, coverage=79.11%, brier=N/A, directional_accuracy=48.96%, fallback_rate=0.00%

### B1_historical_distribution
- 5D: sample=723, coverage=80.64%, brier=0.2504, directional_accuracy=51.45%, fallback_rate=0.00%
- 10D: sample=723, coverage=80.77%, brier=0.2503, directional_accuracy=52.97%, fallback_rate=0.00%
- 20D: sample=723, coverage=79.67%, brier=0.2530, directional_accuracy=49.93%, fallback_rate=0.00%

### B2_state_grouped_distribution
- 5D: sample=723, coverage=78.15%, brier=0.2507, directional_accuracy=50.90%, fallback_rate=30.71%
- 10D: sample=723, coverage=78.01%, brier=0.2541, directional_accuracy=51.59%, fallback_rate=30.98%
- 20D: sample=723, coverage=77.18%, brier=0.2599, directional_accuracy=46.75%, fallback_rate=31.40%

### B3_volatility_adjusted
- 5D: sample=723, coverage=80.77%, brier=N/A, directional_accuracy=50.90%, fallback_rate=0.00%
- 10D: sample=723, coverage=78.42%, brier=N/A, directional_accuracy=53.25%, fallback_rate=0.00%
- 20D: sample=723, coverage=76.07%, brier=N/A, directional_accuracy=50.07%, fallback_rate=0.00%

## B2 vs B1

### standard_walk_forward_metrics
- 10D: conclusion=B2 underperforms B1, coverage_delta=-0.0277, brier_delta=0.0038, pinball_delta=0.0004
- 20D: conclusion=B2 underperforms B1, coverage_delta=-0.0249, brier_delta=0.0068, pinball_delta=0.0012
- 5D: conclusion=B2 underperforms B1, coverage_delta=-0.0249, brier_delta=0.0002, pinball_delta=0.0001

### purged_walk_forward_metrics
- 10D: conclusion=B2 is neutral versus B1, coverage_delta=-0.0411, brier_delta=-0.0012, pinball_delta=-0.0003
- 20D: conclusion=B2 underperforms B1, coverage_delta=-0.0541, brier_delta=0.0111, pinball_delta=0.0015
- 5D: conclusion=B2 is neutral versus B1, coverage_delta=-0.0138, brier_delta=-0.0022, pinball_delta=0.0001

## 禁止动作
- 正式交易信号: NO
- 买入/卖出建议: NO
- 目标仓位/股数: NO
- forbidden_actions: formal_signal_generation, auto_order, broker_api

## 下一阶段
- V1.3 20D path distribution after validation acceptance

## 生成信息
- generated_at: 2026-09-04T14:26:32.325561+00:00
