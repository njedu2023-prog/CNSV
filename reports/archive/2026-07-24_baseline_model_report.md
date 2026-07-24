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
- 最新交易日: 2026-07-24
- 最新收盘价: 33.0600
- 趋势状态: strong_downtrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0811, p50=0.0000, p90=0.0811, p10_price=30.4855, p50_price=33.0600, p90_price=35.8519, sample=3859, fallback=N/A
- 10D: p10=-0.1147, p50=0.0000, p90=0.1147, p10_price=29.4788, p50_price=33.0600, p90_price=37.0763, sample=3854, fallback=N/A
- 20D: p10=-0.1621, p50=0.0000, p90=0.1621, p10_price=28.1115, p50_price=33.0600, p90_price=38.8795, sample=3844, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0017, p90=0.0717, p10_price=30.8516, p50_price=33.0045, p90_price=35.5171, sample=3859, fallback=N/A
- 10D: p10=-0.1016, p50=-0.0039, p90=0.1030, p10_price=29.8654, p50_price=32.9317, p90_price=36.6469, sample=3854, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0034, p90=0.1425, p10_price=28.4794, p50_price=32.9485, p90_price=38.1238, sample=3844, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1424, p50=0.0097, p90=0.0888, p10_price=28.6707, p50_price=33.3832, p90_price=36.1303, sample=69, fallback=NO
- 10D: p10=-0.1041, p50=0.0003, p90=0.1241, p10_price=29.7909, p50_price=33.0705, p90_price=37.4295, sample=69, fallback=NO
- 20D: p10=-0.2008, p50=-0.0167, p90=0.1520, p10_price=27.0459, p50_price=32.5119, p90_price=38.4860, sample=68, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0991, p50=-0.0011, p90=0.0970, p10_price=29.9399, p50_price=33.0241, p90_price=36.4260, sample=3859, fallback=N/A
- 10D: p10=-0.1419, p50=-0.0022, p90=0.1375, p10_price=28.6860, p50_price=32.9879, p90_price=37.9349, sample=3854, fallback=N/A
- 20D: p10=-0.2014, p50=-0.0041, p90=0.1932, p10_price=27.0295, p50_price=32.9243, p90_price=40.1048, sample=3844, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-24T12:24:45.139731+00:00
- 数据快照: cnsvdata-2026-07-24-264425c99a01
