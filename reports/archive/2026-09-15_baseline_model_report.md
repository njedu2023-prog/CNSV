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
- 最新交易日: 2026-09-15
- 最新收盘价: 38.1600
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0750, p50=0.0000, p90=0.0750, p10_price=35.4026, p50_price=38.1600, p90_price=41.1322, sample=3896, fallback=N/A
- 10D: p10=-0.1061, p50=0.0000, p90=0.1061, p10_price=34.3196, p50_price=38.1600, p90_price=42.4301, sample=3891, fallback=N/A
- 20D: p10=-0.1500, p50=0.0000, p90=0.1500, p10_price=32.8444, p50_price=38.1600, p90_price=44.3359, sample=3881, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0689, p50=-0.0016, p90=0.0720, p10_price=35.6207, p50_price=38.0995, p90_price=41.0072, sample=3896, fallback=N/A
- 10D: p10=-0.1010, p50=-0.0036, p90=0.1035, p10_price=34.4928, p50_price=38.0226, p90_price=42.3223, sample=3891, fallback=N/A
- 20D: p10=-0.1489, p50=-0.0032, p90=0.1427, p10_price=32.8814, p50_price=38.0388, p90_price=44.0116, sample=3881, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0794, p50=-0.0071, p90=0.0863, p10_price=35.2481, p50_price=37.8911, p90_price=41.6008, sample=191, fallback=NO
- 10D: p10=-0.1153, p50=-0.0201, p90=0.0829, p10_price=34.0055, p50_price=37.4021, p90_price=41.4571, sample=191, fallback=NO
- 20D: p10=-0.1611, p50=-0.0327, p90=0.1261, p10_price=32.4822, p50_price=36.9324, p90_price=43.2876, sample=191, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0780, p50=-0.0009, p90=0.0763, p10_price=35.2959, p50_price=38.1274, p90_price=41.1861, sample=3896, fallback=N/A
- 10D: p10=-0.1117, p50=-0.0018, p90=0.1081, p10_price=34.1257, p50_price=38.0903, p90_price=42.5155, sample=3891, fallback=N/A
- 20D: p10=-0.1588, p50=-0.0039, p90=0.1511, p10_price=32.5557, p50_price=38.0124, p90_price=44.3838, sample=3881, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-15T15:05:28.917441+00:00
- 数据快照: cnsvdata-2026-09-15-539278e48c30
