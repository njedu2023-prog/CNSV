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
- 最新交易日: 2026-07-31
- 最新收盘价: 35.1800
- 趋势状态: neutral
- 波动率状态: high_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0774, p50=0.0000, p90=0.0774, p10_price=32.5585, p50_price=35.1800, p90_price=38.0126, sample=3864, fallback=N/A
- 10D: p10=-0.1095, p50=0.0000, p90=0.1095, p10_price=31.5307, p50_price=35.1800, p90_price=39.2517, sample=3859, fallback=N/A
- 20D: p10=-0.1549, p50=0.0000, p90=0.1549, p10_price=30.1323, p50_price=35.1800, p90_price=41.0732, sample=3849, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0016, p90=0.0716, p10_price=32.8311, p50_price=35.1221, p90_price=37.7922, sample=3864, fallback=N/A
- 10D: p10=-0.1015, p50=-0.0038, p90=0.1030, p10_price=31.7842, p50_price=35.0449, p90_price=38.9966, sample=3859, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0034, p90=0.1423, p10_price=30.3065, p50_price=35.0611, p90_price=40.5585, sample=3849, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0758, p50=0.0059, p90=0.0905, p10_price=32.6110, p50_price=35.3896, p90_price=38.5139, sample=33, fallback=NO
- 10D: p10=-0.1046, p50=0.0059, p90=0.0877, p10_price=31.6875, p50_price=35.3883, p90_price=38.4047, sample=33, fallback=NO
- 20D: p10=-0.0887, p50=-0.0150, p90=0.1512, p10_price=32.1952, p50_price=34.6560, p90_price=40.9226, sample=33, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0802, p50=-0.0010, p90=0.0781, p10_price=32.4690, p50_price=35.1433, p90_price=38.0380, sample=3864, fallback=N/A
- 10D: p10=-0.1149, p50=-0.0022, p90=0.1106, p10_price=31.3600, p50_price=35.1044, p90_price=39.2959, sample=3859, fallback=N/A
- 20D: p10=-0.1634, p50=-0.0041, p90=0.1551, p10_price=29.8780, p50_price=35.0352, p90_price=41.0825, sample=3849, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-31T12:24:44.176155+00:00
- 数据快照: cnsvdata-2026-07-31-f05451f0431d
