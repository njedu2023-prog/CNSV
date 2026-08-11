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
- 最新交易日: 2026-08-11
- 最新收盘价: 33.9700
- 趋势状态: downtrend
- 波动率状态: normal_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0728, p50=0.0000, p90=0.0728, p10_price=31.5844, p50_price=33.9700, p90_price=36.5358, sample=3871, fallback=N/A
- 10D: p10=-0.1030, p50=0.0000, p90=0.1030, p10_price=30.6460, p50_price=33.9700, p90_price=37.6545, sample=3866, fallback=N/A
- 20D: p10=-0.1456, p50=0.0000, p90=0.1456, p10_price=29.3664, p50_price=33.9700, p90_price=39.2953, sample=3856, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0716, p10_price=31.7042, p50_price=33.9147, p90_price=36.4917, sample=3871, fallback=N/A
- 10D: p10=-0.1013, p50=-0.0036, p90=0.1029, p10_price=30.6959, p50_price=33.8465, p90_price=37.6530, sample=3866, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0035, p90=0.1421, p10_price=29.2654, p50_price=33.8523, p90_price=39.1566, sample=3856, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0674, p50=-0.0109, p90=0.0709, p10_price=31.7545, p50_price=33.6023, p90_price=36.4664, sample=199, fallback=NO
- 10D: p10=-0.1089, p50=-0.0095, p90=0.0880, p10_price=30.4649, p50_price=33.6503, p90_price=37.0964, sample=199, fallback=NO
- 20D: p10=-0.1327, p50=-0.0134, p90=0.1101, p10_price=29.7497, p50_price=33.5171, p90_price=37.9223, sample=199, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0570, p50=-0.0010, p90=0.0549, p10_price=32.0884, p50_price=33.9352, p90_price=35.8884, sample=3871, fallback=N/A
- 10D: p10=-0.0818, p50=-0.0021, p90=0.0777, p10_price=31.3011, p50_price=33.8999, p90_price=36.7144, sample=3866, fallback=N/A
- 20D: p10=-0.1168, p50=-0.0042, p90=0.1084, p10_price=30.2265, p50_price=33.8283, p90_price=37.8592, sample=3856, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-11T12:24:43.485927+00:00
- 数据快照: cnsvdata-2026-08-11-78f964830794
