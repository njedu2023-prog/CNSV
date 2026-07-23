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
- 最新交易日: 2026-07-23
- 最新收盘价: 33.7600
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0808, p50=0.0000, p90=0.0808, p10_price=31.1386, p50_price=33.7600, p90_price=36.6020, sample=3858, fallback=N/A
- 10D: p10=-0.1143, p50=0.0000, p90=0.1143, p10_price=30.1134, p50_price=33.7600, p90_price=37.8482, sample=3853, fallback=N/A
- 20D: p10=-0.1617, p50=0.0000, p90=0.1617, p10_price=28.7208, p50_price=33.7600, p90_price=39.6833, sample=3843, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0017, p90=0.0717, p10_price=31.5049, p50_price=33.7032, p90_price=36.2702, sample=3858, fallback=N/A
- 10D: p10=-0.1014, p50=-0.0038, p90=0.1030, p10_price=30.5040, p50_price=33.6303, p90_price=37.4229, sample=3853, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0034, p90=0.1426, p10_price=29.0823, p50_price=33.6463, p90_price=38.9330, sample=3843, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0638, p50=0.0011, p90=0.0659, p10_price=31.6738, p50_price=33.7977, p90_price=36.0606, sample=80, fallback=NO
- 10D: p10=-0.1005, p50=0.0044, p90=0.0926, p10_price=30.5314, p50_price=33.9073, p90_price=37.0340, sample=80, fallback=NO
- 20D: p10=-0.1390, p50=0.0042, p90=0.1189, p10_price=29.3786, p50_price=33.9020, p90_price=38.0239, sample=79, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.1049, p50=-0.0011, p90=0.1027, p10_price=30.3984, p50_price=33.7231, p90_price=37.4114, sample=3858, fallback=N/A
- 10D: p10=-0.1501, p50=-0.0022, p90=0.1457, p10_price=29.0560, p50_price=33.6874, p90_price=39.0570, sample=3853, fallback=N/A
- 20D: p10=-0.2130, p50=-0.0041, p90=0.2047, p10_price=27.2843, p50_price=33.6215, p90_price=41.4306, sample=3843, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-23T12:24:44.257129+00:00
- 数据快照: cnsvdata-2026-07-23-9cc7c812e1ad
