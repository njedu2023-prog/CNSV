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
- 5D: path_count=3863, 终点收益 P10/P50/P90=-6.68%/-0.17%/7.43%, 最高上行 P90=10.95%, 最低下行 P10=-9.16%, 最大回撤 P50=-3.08%, +5% 触达=32.88%, -5% 下穿=29.87%, fallback=False
- 10D: path_count=3858, 终点收益 P10/P50/P90=-9.65%/-0.39%/10.85%, 最高上行 P90=15.94%, 最低下行 P10=-13.12%, 最大回撤 P50=-5.51%, +5% 触达=47.15%, -5% 下穿=45.80%, fallback=False
- 20D: path_count=3848, 终点收益 P10/P50/P90=-13.85%/-0.34%/15.29%, 最高上行 P90=23.90%, 最低下行 P10=-18.14%, 最大回撤 P50=-8.56%, +5% 触达=60.37%, -5% 下穿=60.03%, fallback=False

### P1_volatility_adjusted_path
- 角色: 路径分布模型
- 5D: path_count=3863, 终点收益 P10/P50/P90=-7.51%/-0.19%/8.35%, 最高上行 P90=12.31%, 最低下行 P10=-10.30%, 最大回撤 P50=-3.45%, +5% 触达=37.51%, -5% 下穿=34.56%, fallback=False
- 10D: path_count=3858, 终点收益 P10/P50/P90=-10.86%/-0.44%/12.20%, 最高上行 P90=17.93%, 最低下行 P10=-14.75%, 最大回撤 P50=-6.15%, +5% 触达=51.66%, -5% 下穿=50.60%, fallback=False
- 20D: path_count=3848, 终点收益 P10/P50/P90=-15.58%/-0.38%/17.20%, 最高上行 P90=26.87%, 最低下行 P10=-20.40%, 最大回撤 P50=-9.57%, +5% 触达=63.90%, -5% 下穿=63.88%, fallback=False

### P2_state_conditional_path
- 角色: 辅助状态层，不作为核心依赖
- 5D: path_count=3863, 终点收益 P10/P50/P90=-7.51%/-0.19%/8.35%, 最高上行 P90=12.31%, 最低下行 P10=-10.30%, 最大回撤 P50=-3.45%, +5% 触达=37.51%, -5% 下穿=34.56%, fallback=True
  - fallback_reason: state_path_sample_size_lt_30; source_model: P1_volatility_adjusted_path
- 10D: path_count=3858, 终点收益 P10/P50/P90=-10.86%/-0.44%/12.20%, 最高上行 P90=17.93%, 最低下行 P10=-14.75%, 最大回撤 P50=-6.15%, +5% 触达=51.66%, -5% 下穿=50.60%, fallback=True
  - fallback_reason: state_path_sample_size_lt_30; source_model: P1_volatility_adjusted_path
- 20D: path_count=3848, 终点收益 P10/P50/P90=-15.58%/-0.38%/17.20%, 最高上行 P90=26.87%, 最低下行 P10=-20.40%, 最大回撤 P50=-9.57%, +5% 触达=63.90%, -5% 下穿=63.88%, fallback=True
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
- generated_at: 2026-07-30T12:25:29.550796+00:00
