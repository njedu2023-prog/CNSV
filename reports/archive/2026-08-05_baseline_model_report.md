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
- 最新交易日: 2026-08-05
- 最新收盘价: 35.2000
- 趋势状态: strong_uptrend
- 波动率状态: high_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0777, p50=0.0000, p90=0.0777, p10_price=32.5679, p50_price=35.2000, p90_price=38.0449, sample=3867, fallback=N/A
- 10D: p10=-0.1099, p50=0.0000, p90=0.1099, p10_price=31.5361, p50_price=35.2000, p90_price=39.2896, sample=3862, fallback=N/A
- 20D: p10=-0.1554, p50=0.0000, p90=0.1554, p10_price=30.1325, p50_price=35.2000, p90_price=41.1197, sample=3852, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0016, p90=0.0716, p10_price=32.8508, p50_price=35.1427, p90_price=37.8134, sample=3867, fallback=N/A
- 10D: p10=-0.1014, p50=-0.0037, p90=0.1030, p10_price=31.8044, p50_price=35.0690, p90_price=39.0182, sample=3862, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0035, p90=0.1422, p10_price=30.3242, p50_price=35.0781, p90_price=40.5769, sample=3852, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0950, p50=-0.0028, p90=0.1064, p10_price=32.0084, p50_price=35.1008, p90_price=39.1511, sample=98, fallback=NO
- 10D: p10=-0.1161, p50=-0.0121, p90=0.1668, p10_price=31.3411, p50_price=34.7761, p90_price=41.5891, sample=98, fallback=NO
- 20D: p10=-0.1827, p50=0.0043, p90=0.2224, p10_price=29.3231, p50_price=35.3502, p90_price=43.9687, sample=97, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0781, p50=-0.0010, p90=0.0761, p10_price=32.5554, p50_price=35.1642, p90_price=37.9819, sample=3867, fallback=N/A
- 10D: p10=-0.1120, p50=-0.0021, p90=0.1077, p10_price=31.4717, p50_price=35.1260, p90_price=39.2047, sample=3862, fallback=N/A
- 20D: p10=-0.1592, p50=-0.0042, p90=0.1509, p10_price=30.0184, p50_price=35.0536, p90_price=40.9334, sample=3852, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-05T12:24:53.733996+00:00
- 数据快照: cnsvdata-2026-08-05-7d4d4e979f11
