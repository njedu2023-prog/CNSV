# CNSV V1.3 路径验证报告

本报告验证路径分布的历史覆盖、触达概率和防未来函数，不生成交易信号。

## 验证质量
- 状态: PASS
- FAIL 数量: 0
- WARN 数量: 0

## 防未来函数
- 状态: PASS
- 检查次数: 72
- purged 模式: every_horizon_step

## Standard Walk-forward 指标

### P0_historical_path_replay
- 5D: sample=72, terminal_coverage=75.00%, up_coverage=79.17%, down_coverage=84.72%, +5% brier=0.2211, -5% brier=0.1889, terminal_rmse=0.0747, fallback_rate=0.00%
- 10D: sample=72, terminal_coverage=76.39%, up_coverage=76.39%, down_coverage=86.11%, +5% brier=0.2495, -5% brier=0.2504, terminal_rmse=0.1161, fallback_rate=0.00%
- 20D: sample=72, terminal_coverage=75.00%, up_coverage=77.78%, down_coverage=76.39%, +5% brier=0.2351, -5% brier=0.2465, terminal_rmse=0.1373, fallback_rate=0.00%

### P1_volatility_adjusted_path
- 5D: sample=72, terminal_coverage=69.44%, up_coverage=72.22%, down_coverage=80.56%, +5% brier=0.2278, -5% brier=0.1740, terminal_rmse=0.0745, fallback_rate=0.00%
- 10D: sample=72, terminal_coverage=65.28%, up_coverage=72.22%, down_coverage=81.94%, +5% brier=0.2727, -5% brier=0.2448, terminal_rmse=0.1157, fallback_rate=0.00%
- 20D: sample=72, terminal_coverage=66.67%, up_coverage=72.22%, down_coverage=76.39%, +5% brier=0.2624, -5% brier=0.2513, terminal_rmse=0.1368, fallback_rate=0.00%

### P2_state_conditional_path
- 5D: sample=72, terminal_coverage=72.22%, up_coverage=72.22%, down_coverage=80.56%, +5% brier=0.2375, -5% brier=0.1853, terminal_rmse=0.0761, fallback_rate=31.94%
- 10D: sample=72, terminal_coverage=69.44%, up_coverage=69.44%, down_coverage=79.17%, +5% brier=0.2785, -5% brier=0.2295, terminal_rmse=0.1166, fallback_rate=31.94%
- 20D: sample=72, terminal_coverage=69.44%, up_coverage=69.44%, down_coverage=70.83%, +5% brier=0.2527, -5% brier=0.2355, terminal_rmse=0.1369, fallback_rate=31.94%

## Purged Walk-forward 指标

### P0_historical_path_replay
- 5D: sample=15, terminal_coverage=73.33%, up_coverage=80.00%, down_coverage=93.33%, +5% brier=0.2328, -5% brier=0.1643, terminal_rmse=0.0765, fallback_rate=0.00%
- 10D: sample=8, terminal_coverage=75.00%, up_coverage=75.00%, down_coverage=100.00%, +5% brier=0.2386, -5% brier=0.2726, terminal_rmse=0.0895, fallback_rate=0.00%
- 20D: sample=4, terminal_coverage=75.00%, up_coverage=75.00%, down_coverage=100.00%, +5% brier=0.1762, -5% brier=0.2891, terminal_rmse=0.1097, fallback_rate=0.00%

### P1_volatility_adjusted_path
- 5D: sample=15, terminal_coverage=60.00%, up_coverage=80.00%, down_coverage=80.00%, +5% brier=0.2320, -5% brier=0.1708, terminal_rmse=0.0763, fallback_rate=0.00%
- 10D: sample=8, terminal_coverage=75.00%, up_coverage=75.00%, down_coverage=87.50%, +5% brier=0.2669, -5% brier=0.3068, terminal_rmse=0.0900, fallback_rate=0.00%
- 20D: sample=4, terminal_coverage=75.00%, up_coverage=75.00%, down_coverage=100.00%, +5% brier=0.2229, -5% brier=0.3082, terminal_rmse=0.1098, fallback_rate=0.00%

### P2_state_conditional_path
- 5D: sample=15, terminal_coverage=73.33%, up_coverage=73.33%, down_coverage=86.67%, +5% brier=0.2526, -5% brier=0.1671, terminal_rmse=0.0763, fallback_rate=20.00%
- 10D: sample=8, terminal_coverage=75.00%, up_coverage=75.00%, down_coverage=87.50%, +5% brier=0.2619, -5% brier=0.2541, terminal_rmse=0.0878, fallback_rate=25.00%
- 20D: sample=4, terminal_coverage=100.00%, up_coverage=75.00%, down_coverage=100.00%, +5% brier=0.1469, -5% brier=0.2711, terminal_rmse=0.1172, fallback_rate=50.00%

## P2 vs P1

### standard_walk_forward_metrics
- 5D: conclusion=P2 underperforms P1, rmse_delta=0.0016, fallback_rate=31.94%
- 10D: conclusion=neutral, rmse_delta=0.0009, fallback_rate=31.94%
- 20D: conclusion=neutral, rmse_delta=0.0000, fallback_rate=31.94%

### purged_walk_forward_metrics
- 5D: conclusion=neutral, rmse_delta=0.0000, fallback_rate=20.00%
- 10D: conclusion=P2 improves P1, rmse_delta=-0.0023, fallback_rate=25.00%
- 20D: conclusion=P2 underperforms P1, rmse_delta=0.0074, fallback_rate=50.00%

## 禁止动作
- 正式交易信号: NO
- 买入/卖出建议: NO
- 目标仓位/目标股数: NO
- 止盈止损: NO
- forbidden_actions: formal_signal_generation, auto_order, broker_api

## 下一阶段
- V1.4 observation backtest after path validation acceptance

## 生成信息
- generated_at: 2026-06-20T15:19:18.518267+00:00
