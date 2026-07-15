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
- 最新交易日: 2026-07-14
- 最新收盘价: 33.7700
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0856, p50=0.0000, p90=0.0856, p10_price=30.9991, p50_price=33.7700, p90_price=36.7886, sample=3851, fallback=N/A
- 10D: p10=-0.1211, p50=0.0000, p90=0.1211, p10_price=29.9190, p50_price=33.7700, p90_price=38.1167, sample=3846, fallback=N/A
- 20D: p10=-0.1712, p50=0.0000, p90=0.1712, p10_price=28.4555, p50_price=33.7700, p90_price=40.0770, sample=3836, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0719, p10_price=31.5176, p50_price=33.7137, p90_price=36.2884, sample=3851, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0036, p90=0.1032, p10_price=30.5236, p50_price=33.6472, p90_price=37.4422, sample=3846, fallback=N/A
- 20D: p10=-0.1492, p50=-0.0030, p90=0.1428, p10_price=29.0884, p50_price=33.6685, p90_price=38.9552, sample=3836, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0805, p50=-0.0040, p90=0.0846, p10_price=31.1578, p50_price=33.6350, p90_price=36.7528, sample=173, fallback=NO
- 10D: p10=-0.1182, p50=-0.0059, p90=0.1187, p10_price=30.0066, p50_price=33.5699, p90_price=38.0259, sample=173, fallback=NO
- 20D: p10=-0.1593, p50=0.0037, p90=0.1554, p10_price=28.7977, p50_price=33.8958, p90_price=39.4489, sample=172, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.1082, p50=-0.0010, p90=0.1062, p10_price=30.3062, p50_price=33.7361, p90_price=37.5541, sample=3851, fallback=N/A
- 10D: p10=-0.1548, p50=-0.0020, p90=0.1508, p10_price=28.9276, p50_price=33.7026, p90_price=39.2657, sample=3846, fallback=N/A
- 20D: p10=-0.2198, p50=-0.0040, p90=0.2119, p10_price=27.1060, p50_price=33.6364, p90_price=41.7403, sample=3836, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-15T07:01:53.703068+00:00
- 数据快照: cnsvdata-2026-07-14-39131a8e93f4
