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
- 最新交易日: 2026-07-20
- 最新收盘价: 33.0100
- 趋势状态: strong_downtrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0833, p50=0.0000, p90=0.0833, p10_price=30.3718, p50_price=33.0100, p90_price=35.8773, sample=3855, fallback=N/A
- 10D: p10=-0.1178, p50=0.0000, p90=0.1178, p10_price=29.3418, p50_price=33.0100, p90_price=37.1368, sample=3850, fallback=N/A
- 20D: p10=-0.1666, p50=0.0000, p90=0.1666, p10_price=27.9445, p50_price=33.0100, p90_price=38.9938, sample=3840, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0017, p90=0.0718, p10_price=30.8049, p50_price=32.9546, p90_price=35.4675, sample=3855, fallback=N/A
- 10D: p10=-0.1013, p50=-0.0037, p90=0.1031, p10_price=29.8312, p50_price=32.8871, p90_price=36.5932, sample=3850, fallback=N/A
- 20D: p10=-0.1492, p50=-0.0033, p90=0.1427, p10_price=28.4355, p50_price=32.9026, p90_price=38.0732, sample=3840, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1424, p50=0.0097, p90=0.0888, p10_price=28.6273, p50_price=33.3327, p90_price=36.0756, sample=69, fallback=NO
- 10D: p10=-0.1041, p50=0.0003, p90=0.1241, p10_price=29.7458, p50_price=33.0205, p90_price=37.3729, sample=69, fallback=NO
- 20D: p10=-0.2008, p50=-0.0167, p90=0.1520, p10_price=27.0050, p50_price=32.4627, p90_price=38.4278, sample=68, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.1066, p50=-0.0011, p90=0.1044, p10_price=29.6732, p50_price=32.9742, p90_price=36.6425, sample=3855, fallback=N/A
- 10D: p10=-0.1523, p50=-0.0021, p90=0.1482, p10_price=28.3455, p50_price=32.9413, p90_price=38.2822, sample=3850, fallback=N/A
- 20D: p10=-0.2163, p50=-0.0041, p90=0.2082, p10_price=26.5891, p50_price=32.8761, p90_price=40.6498, sample=3840, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-20T12:28:21.969924+00:00
- 数据快照: cnsvdata-2026-07-20-151a7e16dce5
