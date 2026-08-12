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
- 最新交易日: 2026-08-12
- 最新收盘价: 33.8900
- 趋势状态: downtrend
- 波动率状态: normal_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0726, p50=0.0000, p90=0.0726, p10_price=31.5179, p50_price=33.8900, p90_price=36.4406, sample=3872, fallback=N/A
- 10D: p10=-0.1026, p50=0.0000, p90=0.1026, p10_price=30.5847, p50_price=33.8900, p90_price=37.5525, sample=3867, fallback=N/A
- 20D: p10=-0.1451, p50=0.0000, p90=0.1451, p10_price=29.3118, p50_price=33.8900, p90_price=39.1832, sample=3857, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0716, p10_price=31.6296, p50_price=33.8342, p90_price=36.4053, sample=3872, fallback=N/A
- 10D: p10=-0.1013, p50=-0.0036, p90=0.1029, p10_price=30.6244, p50_price=33.7667, p90_price=37.5639, sample=3867, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0035, p90=0.1421, p10_price=29.1967, p50_price=33.7704, p90_price=39.0638, sample=3857, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0674, p50=-0.0109, p90=0.0709, p10_price=31.6797, p50_price=33.5231, p90_price=36.3806, sample=199, fallback=NO
- 10D: p10=-0.1089, p50=-0.0095, p90=0.0880, p10_price=30.3932, p50_price=33.5711, p90_price=37.0090, sample=199, fallback=NO
- 20D: p10=-0.1327, p50=-0.0134, p90=0.1101, p10_price=29.6796, p50_price=33.4381, p90_price=37.8330, sample=199, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0559, p50=-0.0010, p90=0.0539, p10_price=32.0459, p50_price=33.8550, p90_price=35.7662, sample=3872, fallback=N/A
- 10D: p10=-0.0803, p50=-0.0021, p90=0.0762, p10_price=31.2738, p50_price=33.8198, p90_price=36.5731, sample=3867, fallback=N/A
- 20D: p10=-0.1147, p50=-0.0042, p90=0.1063, p10_price=30.2188, p50_price=33.7485, p90_price=37.6906, sample=3857, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-12T12:24:43.902059+00:00
- 数据快照: cnsvdata-2026-08-12-e8147ed2cad7
