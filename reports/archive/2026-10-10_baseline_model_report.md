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
- 最新交易日: 2026-10-09
- 最新收盘价: 38.5400
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0686, p50=0.0000, p90=0.0686, p10_price=35.9831, p50_price=38.5400, p90_price=41.2786, sample=3908, fallback=N/A
- 10D: p10=-0.0971, p50=0.0000, p90=0.0971, p10_price=34.9743, p50_price=38.5400, p90_price=42.4692, sample=3903, fallback=N/A
- 20D: p10=-0.1373, p50=0.0000, p90=0.1373, p10_price=33.5958, p50_price=38.5400, p90_price=44.2118, sample=3893, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0688, p50=-0.0016, p90=0.0717, p10_price=35.9785, p50_price=38.4779, p90_price=41.4056, sample=3908, fallback=N/A
- 10D: p10=-0.1006, p50=-0.0036, p90=0.1038, p10_price=34.8529, p50_price=38.4016, p90_price=42.7539, sample=3903, fallback=N/A
- 20D: p10=-0.1488, p50=-0.0026, p90=0.1433, p10_price=33.2120, p50_price=38.4401, p90_price=44.4765, sample=3893, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0803, p50=-0.0040, p90=0.0846, p10_price=35.5676, p50_price=38.3859, p90_price=41.9429, sample=175, fallback=NO
- 10D: p10=-0.1168, p50=-0.0059, p90=0.1185, p10_price=34.2898, p50_price=38.3117, p90_price=43.3904, sample=175, fallback=NO
- 20D: p10=-0.1564, p50=0.0047, p90=0.1546, p10_price=32.9587, p50_price=38.7231, p90_price=44.9834, sample=175, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0923, p50=-0.0009, p90=0.0906, p10_price=35.1403, p50_price=38.5065, p90_price=42.1951, sample=3908, fallback=N/A
- 10D: p10=-0.1321, p50=-0.0017, p90=0.1286, p10_price=33.7721, p50_price=38.4729, p90_price=43.8280, sample=3903, fallback=N/A
- 20D: p10=-0.1874, p50=-0.0034, p90=0.1805, p10_price=31.9545, p50_price=38.4079, p90_price=46.1646, sample=3893, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-10-10T15:54:32.335065+00:00
- 数据快照: cnsvdata-2026-10-09-40921c8e48c9
