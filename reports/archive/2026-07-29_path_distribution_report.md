# CNSV V1.3 路径分布报告

本报告只展示路径分布观察，不生成交易信号、不输出买入/卖出建议、不输出仓位或止盈止损。

## 路径质量
- 状态: PASS
- FAIL 数量: 0
- WARN 数量: 0

## 当前状态
- {'trend_state': 'neutral', 'volatility_state': 'high_vol', 'flow_strength_basic': 'mixed'}

## P0/P1/P2 路径模型

### P0_historical_path_replay
- 角色: 路径分布模型
- 5D: path_count=3862, 终点收益 P10/P50/P90=-6.68%/-0.17%/7.43%, 最高上行 P90=10.95%, 最低下行 P10=-9.16%, 最大回撤 P50=-3.08%, +5% 触达=32.88%, -5% 下穿=29.88%, fallback=False
- 10D: path_count=3857, 终点收益 P10/P50/P90=-9.66%/-0.39%/10.85%, 最高上行 P90=15.94%, 最低下行 P10=-13.12%, 最大回撤 P50=-5.51%, +5% 触达=47.14%, -5% 下穿=45.81%, fallback=False
- 20D: path_count=3847, 终点收益 P10/P50/P90=-13.85%/-0.34%/15.30%, 最高上行 P90=23.90%, 最低下行 P10=-18.15%, 最大回撤 P50=-8.56%, +5% 触达=60.36%, -5% 下穿=60.02%, fallback=False

### P1_volatility_adjusted_path
- 角色: 路径分布模型
- 5D: path_count=3862, 终点收益 P10/P50/P90=-7.61%/-0.19%/8.47%, 最高上行 P90=12.48%, 最低下行 P10=-10.44%, 最大回撤 P50=-3.49%, +5% 触达=38.19%, -5% 下穿=35.09%, fallback=False
- 10D: path_count=3857, 终点收益 P10/P50/P90=-11.01%/-0.45%/12.37%, 最高上行 P90=18.18%, 最低下行 P10=-14.96%, 最大回撤 P50=-6.23%, +5% 触达=52.11%, -5% 下穿=51.13%, fallback=False
- 20D: path_count=3847, 终点收益 P10/P50/P90=-15.79%/-0.39%/17.44%, 最高上行 P90=27.25%, 最低下行 P10=-20.69%, 最大回撤 P50=-9.70%, +5% 触达=64.39%, -5% 下穿=64.41%, fallback=False

### P2_state_conditional_path
- 角色: 辅助状态层，不作为核心依赖
- 5D: path_count=3862, 终点收益 P10/P50/P90=-7.61%/-0.19%/8.47%, 最高上行 P90=12.48%, 最低下行 P10=-10.44%, 最大回撤 P50=-3.49%, +5% 触达=38.19%, -5% 下穿=35.09%, fallback=True
  - fallback_reason: state_path_sample_size_lt_30; source_model: P1_volatility_adjusted_path
- 10D: path_count=3857, 终点收益 P10/P50/P90=-11.01%/-0.45%/12.37%, 最高上行 P90=18.18%, 最低下行 P10=-14.96%, 最大回撤 P50=-6.23%, +5% 触达=52.11%, -5% 下穿=51.13%, fallback=True
  - fallback_reason: state_path_sample_size_lt_30; source_model: P1_volatility_adjusted_path
- 20D: path_count=3847, 终点收益 P10/P50/P90=-15.79%/-0.39%/17.44%, 最高上行 P90=27.25%, 最低下行 P10=-20.69%, 最大回撤 P50=-9.70%, +5% 触达=64.39%, -5% 下穿=64.41%, fallback=True
  - fallback_reason: state_path_sample_size_lt_30; source_model: P1_volatility_adjusted_path

## 禁止动作
- 正式交易信号: NO
- 买入/卖出建议: NO
- 目标仓位/目标股数: NO
- 止盈止损: NO
- forbidden_actions: formal_signal_generation, auto_order, broker_api

## 下一阶段
- V1.4 observation backtest after path validation acceptance

## 生成信息
- generated_at: 2026-07-29T12:26:42.525240+00:00
