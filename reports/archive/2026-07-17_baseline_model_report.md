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
- 最新交易日: 2026-07-17
- 最新收盘价: 32.3400
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0837, p50=0.0000, p90=0.0837, p10_price=29.7442, p50_price=32.3400, p90_price=35.1623, sample=3854, fallback=N/A
- 10D: p10=-0.1183, p50=0.0000, p90=0.1183, p10_price=28.7310, p50_price=32.3400, p90_price=36.4023, sample=3849, fallback=N/A
- 20D: p10=-0.1673, p50=0.0000, p90=0.1673, p10_price=27.3568, p50_price=32.3400, p90_price=38.2310, sample=3839, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0017, p90=0.0718, p10_price=30.1797, p50_price=32.2858, p90_price=34.7487, sample=3854, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0037, p90=0.1031, p10_price=29.2293, p50_price=32.2215, p90_price=35.8520, sample=3849, fallback=N/A
- 20D: p10=-0.1492, p50=-0.0032, p90=0.1427, p10_price=27.8579, p50_price=32.2359, p90_price=37.3017, sample=3839, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0805, p50=-0.0040, p90=0.0846, p10_price=29.8384, p50_price=32.2107, p90_price=35.1965, sample=173, fallback=NO
- 10D: p10=-0.1182, p50=-0.0059, p90=0.1187, p10_price=28.7360, p50_price=32.1484, p90_price=36.4156, sample=173, fallback=NO
- 20D: p10=-0.1593, p50=0.0037, p90=0.1554, p10_price=27.5783, p50_price=32.4604, p90_price=37.7785, sample=172, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.1083, p50=-0.0011, p90=0.1061, p10_price=29.0215, p50_price=32.3052, p90_price=35.9606, sample=3854, fallback=N/A
- 10D: p10=-0.1547, p50=-0.0021, p90=0.1506, p10_price=27.7043, p50_price=32.2738, p90_price=37.5969, sample=3849, fallback=N/A
- 20D: p10=-0.2197, p50=-0.0040, p90=0.2116, p10_price=25.9610, p50_price=32.2099, p90_price=39.9628, sample=3839, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-17T12:24:47.626768+00:00
- 数据快照: cnsvdata-2026-07-17-1aee2598b1ca
