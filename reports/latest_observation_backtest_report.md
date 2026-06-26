# CNSV V1.4 观察级回测报告

本报告是观察级回测，不是交易回测；不生成交易信号，不构成买卖建议，不输出仓位、目标价、止盈或止损。

## 阶段与范围
- 版本: 1.4
- 阶段: V1.4_observation_backtest
- latest_trade_date: 2026-06-26
- horizons: [5, 10, 20]
- models: P0_historical_path_replay, P1_volatility_adjusted_path, P2_state_conditional_path
- standard walk-forward 样本数: 648
- purged walk-forward 样本数: 81

## 质量门禁
- 状态: PASS
- FAIL 数量: 0
- WARN 数量: 0

## 模型指标总览

### P0_historical_path_replay
- 5D: sample=72, positive=56.94%, mean_return=1.18%, +5%=33.33%, -5%=25.00%, drawdown_p90=-1.08%, fallback=0.00%
- 10D: sample=72, positive=44.44%, mean_return=0.59%, +5%=47.22%, -5%=45.83%, drawdown_p90=-1.93%, fallback=0.00%
- 20D: sample=72, positive=55.56%, mean_return=1.33%, +5%=63.89%, -5%=58.33%, drawdown_p90=-4.51%, fallback=0.00%

### P1_volatility_adjusted_path
- 5D: sample=72, positive=56.94%, mean_return=1.18%, +5%=33.33%, -5%=25.00%, drawdown_p90=-1.08%, fallback=0.00%
- 10D: sample=72, positive=44.44%, mean_return=0.59%, +5%=47.22%, -5%=45.83%, drawdown_p90=-1.93%, fallback=0.00%
- 20D: sample=72, positive=55.56%, mean_return=1.33%, +5%=63.89%, -5%=58.33%, drawdown_p90=-4.51%, fallback=0.00%

### P2_state_conditional_path
- 5D: sample=72, positive=56.94%, mean_return=1.18%, +5%=33.33%, -5%=25.00%, drawdown_p90=-1.08%, fallback=31.94%
- 10D: sample=72, positive=44.44%, mean_return=0.59%, +5%=47.22%, -5%=45.83%, drawdown_p90=-1.93%, fallback=31.94%
- 20D: sample=72, positive=55.56%, mean_return=1.33%, +5%=63.89%, -5%=58.33%, drawdown_p90=-4.51%, fallback=31.94%

## Purged Walk-forward

### P0_historical_path_replay
- 5D: sample=15, positive=60.00%, mean_return=1.86%, +5%=33.33%, -5%=20.00%, drawdown_p90=-0.77%, fallback=0.00%
- 10D: sample=8, positive=37.50%, mean_return=-0.87%, +5%=50.00%, -5%=62.50%, drawdown_p90=-4.27%, fallback=0.00%
- 20D: sample=4, positive=100.00%, mean_return=9.28%, +5%=100.00%, -5%=50.00%, drawdown_p90=-3.72%, fallback=0.00%

### P1_volatility_adjusted_path
- 5D: sample=15, positive=60.00%, mean_return=1.86%, +5%=33.33%, -5%=20.00%, drawdown_p90=-0.77%, fallback=0.00%
- 10D: sample=8, positive=37.50%, mean_return=-0.87%, +5%=50.00%, -5%=62.50%, drawdown_p90=-4.27%, fallback=0.00%
- 20D: sample=4, positive=100.00%, mean_return=9.28%, +5%=100.00%, -5%=50.00%, drawdown_p90=-3.72%, fallback=0.00%

### P2_state_conditional_path
- 5D: sample=15, positive=60.00%, mean_return=1.86%, +5%=33.33%, -5%=20.00%, drawdown_p90=-0.77%, fallback=20.00%
- 10D: sample=8, positive=37.50%, mean_return=-0.87%, +5%=50.00%, -5%=62.50%, drawdown_p90=-4.27%, fallback=25.00%
- 20D: sample=4, positive=100.00%, mean_return=9.28%, +5%=100.00%, -5%=50.00%, drawdown_p90=-3.72%, fallback=50.00%

## 触达概率分组
- 已完成 touch_up/touch_down 3%/5%/8% 的 low/mid/high 分组。

## 下穿概率分组
- 已完成 touch_down 3%/5%/8% 的分组与真实下穿率统计。

## 回撤风险分组
- 已完成 max_drawdown 与 max_down_return 分组。

## 上行路径分组
- 已完成 max_up_return、touch_up_5pct_prob、positive_terminal_prob 分组。

## P0/P1/P2 对比
- 5D: P1 is neutral versus P0; P2 is neutral versus P1; P2 is auxiliary only and must not be used as core decision dependency.
- 10D: P1 is neutral versus P0; P2 is neutral versus P1; P2 is auxiliary only and must not be used as core decision dependency.
- 20D: P1 underperforms P0; P2 is neutral versus P1; P2 is auxiliary only and must not be used as core decision dependency.

## 观察条件有效性
- neutral_observation: 8
- unstable_observation: 2
- useful_observation: 4

## 防未来函数
- 状态: PASS
- 检查次数: 72
- purged_sample_mode: every_horizon_step

## 禁止动作
- 正式交易信号: NO
- 买入/卖出建议: NO
- 目标仓位/目标股数: NO
- 止盈止损/目标价: NO
- forbidden_actions: formal_signal_generation, auto_order, broker_api

## 下一阶段
- V1.5 human decision support
