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
- 检查次数: 722
- 规则: training data must be <= as_of_date
- 重叠样本说明: 20D validation includes overlapping samples; purged metrics use every_horizon_step.

## 模型指标

### B0_random_walk
- 5D: sample=722, coverage=81.16%, brier=N/A, directional_accuracy=48.61%, fallback_rate=0.00%
- 10D: sample=722, coverage=78.81%, brier=N/A, directional_accuracy=46.54%, fallback_rate=0.00%
- 20D: sample=722, coverage=79.09%, brier=N/A, directional_accuracy=49.03%, fallback_rate=0.00%

### B1_historical_distribution
- 5D: sample=722, coverage=80.61%, brier=0.2504, directional_accuracy=51.39%, fallback_rate=0.00%
- 10D: sample=722, coverage=80.75%, brier=0.2503, directional_accuracy=52.91%, fallback_rate=0.00%
- 20D: sample=722, coverage=79.64%, brier=0.2531, directional_accuracy=49.86%, fallback_rate=0.00%

### B2_state_grouped_distribution
- 5D: sample=722, coverage=78.12%, brier=0.2507, directional_accuracy=50.83%, fallback_rate=30.75%
- 10D: sample=722, coverage=77.98%, brier=0.2542, directional_accuracy=51.52%, fallback_rate=31.02%
- 20D: sample=722, coverage=77.15%, brier=0.2600, directional_accuracy=46.68%, fallback_rate=31.44%

### B3_volatility_adjusted
- 5D: sample=722, coverage=80.75%, brier=N/A, directional_accuracy=50.83%, fallback_rate=0.00%
- 10D: sample=722, coverage=78.39%, brier=N/A, directional_accuracy=53.19%, fallback_rate=0.00%
- 20D: sample=722, coverage=76.04%, brier=N/A, directional_accuracy=50.00%, fallback_rate=0.00%

## B2 vs B1

### standard_walk_forward_metrics
- 10D: conclusion=B2 underperforms B1, coverage_delta=-0.0277, brier_delta=0.0039, pinball_delta=0.0004
- 20D: conclusion=B2 underperforms B1, coverage_delta=-0.0249, brier_delta=0.0070, pinball_delta=0.0012
- 5D: conclusion=B2 underperforms B1, coverage_delta=-0.0249, brier_delta=0.0003, pinball_delta=0.0001

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
- generated_at: 2026-08-27T21:05:29.043094+00:00
