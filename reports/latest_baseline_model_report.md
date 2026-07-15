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
- 最新交易日: 2026-07-15
- 最新收盘价: 34.3100
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0858, p50=0.0000, p90=0.0858, p10_price=31.4889, p50_price=34.3100, p90_price=37.3839, sample=3852, fallback=N/A
- 10D: p10=-0.1213, p50=0.0000, p90=0.1213, p10_price=30.3894, p50_price=34.3100, p90_price=38.7364, sample=3847, fallback=N/A
- 20D: p10=-0.1716, p50=0.0000, p90=0.1716, p10_price=28.8997, p50_price=34.3100, p90_price=40.7332, sample=3837, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0719, p10_price=32.0216, p50_price=34.2527, p90_price=36.8676, sample=3852, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0036, p90=0.1032, p10_price=31.0119, p50_price=34.1851, p90_price=38.0393, sample=3847, fallback=N/A
- 20D: p10=-0.1492, p50=-0.0031, p90=0.1428, p10_price=29.5540, p50_price=34.2037, p90_price=39.5768, sample=3837, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1105, p50=-0.0076, p90=0.0677, p10_price=30.7217, p50_price=34.0512, p90_price=36.7116, sample=92, fallback=NO
- 10D: p10=-0.1316, p50=0.0066, p90=0.1467, p10_price=30.0808, p50_price=34.5358, p90_price=39.7295, sample=91, fallback=NO
- 20D: p10=-0.1696, p50=0.0140, p90=0.1226, p10_price=28.9567, p50_price=34.7926, p90_price=38.7867, sample=89, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.1089, p50=-0.0010, p90=0.1069, p10_price=30.7699, p50_price=34.2751, p90_price=38.1796, sample=3852, fallback=N/A
- 10D: p10=-0.1557, p50=-0.0020, p90=0.1517, p10_price=29.3623, p50_price=34.2413, p90_price=39.9310, sample=3847, fallback=N/A
- 20D: p10=-0.2212, p50=-0.0040, p90=0.2132, p10_price=27.5024, p50_price=34.1739, p90_price=42.4638, sample=3837, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-15T14:16:45.201671+00:00
- 数据快照: cnsvdata-2026-07-15-423a7c34c060
