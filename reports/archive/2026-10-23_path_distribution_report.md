# CNSV V1.3 路径分布报告

本报告只展示路径分布观察，不生成交易信号、不输出买入/卖出建议、不输出仓位或止盈止损。

## 路径质量
- 状态: PASS
- FAIL 数量: 0
- WARN 数量: 0

## 当前状态
- {'trend_state': 'strong_downtrend', 'volatility_state': 'high_vol', 'flow_strength_basic': 'positive'}

## P0/P1/P2 路径模型

### P0_historical_path_replay
- 角色: 路径分布模型
- 5D: path_count=3918, 终点收益 P10/P50/P90=-6.67%/-0.17%/7.42%, 最高上行 P90=10.93%, 最低下行 P10=-9.14%, 最大回撤 P50=-3.08%, +5% 触达=32.92%, -5% 下穿=29.73%, fallback=False
- 10D: path_count=3913, 终点收益 P10/P50/P90=-9.60%/-0.36%/10.91%, 最高上行 P90=15.96%, 最低下行 P10=-13.06%, 最大回撤 P50=-5.48%, +5% 触达=47.28%, -5% 下穿=45.62%, fallback=False
- 20D: path_count=3903, 终点收益 P10/P50/P90=-13.80%/-0.28%/15.40%, 最高上行 P90=23.85%, 最低下行 P10=-18.05%, 最大回撤 P50=-8.52%, +5% 触达=60.47%, -5% 下穿=59.80%, fallback=False

### P1_volatility_adjusted_path
- 角色: 路径分布模型
- 5D: path_count=3918, 终点收益 P10/P50/P90=-6.09%/-0.15%/6.78%, 最高上行 P90=9.97%, 最低下行 P10=-8.35%, 最大回撤 P50=-2.81%, +5% 触达=30.09%, -5% 下穿=26.29%, fallback=False
- 10D: path_count=3913, 终点收益 P10/P50/P90=-8.77%/-0.33%/9.96%, 最高上行 P90=14.56%, 最低下行 P10=-11.92%, 最大回撤 P50=-5.03%, +5% 触达=44.42%, -5% 下穿=42.04%, fallback=False
- 20D: path_count=3903, 终点收益 P10/P50/P90=-12.59%/-0.26%/14.05%, 最高上行 P90=21.77%, 最低下行 P10=-16.48%, 最大回撤 P50=-7.81%, +5% 触达=58.11%, -5% 下穿=56.57%, fallback=False

### P2_state_conditional_path
- 角色: 辅助状态层，不作为核心依赖
- 5D: path_count=3918, 终点收益 P10/P50/P90=-6.09%/-0.15%/6.78%, 最高上行 P90=9.97%, 最低下行 P10=-8.35%, 最大回撤 P50=-2.81%, +5% 触达=30.09%, -5% 下穿=26.29%, fallback=True
  - fallback_reason: state_path_sample_size_lt_30; source_model: P1_volatility_adjusted_path
- 10D: path_count=3913, 终点收益 P10/P50/P90=-8.77%/-0.33%/9.96%, 最高上行 P90=14.56%, 最低下行 P10=-11.92%, 最大回撤 P50=-5.03%, +5% 触达=44.42%, -5% 下穿=42.04%, fallback=True
  - fallback_reason: state_path_sample_size_lt_30; source_model: P1_volatility_adjusted_path
- 20D: path_count=3903, 终点收益 P10/P50/P90=-12.59%/-0.26%/14.05%, 最高上行 P90=21.77%, 最低下行 P10=-16.48%, 最大回撤 P50=-7.81%, +5% 触达=58.11%, -5% 下穿=56.57%, fallback=True
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
- generated_at: 2026-10-23T15:13:07.553953+00:00
