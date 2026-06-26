# CNSV V1.2 基准模型报告

本报告仅展示 5D/10D/20D 终端收益分布基准模型，不生成交易动作。

## CNSVdata 数据门禁
- 状态: PASS
- 就绪: YES
- 允许继续: YES

## 特征质量
- 状态: PASS
- FAIL 数量: 0
- WARN 数量: 0

## 基准模型质量
- 状态: PASS
- blocking_errors: 0
- gating_warnings: 0
- non_gating_warnings: 0
- fallback_count: 0

## 受控回退说明
B2 状态分组样本不足时透明回退到 B1 历史分布基准；该回退不生成正式交易信号，也不影响 V1.2 基准模型层验收状态。
- 无

## 当前状态
- 最新交易日: 2026-06-26
- 最新收盘价: 33.4000
- 趋势状态: strong_downtrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0733, p50=0.0000, p90=0.0733, p10_price=31.0398, p50_price=33.4000, p90_price=35.9396, sample=3839, fallback=N/A
- 10D: p10=-0.1036, p50=0.0000, p90=0.1036, p10_price=30.1117, p50_price=33.4000, p90_price=37.0473, sample=3834, fallback=N/A
- 20D: p10=-0.1466, p50=0.0000, p90=0.1466, p10_price=28.8464, p50_price=33.4000, p90_price=38.6724, sample=3824, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0716, p10_price=31.1744, p50_price=33.3457, p90_price=35.8796, sample=3839, fallback=N/A
- 10D: p10=-0.1012, p50=-0.0037, p90=0.1034, p10_price=30.1855, p50_price=33.2757, p90_price=37.0367, sample=3834, fallback=N/A
- 20D: p10=-0.1494, p50=-0.0030, p90=0.1430, p10_price=28.7659, p50_price=33.2996, p90_price=38.5357, sample=3824, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0729, p50=0.0005, p90=0.0675, p10_price=31.0531, p50_price=33.4175, p90_price=35.7341, sample=152, fallback=NO
- 10D: p10=-0.0898, p50=-0.0016, p90=0.0919, p10_price=30.5311, p50_price=33.3468, p90_price=36.6163, sample=152, fallback=NO
- 20D: p10=-0.1784, p50=-0.0038, p90=0.1315, p10_price=27.9439, p50_price=33.2719, p90_price=38.0924, sample=150, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0725, p50=-0.0010, p90=0.0705, p10_price=31.0641, p50_price=33.3664, p90_price=35.8393, sample=3839, fallback=N/A
- 10D: p10=-0.1041, p50=-0.0020, p90=0.1000, p10_price=30.0988, p50_price=33.3328, p90_price=36.9142, sample=3834, fallback=N/A
- 20D: p10=-0.1482, p50=-0.0039, p90=0.1403, p10_price=28.8008, p50_price=33.2684, p90_price=38.4290, sample=3824, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-06-26T16:15:27.536079+00:00
- 数据快照: cnsvdata-2026-06-26-b3d58a5c3acb
