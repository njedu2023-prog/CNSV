# CNSV V1.3 路径验证报告

本报告验证路径分布的历史覆盖、触达概率和防未来函数，不生成交易信号。

## 验证质量
- 状态: PASS
- FAIL 数量: 0
- WARN 数量: 0

## 防未来函数
- 状态: PASS
- 检查次数: 73
- purged 模式: every_horizon_step

## Standard Walk-forward 指标

### P0_historical_path_replay
- 5D: sample=73, terminal_coverage=75.34%, up_coverage=79.45%, down_coverage=84.93%, +5% brier=0.2195, -5% brier=0.1875, terminal_rmse=0.0742, fallback_rate=0.00%
- 10D: sample=73, terminal_coverage=76.71%, up_coverage=76.71%, down_coverage=86.30%, +5% brier=0.2499, -5% brier=0.2498, terminal_rmse=0.1155, fallback_rate=0.00%
- 20D: sample=73, terminal_coverage=75.34%, up_coverage=78.08%, down_coverage=75.34%, +5% brier=0.2340, -5% brier=0.2481, terminal_rmse=0.1364, fallback_rate=0.00%

### P1_volatility_adjusted_path
- 5D: sample=73, terminal_coverage=69.86%, up_coverage=72.60%, down_coverage=80.82%, +5% brier=0.2269, -5% brier=0.1735, terminal_rmse=0.0740, fallback_rate=0.00%
- 10D: sample=73, terminal_coverage=65.75%, up_coverage=72.60%, down_coverage=80.82%, +5% brier=0.2719, -5% brier=0.2453, terminal_rmse=0.1151, fallback_rate=0.00%
- 20D: sample=73, terminal_coverage=67.12%, up_coverage=72.60%, down_coverage=75.34%, +5% brier=0.2604, -5% brier=0.2537, terminal_rmse=0.1359, fallback_rate=0.00%

### P2_state_conditional_path
- 5D: sample=73, terminal_coverage=72.60%, up_coverage=72.60%, down_coverage=80.82%, +5% brier=0.2370, -5% brier=0.1849, terminal_rmse=0.0756, fallback_rate=31.51%
- 10D: sample=73, terminal_coverage=69.86%, up_coverage=69.86%, down_coverage=78.08%, +5% brier=0.2770, -5% brier=0.2301, terminal_rmse=0.1159, fallback_rate=31.51%
- 20D: sample=73, terminal_coverage=69.86%, up_coverage=69.86%, down_coverage=69.86%, +5% brier=0.2504, -5% brier=0.2386, terminal_rmse=0.1360, fallback_rate=31.51%

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
- 5D: conclusion=P2 underperforms P1, rmse_delta=0.0016, fallback_rate=31.51%
- 10D: conclusion=neutral, rmse_delta=0.0008, fallback_rate=31.51%
- 20D: conclusion=neutral, rmse_delta=0.0001, fallback_rate=31.51%

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
- generated_at: 2026-08-28T00:10:17.243143+00:00
