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
- B2_state_grouped_distribution 5D: state_key=neutral|high_vol|mixed, reason=state_sample_size_lt_30, state_sample_size=23, usable_state_rows=3819, fallback_method=B1_historical_distribution, gating=NO, non_blocking=YES, next_coverage_action=extend historical state coverage for trend_state, volatility_state, and flow_strength_basic
- B2_state_grouped_distribution 10D: state_key=neutral|high_vol|mixed, reason=state_sample_size_lt_30, state_sample_size=23, usable_state_rows=3819, fallback_method=B1_historical_distribution, gating=NO, non_blocking=YES, next_coverage_action=extend historical state coverage for trend_state, volatility_state, and flow_strength_basic
- B2_state_grouped_distribution 20D: state_key=neutral|high_vol|mixed, reason=state_sample_size_lt_30, state_sample_size=23, usable_state_rows=3819, fallback_method=B1_historical_distribution, gating=NO, non_blocking=YES, next_coverage_action=extend historical state coverage for trend_state, volatility_state, and flow_strength_basic

## 当前状态
- 最新交易日: 2026-07-30
- 最新收盘价: 34.6300
- 趋势状态: neutral
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0772, p50=0.0000, p90=0.0772, p10_price=32.0556, p50_price=34.6300, p90_price=37.4112, sample=3863, fallback=N/A
- 10D: p10=-0.1092, p50=0.0000, p90=0.1092, p10_price=31.0461, p50_price=34.6300, p90_price=38.6276, sample=3858, fallback=N/A
- 20D: p10=-0.1545, p50=0.0000, p90=0.1545, p10_price=29.6725, p50_price=34.6300, p90_price=40.4158, sample=3848, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0017, p90=0.0716, p10_price=32.3175, p50_price=34.5723, p90_price=37.2014, sample=3863, fallback=N/A
- 10D: p10=-0.1015, p50=-0.0039, p90=0.1030, p10_price=31.2865, p50_price=34.4956, p90_price=38.3869, sample=3858, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0034, p90=0.1423, p10_price=29.8325, p50_price=34.5132, p90_price=39.9264, sample=3848, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0691, p50=-0.0017, p90=0.0716, p10_price=32.3175, p50_price=34.5723, p90_price=37.2014, sample=23, fallback=YES
- 10D: p10=-0.1015, p50=-0.0039, p90=0.1030, p10_price=31.2865, p50_price=34.4956, p90_price=38.3869, sample=23, fallback=YES
- 20D: p10=-0.1491, p50=-0.0034, p90=0.1423, p10_price=29.8325, p50_price=34.5132, p90_price=39.9264, sample=23, fallback=YES

### B3_volatility_adjusted
- 5D: p10=-0.0972, p50=-0.0011, p90=0.0951, p10_price=31.4210, p50_price=34.5934, p90_price=38.0860, sample=3863, fallback=N/A
- 10D: p10=-0.1392, p50=-0.0022, p90=0.1349, p10_price=30.1287, p50_price=34.5548, p90_price=39.6312, sample=3858, fallback=N/A
- 20D: p10=-0.1976, p50=-0.0041, p90=0.1894, p10_price=28.4200, p50_price=34.4879, p90_price=41.8513, sample=3848, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-30T12:24:39.529369+00:00
- 数据快照: cnsvdata-2026-07-30-d68c5891b29c
