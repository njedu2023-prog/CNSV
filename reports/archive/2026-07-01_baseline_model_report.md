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
- 最新交易日: 2026-07-01
- 最新收盘价: 35.1900
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0745, p50=0.0000, p90=0.0745, p10_price=32.6622, p50_price=35.1900, p90_price=37.9134, sample=3842, fallback=N/A
- 10D: p10=-0.1054, p50=0.0000, p90=0.1054, p10_price=31.6691, p50_price=35.1900, p90_price=39.1023, sample=3837, fallback=N/A
- 20D: p10=-0.1491, p50=0.0000, p90=0.1491, p10_price=30.3160, p50_price=35.1900, p90_price=40.8476, sample=3827, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0716, p10_price=32.8433, p50_price=35.1312, p90_price=37.8018, sample=3842, fallback=N/A
- 10D: p10=-0.1012, p50=-0.0038, p90=0.1032, p10_price=31.8044, p50_price=35.0548, p90_price=39.0159, sample=3837, fallback=N/A
- 20D: p10=-0.1493, p50=-0.0032, p90=0.1430, p10_price=30.3083, p50_price=35.0767, p90_price=40.6007, sample=3827, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0647, p50=0.0004, p90=0.0666, p10_price=32.9844, p50_price=35.2036, p90_price=37.6134, sample=79, fallback=NO
- 10D: p10=-0.1015, p50=0.0048, p90=0.0951, p10_price=31.7939, p50_price=35.3606, p90_price=38.6996, sample=79, fallback=NO
- 20D: p10=-0.1390, p50=0.0042, p90=0.1189, p10_price=30.6230, p50_price=35.3381, p90_price=39.6345, sample=79, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0781, p50=-0.0011, p90=0.0760, p10_price=32.5470, p50_price=35.1531, p90_price=37.9678, sample=3842, fallback=N/A
- 10D: p10=-0.1120, p50=-0.0020, p90=0.1079, p10_price=31.4628, p50_price=35.1181, p90_price=39.1980, sample=3837, fallback=N/A
- 20D: p10=-0.1593, p50=-0.0040, p90=0.1513, p10_price=30.0074, p50_price=35.0494, p90_price=40.9384, sample=3827, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-01T16:25:48.250765+00:00
- 数据快照: cnsvdata-2026-07-01-11e6b47b3f70
