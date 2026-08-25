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
- 最新交易日: 2026-08-25
- 最新收盘价: 33.8400
- 趋势状态: downtrend
- 波动率状态: low_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0707, p50=0.0000, p90=0.0707, p10_price=31.5299, p50_price=33.8400, p90_price=36.3194, sample=3881, fallback=N/A
- 10D: p10=-0.1000, p50=0.0000, p90=0.1000, p10_price=30.6198, p50_price=33.8400, p90_price=37.3988, sample=3876, fallback=N/A
- 20D: p10=-0.1414, p50=0.0000, p90=0.1414, p10_price=29.3775, p50_price=33.8400, p90_price=38.9804, sample=3866, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0715, p10_price=31.5830, p50_price=33.7834, p90_price=36.3476, sample=3881, fallback=N/A
- 10D: p10=-0.1012, p50=-0.0039, p90=0.1029, p10_price=30.5839, p50_price=33.7087, p90_price=37.5065, sample=3876, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0033, p90=0.1419, p10_price=29.1545, p50_price=33.7274, p90_price=39.0012, sample=3866, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0498, p50=0.0015, p90=0.0457, p10_price=32.1971, p50_price=33.8901, p90_price=35.4214, sample=98, fallback=NO
- 10D: p10=-0.0829, p50=0.0104, p90=0.0784, p10_price=31.1464, p50_price=34.1951, p90_price=36.5982, sample=97, fallback=NO
- 20D: p10=-0.1019, p50=0.0263, p90=0.1248, p10_price=30.5615, p50_price=34.7401, p90_price=38.3386, sample=97, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0438, p50=-0.0011, p90=0.0416, p10_price=32.3912, p50_price=33.8038, p90_price=35.2781, sample=3881, fallback=N/A
- 10D: p10=-0.0630, p50=-0.0022, p90=0.0587, p10_price=31.7741, p50_price=33.7672, p90_price=35.8854, sample=3876, fallback=N/A
- 20D: p10=-0.0900, p50=-0.0041, p90=0.0817, p10_price=30.9272, p50_price=33.7000, p90_price=36.7214, sample=3866, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-25T12:24:45.663604+00:00
- 数据快照: cnsvdata-2026-08-25-be479a53e6bd
