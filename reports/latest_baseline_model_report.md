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
- 最新交易日: 2026-07-16
- 最新收盘价: 33.0000
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0870, p50=0.0000, p90=0.0870, p10_price=30.2509, p50_price=33.0000, p90_price=35.9990, sample=3853, fallback=N/A
- 10D: p10=-0.1230, p50=0.0000, p90=0.1230, p10_price=29.1804, p50_price=33.0000, p90_price=37.3196, sample=3848, fallback=N/A
- 20D: p10=-0.1740, p50=0.0000, p90=0.1740, p10_price=27.7308, p50_price=33.0000, p90_price=39.2704, sample=3838, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0017, p90=0.0719, p10_price=30.7963, p50_price=32.9448, p90_price=35.4589, sample=3853, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0037, p90=0.1031, p10_price=29.8280, p50_price=32.8795, p90_price=36.5853, sample=3848, fallback=N/A
- 20D: p10=-0.1492, p50=-0.0032, p90=0.1428, p10_price=28.4260, p50_price=32.8958, p90_price=38.0643, sample=3838, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1105, p50=-0.0076, p90=0.0677, p10_price=29.5487, p50_price=32.7510, p90_price=35.3099, sample=92, fallback=NO
- 10D: p10=-0.1307, p50=0.0036, p90=0.1447, p10_price=28.9557, p50_price=33.1192, p90_price=38.1398, sample=92, fallback=NO
- 20D: p10=-0.1696, p50=0.0140, p90=0.1226, p10_price=27.8511, p50_price=33.4642, p90_price=37.3057, sample=89, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.1088, p50=-0.0010, p90=0.1067, p10_price=29.5993, p50_price=32.9657, p90_price=36.7150, sample=3853, fallback=N/A
- 10D: p10=-0.1555, p50=-0.0020, p90=0.1514, p10_price=28.2485, p50_price=32.9336, p90_price=38.3957, sample=3848, fallback=N/A
- 20D: p10=-0.2208, p50=-0.0040, p90=0.2128, p10_price=26.4611, p50_price=32.8681, p90_price=40.8265, sample=3838, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-16T16:54:03.832395+00:00
- 数据快照: cnsvdata-2026-07-16-d5a61717b5d3
