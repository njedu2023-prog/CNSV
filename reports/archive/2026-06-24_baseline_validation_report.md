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
- 检查次数: 713
- 规则: training data must be <= as_of_date
- 重叠样本说明: 20D validation includes overlapping samples; purged metrics use every_horizon_step.

## 模型指标

### B0_random_walk
- 5D: sample=713, coverage=81.21%, brier=N/A, directional_accuracy=48.67%, fallback_rate=0.00%
- 10D: sample=713, coverage=78.68%, brier=N/A, directional_accuracy=46.56%, fallback_rate=0.00%
- 20D: sample=713, coverage=78.82%, brier=N/A, directional_accuracy=49.09%, fallback_rate=0.00%

### B1_historical_distribution
- 5D: sample=713, coverage=80.65%, brier=0.2505, directional_accuracy=51.33%, fallback_rate=0.00%
- 10D: sample=713, coverage=80.65%, brier=0.2503, directional_accuracy=52.88%, fallback_rate=0.00%
- 20D: sample=713, coverage=79.38%, brier=0.2531, directional_accuracy=49.79%, fallback_rate=0.00%

### B2_state_grouped_distribution
- 5D: sample=713, coverage=78.12%, brier=0.2508, directional_accuracy=50.63%, fallback_rate=31.14%
- 10D: sample=713, coverage=77.84%, brier=0.2545, directional_accuracy=51.19%, fallback_rate=31.42%
- 20D: sample=713, coverage=76.86%, brier=0.2603, directional_accuracy=46.42%, fallback_rate=31.84%

### B3_volatility_adjusted
- 5D: sample=713, coverage=80.79%, brier=N/A, directional_accuracy=50.77%, fallback_rate=0.00%
- 10D: sample=713, coverage=78.12%, brier=N/A, directional_accuracy=53.16%, fallback_rate=0.00%
- 20D: sample=713, coverage=75.74%, brier=N/A, directional_accuracy=49.93%, fallback_rate=0.00%

## B2 vs B1

### standard_walk_forward_metrics
- 10D: conclusion=B2 underperforms B1, coverage_delta=-0.0281, brier_delta=0.0042, pinball_delta=0.0004
- 20D: conclusion=B2 underperforms B1, coverage_delta=-0.0252, brier_delta=0.0072, pinball_delta=0.0012
- 5D: conclusion=B2 underperforms B1, coverage_delta=-0.0252, brier_delta=0.0004, pinball_delta=0.0001

### purged_walk_forward_metrics
- 10D: conclusion=B2 is neutral versus B1, coverage_delta=-0.0417, brier_delta=-0.0008, pinball_delta=-0.0002
- 20D: conclusion=B2 underperforms B1, coverage_delta=-0.0556, brier_delta=0.0100, pinball_delta=0.0013
- 5D: conclusion=B2 is neutral versus B1, coverage_delta=-0.0140, brier_delta=-0.0022, pinball_delta=0.0001

## 禁止动作
- 正式交易信号: NO
- 买入/卖出建议: NO
- 目标仓位/股数: NO
- forbidden_actions: formal_signal_generation, auto_order, broker_api

## 下一阶段
- V1.3 20D path distribution after validation acceptance

## 生成信息
- generated_at: 2026-06-24T03:52:15.909321+00:00
