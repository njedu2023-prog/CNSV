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
- 最新交易日: 2026-09-18
- 最新收盘价: 39.4700
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0726, p50=0.0000, p90=0.0726, p10_price=36.7052, p50_price=39.4700, p90_price=42.4430, sample=3899, fallback=N/A
- 10D: p10=-0.1027, p50=0.0000, p90=0.1027, p10_price=35.6176, p50_price=39.4700, p90_price=43.7391, sample=3894, fallback=N/A
- 20D: p10=-0.1452, p50=0.0000, p90=0.1452, p10_price=34.1342, p50_price=39.4700, p90_price=45.6399, sample=3884, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0688, p50=-0.0016, p90=0.0719, p10_price=36.8453, p50_price=39.4058, p90_price=42.4141, sample=3899, fallback=N/A
- 10D: p10=-0.1009, p50=-0.0036, p90=0.1040, p10_price=35.6813, p50_price=39.3283, p90_price=43.7972, sample=3894, fallback=N/A
- 20D: p10=-0.1489, p50=-0.0030, p90=0.1430, p10_price=34.0109, p50_price=39.3513, p90_price=45.5391, sample=3884, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0811, p50=-0.0072, p90=0.0771, p10_price=36.3964, p50_price=39.1851, p90_price=42.6323, sample=72, fallback=NO
- 10D: p10=-0.0849, p50=-0.0037, p90=0.1392, p10_price=36.2570, p50_price=39.3238, p90_price=45.3648, sample=72, fallback=NO
- 20D: p10=-0.1552, p50=-0.0317, p90=0.1401, p10_price=33.7976, p50_price=38.2374, p90_price=45.4056, sample=72, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0787, p50=-0.0009, p90=0.0770, p10_price=36.4820, p50_price=39.4353, p90_price=42.6276, sample=3899, fallback=N/A
- 10D: p10=-0.1127, p50=-0.0018, p90=0.1092, p10_price=35.2647, p50_price=39.4009, p90_price=44.0222, sample=3894, fallback=N/A
- 20D: p10=-0.1601, p50=-0.0038, p90=0.1526, p10_price=33.6296, p50_price=39.3221, p90_price=45.9781, sample=3884, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-21T18:56:40.919421+00:00
- 数据快照: cnsvdata-2026-09-18-2c32836fe390
