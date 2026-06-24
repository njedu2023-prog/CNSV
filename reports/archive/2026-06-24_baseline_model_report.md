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
- 最新交易日: 2026-06-24
- 最新收盘价: 35.3500
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0716, p50=0.0000, p90=0.0716, p10_price=32.9081, p50_price=35.3500, p90_price=37.9731, sample=3837, fallback=N/A
- 10D: p10=-0.1012, p50=0.0000, p90=0.1012, p10_price=31.9467, p50_price=35.3500, p90_price=39.1158, sample=3832, fallback=N/A
- 20D: p10=-0.1432, p50=0.0000, p90=0.1432, p10_price=30.6349, p50_price=35.3500, p90_price=40.7908, sample=3822, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0688, p50=-0.0016, p90=0.0716, p10_price=32.9982, p50_price=35.2925, p90_price=37.9745, sample=3837, fallback=N/A
- 10D: p10=-0.1012, p50=-0.0037, p90=0.1035, p10_price=31.9471, p50_price=35.2184, p90_price=39.2029, sample=3832, fallback=N/A
- 20D: p10=-0.1494, p50=-0.0029, p90=0.1430, p10_price=30.4448, p50_price=35.2482, p90_price=40.7857, sample=3822, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1134, p50=-0.0076, p90=0.0693, p10_price=31.5600, p50_price=35.0811, p90_price=37.8858, sample=89, fallback=NO
- 10D: p10=-0.1318, p50=0.0007, p90=0.1470, p10_price=30.9839, p50_price=35.3730, p90_price=40.9487, sample=89, fallback=NO
- 20D: p10=-0.1750, p50=0.0151, p90=0.1244, p10_price=29.6738, p50_price=35.8883, p90_price=40.0323, sample=88, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0649, p50=-0.0010, p90=0.0629, p10_price=33.1293, p50_price=35.3156, p90_price=37.6461, sample=3837, fallback=N/A
- 10D: p10=-0.0933, p50=-0.0020, p90=0.0892, p10_price=32.2026, p50_price=35.2790, p90_price=38.6493, sample=3832, fallback=N/A
- 20D: p10=-0.1328, p50=-0.0039, p90=0.1250, p10_price=30.9538, p50_price=35.2125, p90_price=40.0572, sample=3822, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-06-24T21:10:05.970380+00:00
- 数据快照: cnsvdata-2026-06-24-9039ab677ed3
