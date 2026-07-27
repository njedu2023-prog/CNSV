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
- 最新交易日: 2026-07-27
- 最新收盘价: 33.5300
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0762, p50=0.0000, p90=0.0762, p10_price=31.0694, p50_price=33.5300, p90_price=36.1855, sample=3860, fallback=N/A
- 10D: p10=-0.1078, p50=0.0000, p90=0.1078, p10_price=30.1039, p50_price=33.5300, p90_price=37.3461, sample=3855, fallback=N/A
- 20D: p10=-0.1524, p50=0.0000, p90=0.1524, p10_price=28.7894, p50_price=33.5300, p90_price=39.0512, sample=3845, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0017, p90=0.0717, p10_price=31.2903, p50_price=33.4738, p90_price=36.0210, sample=3860, fallback=N/A
- 10D: p10=-0.1016, p50=-0.0039, p90=0.1030, p10_price=30.2907, p50_price=33.3986, p90_price=37.1678, sample=3855, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0034, p90=0.1425, p10_price=28.8845, p50_price=33.4171, p90_price=38.6639, sample=3845, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0638, p50=0.0011, p90=0.0659, p10_price=31.4580, p50_price=33.5674, p90_price=35.8150, sample=80, fallback=NO
- 10D: p10=-0.1005, p50=0.0044, p90=0.0926, p10_price=30.3234, p50_price=33.6763, p90_price=36.7817, sample=80, fallback=NO
- 20D: p10=-0.1390, p50=0.0042, p90=0.1189, p10_price=29.1784, p50_price=33.6711, p90_price=37.7649, sample=79, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0995, p50=-0.0011, p90=0.0974, p10_price=30.3538, p50_price=33.4937, p90_price=36.9584, sample=3860, fallback=N/A
- 10D: p10=-0.1425, p50=-0.0022, p90=0.1381, p10_price=29.0776, p50_price=33.4567, p90_price=38.4954, sample=3855, fallback=N/A
- 20D: p10=-0.2022, p50=-0.0041, p90=0.1940, p10_price=27.3923, p50_price=33.3924, p90_price=40.7068, sample=3845, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-27T13:23:39.099961+00:00
- 数据快照: cnsvdata-2026-07-27-673d53156022
