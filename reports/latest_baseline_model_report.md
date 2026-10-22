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
- 最新交易日: 2026-10-22
- 最新收盘价: 34.5300
- 趋势状态: strong_downtrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0668, p50=0.0000, p90=0.0668, p10_price=32.2995, p50_price=34.5300, p90_price=36.9146, sample=3917, fallback=N/A
- 10D: p10=-0.0944, p50=0.0000, p90=0.0944, p10_price=31.4183, p50_price=34.5300, p90_price=37.9499, sample=3912, fallback=N/A
- 20D: p10=-0.1336, p50=0.0000, p90=0.1336, p10_price=30.2130, p50_price=34.5300, p90_price=39.4638, sample=3902, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0716, p10_price=32.2270, p50_price=34.4723, p90_price=37.0936, sample=3917, fallback=N/A
- 10D: p10=-0.1010, p50=-0.0036, p90=0.1035, p10_price=31.2128, p50_price=34.4044, p90_price=38.2962, sample=3912, fallback=N/A
- 20D: p10=-0.1486, p50=-0.0028, p90=0.1432, p10_price=29.7631, p50_price=34.4333, p90_price=39.8472, sample=3902, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0691, p50=0.0005, p90=0.0711, p10_price=32.2248, p50_price=34.5481, p90_price=37.0751, sample=156, fallback=NO
- 10D: p10=-0.0898, p50=-0.0010, p90=0.0923, p10_price=31.5641, p50_price=34.4957, p90_price=37.8693, sample=154, fallback=NO
- 20D: p10=-0.1753, p50=-0.0038, p90=0.1309, p10_price=28.9775, p50_price=34.3976, p90_price=39.3581, sample=154, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0813, p50=-0.0010, p90=0.0793, p10_price=31.8338, p50_price=34.4957, p90_price=37.3803, sample=3917, fallback=N/A
- 10D: p10=-0.1163, p50=-0.0019, p90=0.1125, p10_price=30.7393, p50_price=34.4639, p90_price=38.6398, sample=3912, fallback=N/A
- 20D: p10=-0.1650, p50=-0.0036, p90=0.1578, p10_price=29.2792, p50_price=34.4065, p90_price=40.4317, sample=3902, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-10-22T15:23:12.647641+00:00
- 数据快照: cnsvdata-2026-10-22-acf74a3708b5
