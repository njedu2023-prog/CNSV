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
- 最新交易日: 2026-07-22
- 最新收盘价: 33.0200
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0804, p50=0.0000, p90=0.0804, p10_price=30.4705, p50_price=33.0200, p90_price=35.7828, sample=3857, fallback=N/A
- 10D: p10=-0.1136, p50=0.0000, p90=0.1136, p10_price=29.4730, p50_price=33.0200, p90_price=36.9938, sample=3852, fallback=N/A
- 20D: p10=-0.1607, p50=0.0000, p90=0.1607, p10_price=28.1179, p50_price=33.0200, p90_price=38.7768, sample=3842, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0017, p90=0.0717, p10_price=30.8143, p50_price=32.9644, p90_price=35.4762, sample=3857, fallback=N/A
- 10D: p10=-0.1014, p50=-0.0038, p90=0.1030, p10_price=29.8347, p50_price=32.8941, p90_price=36.6026, sample=3852, fallback=N/A
- 20D: p10=-0.1492, p50=-0.0033, p90=0.1426, p10_price=28.4447, p50_price=32.9101, p90_price=38.0815, sample=3842, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1058, p50=-0.0085, p90=0.0665, p10_price=29.7054, p50_price=32.7420, p90_price=35.2894, sample=94, fallback=NO
- 10D: p10=-0.1307, p50=0.0036, p90=0.1447, p10_price=28.9733, p50_price=33.1393, p90_price=38.1629, sample=92, fallback=NO
- 20D: p10=-0.1588, p50=0.0096, p90=0.1191, p10_price=28.1704, p50_price=33.3385, p90_price=37.1980, sample=91, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.1035, p50=-0.0011, p90=0.1013, p10_price=29.7723, p50_price=32.9837, p90_price=36.5415, sample=3857, fallback=N/A
- 10D: p10=-0.1481, p50=-0.0021, p90=0.1438, p10_price=28.4747, p50_price=32.9495, p90_price=38.1275, sample=3852, fallback=N/A
- 20D: p10=-0.2102, p50=-0.0041, p90=0.2020, p10_price=26.7595, p50_price=32.8849, p90_price=40.4124, sample=3842, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-22T12:24:54.649773+00:00
- 数据快照: cnsvdata-2026-07-22-cd0574e42525
