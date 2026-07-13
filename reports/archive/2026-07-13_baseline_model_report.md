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
- 最新交易日: 2026-07-13
- 最新收盘价: 34.2100
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0855, p50=0.0000, p90=0.0855, p10_price=31.4054, p50_price=34.2100, p90_price=37.2651, sample=3850, fallback=N/A
- 10D: p10=-0.1210, p50=0.0000, p90=0.1210, p10_price=30.3121, p50_price=34.2100, p90_price=38.6091, sample=3845, fallback=N/A
- 20D: p10=-0.1711, p50=0.0000, p90=0.1711, p10_price=28.8307, p50_price=34.2100, p90_price=40.5930, sample=3835, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0719, p10_price=31.9283, p50_price=34.1537, p90_price=36.7615, sample=3850, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0036, p90=0.1033, p10_price=30.9211, p50_price=34.0855, p90_price=37.9317, sample=3845, fallback=N/A
- 20D: p10=-0.1492, p50=-0.0029, p90=0.1429, p10_price=29.4670, p50_price=34.1103, p90_price=39.4642, sample=3835, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1105, p50=-0.0076, p90=0.0677, p10_price=30.6322, p50_price=33.9519, p90_price=36.6046, sample=92, fallback=NO
- 10D: p10=-0.1316, p50=0.0066, p90=0.1467, p10_price=29.9931, p50_price=34.4352, p90_price=39.6137, sample=91, fallback=NO
- 20D: p10=-0.1696, p50=0.0140, p90=0.1226, p10_price=28.8723, p50_price=34.6912, p90_price=38.6736, sample=89, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.1099, p50=-0.0010, p90=0.1079, p10_price=30.6496, p50_price=34.1765, p90_price=38.1092, sample=3850, fallback=N/A
- 10D: p10=-0.1572, p50=-0.0020, p90=0.1532, p10_price=29.2322, p50_price=34.1417, p90_price=39.8757, sample=3845, fallback=N/A
- 20D: p10=-0.2233, p50=-0.0039, p90=0.2154, p10_price=27.3640, p50_price=34.0752, p90_price=42.4324, sample=3835, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-13T16:31:08.377152+00:00
- 数据快照: cnsvdata-2026-07-13-6a69c54046df
