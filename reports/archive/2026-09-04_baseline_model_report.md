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
- 最新交易日: 2026-09-04
- 最新收盘价: 37.4700
- 趋势状态: strong_uptrend
- 波动率状态: high_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0767, p50=0.0000, p90=0.0767, p10_price=34.7024, p50_price=37.4700, p90_price=40.4583, sample=3889, fallback=N/A
- 10D: p10=-0.1085, p50=0.0000, p90=0.1085, p10_price=33.6168, p50_price=37.4700, p90_price=41.7649, sample=3884, fallback=N/A
- 20D: p10=-0.1535, p50=0.0000, p90=0.1535, p10_price=32.1392, p50_price=37.4700, p90_price=43.6850, sample=3874, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0715, p10_price=34.9732, p50_price=37.4090, p90_price=40.2475, sample=3889, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0037, p90=0.1029, p10_price=33.8674, p50_price=37.3332, p90_price=41.5300, sample=3884, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0034, p90=0.1415, p10_price=32.2833, p50_price=37.3436, p90_price=43.1669, sample=3874, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0944, p50=-0.0041, p90=0.1059, p10_price=34.0933, p50_price=37.3158, p90_price=41.6552, sample=99, fallback=NO
- 10D: p10=-0.1154, p50=-0.0146, p90=0.1657, p10_price=33.3863, p50_price=36.9281, p90_price=44.2221, sample=99, fallback=NO
- 20D: p10=-0.1801, p50=0.0021, p90=0.2218, p10_price=31.2944, p50_price=37.5492, p90_price=46.7757, sample=99, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0712, p50=-0.0010, p90=0.0691, p10_price=34.8956, p50_price=37.4319, p90_price=40.1526, sample=3889, fallback=N/A
- 10D: p10=-0.1021, p50=-0.0021, p90=0.0979, p10_price=33.8340, p50_price=37.3923, p90_price=41.3247, sample=3884, fallback=N/A
- 20D: p10=-0.1452, p50=-0.0041, p90=0.1369, p10_price=32.4046, p50_price=37.3149, p90_price=42.9693, sample=3874, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-04T14:25:22.370962+00:00
- 数据快照: cnsvdata-2026-09-04-ef09247b6aa5
