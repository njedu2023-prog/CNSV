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
- 最新交易日: 2026-10-15
- 最新收盘价: 35.4500
- 趋势状态: strong_downtrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0683, p50=0.0000, p90=0.0683, p10_price=33.1099, p50_price=35.4500, p90_price=37.9555, sample=3912, fallback=N/A
- 10D: p10=-0.0966, p50=0.0000, p90=0.0966, p10_price=32.1865, p50_price=35.4500, p90_price=39.0444, sample=3907, fallback=N/A
- 20D: p10=-0.1366, p50=0.0000, p90=0.1366, p10_price=30.9243, p50_price=35.4500, p90_price=40.6380, sample=3897, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0688, p50=-0.0016, p90=0.0716, p10_price=33.0938, p50_price=35.3923, p90_price=38.0824, sample=3912, fallback=N/A
- 10D: p10=-0.1004, p50=-0.0036, p90=0.1036, p10_price=32.0627, p50_price=35.3224, p90_price=39.3213, sample=3907, fallback=N/A
- 20D: p10=-0.1487, p50=-0.0026, p90=0.1433, p10_price=30.5510, p50_price=35.3581, p90_price=40.9101, sample=3897, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0710, p50=0.0009, p90=0.0724, p10_price=33.0212, p50_price=35.4806, p90_price=38.1099, sample=154, fallback=NO
- 10D: p10=-0.0898, p50=-0.0010, p90=0.0923, p10_price=32.4051, p50_price=35.4148, p90_price=38.8782, sample=154, fallback=NO
- 20D: p10=-0.1753, p50=-0.0038, p90=0.1309, p10_price=29.7495, p50_price=35.3141, p90_price=40.4068, sample=154, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0857, p50=-0.0009, p90=0.0839, p10_price=32.5384, p50_price=35.4179, p90_price=38.5523, sample=3912, fallback=N/A
- 10D: p10=-0.1226, p50=-0.0018, p90=0.1190, p10_price=31.3606, p50_price=35.3863, p90_price=39.9289, sample=3907, fallback=N/A
- 20D: p10=-0.1739, p50=-0.0035, p90=0.1670, p10_price=29.7910, p50_price=35.3277, p90_price=41.8934, sample=3897, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-10-15T15:07:16.539466+00:00
- 数据快照: cnsvdata-2026-10-15-f461297b8d39
