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
- 最新交易日: 2026-10-21
- 最新收盘价: 34.8600
- 趋势状态: strong_downtrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0667, p50=0.0000, p90=0.0667, p10_price=32.6118, p50_price=34.8600, p90_price=37.2632, sample=3916, fallback=N/A
- 10D: p10=-0.0943, p50=0.0000, p90=0.0943, p10_price=31.7235, p50_price=34.8600, p90_price=38.3066, sample=3911, fallback=N/A
- 20D: p10=-0.1333, p50=0.0000, p90=0.1333, p10_price=30.5085, p50_price=34.8600, p90_price=39.8321, sample=3901, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0716, p10_price=32.5349, p50_price=34.8018, p90_price=37.4482, sample=3916, fallback=N/A
- 10D: p10=-0.1007, p50=-0.0036, p90=0.1035, p10_price=31.5217, p50_price=34.7333, p90_price=38.6623, sample=3911, fallback=N/A
- 20D: p10=-0.1487, p50=-0.0028, p90=0.1432, p10_price=30.0442, p50_price=34.7639, p90_price=40.2288, sample=3901, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0700, p50=0.0007, p90=0.0717, p10_price=32.5022, p50_price=34.8852, p90_price=37.4525, sample=155, fallback=NO
- 10D: p10=-0.0898, p50=-0.0010, p90=0.0923, p10_price=31.8658, p50_price=34.8254, p90_price=38.2312, sample=154, fallback=NO
- 20D: p10=-0.1753, p50=-0.0038, p90=0.1309, p10_price=29.2544, p50_price=34.7263, p90_price=39.7343, sample=154, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0813, p50=-0.0010, p90=0.0793, p10_price=32.1380, p50_price=34.8256, p90_price=37.7381, sample=3916, fallback=N/A
- 10D: p10=-0.1162, p50=-0.0019, p90=0.1125, p10_price=31.0348, p50_price=34.7945, p90_price=39.0097, sample=3911, fallback=N/A
- 20D: p10=-0.1649, p50=-0.0036, p90=0.1578, p10_price=29.5594, p50_price=34.7361, p90_price=40.8193, sample=3901, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-10-21T15:22:17.206743+00:00
- 数据快照: cnsvdata-2026-10-21-6217d52db1c2
