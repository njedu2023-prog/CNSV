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
- 最新交易日: 2026-09-30
- 最新收盘价: 39.1000
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0687, p50=0.0000, p90=0.0687, p10_price=36.5050, p50_price=39.1000, p90_price=41.8794, sample=3906, fallback=N/A
- 10D: p10=-0.0971, p50=0.0000, p90=0.0971, p10_price=35.4813, p50_price=39.1000, p90_price=43.0878, sample=3901, fallback=N/A
- 20D: p10=-0.1373, p50=0.0000, p90=0.1373, p10_price=34.0823, p50_price=39.1000, p90_price=44.8564, sample=3891, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0688, p50=-0.0016, p90=0.0718, p10_price=36.5012, p50_price=39.0364, p90_price=42.0097, sample=3906, fallback=N/A
- 10D: p10=-0.1006, p50=-0.0036, p90=0.1038, p10_price=35.3571, p50_price=38.9596, p90_price=43.3777, sample=3901, fallback=N/A
- 20D: p10=-0.1488, p50=-0.0027, p90=0.1432, p10_price=33.6937, p50_price=38.9946, p90_price=45.1218, sample=3891, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0788, p50=-0.0043, p90=0.0735, p10_price=36.1382, p50_price=38.9314, p90_price=42.0833, sample=77, fallback=NO
- 10D: p10=-0.1055, p50=-0.0189, p90=0.0772, p10_price=35.1847, p50_price=38.3675, p90_price=42.2389, sample=77, fallback=NO
- 20D: p10=-0.1526, p50=-0.0207, p90=0.1414, p10_price=33.5662, p50_price=38.2995, p90_price=45.0397, sample=77, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0894, p50=-0.0009, p90=0.0877, p10_price=35.7553, p50_price=39.0655, p90_price=42.6822, sample=3906, fallback=N/A
- 10D: p10=-0.1279, p50=-0.0018, p90=0.1244, p10_price=34.4061, p50_price=39.0315, p90_price=44.2787, sample=3901, fallback=N/A
- 20D: p10=-0.1815, p50=-0.0035, p90=0.1745, p10_price=32.6099, p50_price=38.9631, p90_price=46.5541, sample=3891, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-10-08T17:55:49.440032+00:00
- 数据快照: cnsvdata-2026-09-30-3e8a073970a3
