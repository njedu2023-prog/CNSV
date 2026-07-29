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
- non_gating_warnings: 3
- fallback_count: 3

## 受控回退说明
B2 状态分组样本不足时透明回退到 B1 历史分布基准；该回退不生成正式交易信号，也不影响 V1.2 基准模型层验收状态。
- B2_state_grouped_distribution 5D: state_key=neutral|high_vol|mixed, reason=state_sample_size_lt_30, state_sample_size=23, usable_state_rows=3818, fallback_method=B1_historical_distribution, gating=NO, non_blocking=YES, next_coverage_action=extend historical state coverage for trend_state, volatility_state, and flow_strength_basic
- B2_state_grouped_distribution 10D: state_key=neutral|high_vol|mixed, reason=state_sample_size_lt_30, state_sample_size=23, usable_state_rows=3818, fallback_method=B1_historical_distribution, gating=NO, non_blocking=YES, next_coverage_action=extend historical state coverage for trend_state, volatility_state, and flow_strength_basic
- B2_state_grouped_distribution 20D: state_key=neutral|high_vol|mixed, reason=state_sample_size_lt_30, state_sample_size=23, usable_state_rows=3818, fallback_method=B1_historical_distribution, gating=NO, non_blocking=YES, next_coverage_action=extend historical state coverage for trend_state, volatility_state, and flow_strength_basic

## 当前状态
- 最新交易日: 2026-07-29
- 最新收盘价: 34.7300
- 趋势状态: neutral
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0774, p50=0.0000, p90=0.0774, p10_price=32.1446, p50_price=34.7300, p90_price=37.5233, sample=3862, fallback=N/A
- 10D: p10=-0.1094, p50=0.0000, p90=0.1094, p10_price=31.1309, p50_price=34.7300, p90_price=38.7452, sample=3857, fallback=N/A
- 20D: p10=-0.1547, p50=0.0000, p90=0.1547, p10_price=29.7517, p50_price=34.7300, p90_price=40.5413, sample=3847, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0017, p90=0.0716, p10_price=32.4104, p50_price=34.6720, p90_price=37.3089, sample=3862, fallback=N/A
- 10D: p10=-0.1016, p50=-0.0039, p90=0.1030, p10_price=31.3762, p50_price=34.5938, p90_price=38.4979, sample=3857, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0034, p90=0.1424, p10_price=29.9185, p50_price=34.6127, p90_price=40.0437, sample=3847, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0691, p50=-0.0017, p90=0.0716, p10_price=32.4104, p50_price=34.6720, p90_price=37.3089, sample=23, fallback=YES
- 10D: p10=-0.1016, p50=-0.0039, p90=0.1030, p10_price=31.3762, p50_price=34.5938, p90_price=38.4979, sample=23, fallback=YES
- 20D: p10=-0.1491, p50=-0.0034, p90=0.1424, p10_price=29.9185, p50_price=34.6127, p90_price=40.0437, sample=23, fallback=YES

### B3_volatility_adjusted
- 5D: p10=-0.0986, p50=-0.0011, p90=0.0965, p10_price=31.4691, p50_price=34.6930, p90_price=38.2472, sample=3862, fallback=N/A
- 10D: p10=-0.1412, p50=-0.0022, p90=0.1368, p10_price=30.1574, p50_price=34.6542, p90_price=39.8214, sample=3857, fallback=N/A
- 20D: p10=-0.2003, p50=-0.0041, p90=0.1921, p10_price=28.4246, p50_price=34.5874, p90_price=42.0862, sample=3847, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-29T12:25:33.711711+00:00
- 数据快照: cnsvdata-2026-07-29-6d0cafe8e925
