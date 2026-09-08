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
- 最新交易日: 2026-09-08
- 最新收盘价: 39.0800
- 趋势状态: strong_uptrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0767, p50=0.0000, p90=0.0767, p10_price=36.1964, p50_price=39.0800, p90_price=42.1933, sample=3891, fallback=N/A
- 10D: p10=-0.1084, p50=0.0000, p90=0.1084, p10_price=35.0653, p50_price=39.0800, p90_price=43.5544, sample=3886, fallback=N/A
- 20D: p10=-0.1533, p50=0.0000, p90=0.1533, p10_price=33.5256, p50_price=39.0800, p90_price=45.5546, sample=3876, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0689, p50=-0.0016, p90=0.0716, p10_price=36.4765, p50_price=39.0164, p90_price=41.9820, sample=3891, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0036, p90=0.1030, p10_price=35.3231, p50_price=38.9379, p90_price=43.3199, sample=3886, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0033, p90=0.1413, p10_price=33.6715, p50_price=38.9499, p90_price=45.0113, sample=3876, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0941, p50=-0.0008, p90=0.1531, p10_price=35.5708, p50_price=39.0495, p90_price=45.5438, sample=73, fallback=NO
- 10D: p10=-0.1069, p50=0.0111, p90=0.2774, p10_price=35.1179, p50_price=39.5148, p90_price=51.5725, sample=73, fallback=NO
- 20D: p10=-0.1646, p50=0.0022, p90=0.1992, p10_price=33.1473, p50_price=39.1644, p90_price=47.6919, sample=73, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0697, p50=-0.0010, p90=0.0678, p10_price=36.4494, p50_price=39.0428, p90_price=41.8207, sample=3891, fallback=N/A
- 10D: p10=-0.0999, p50=-0.0020, p90=0.0959, p10_price=35.3635, p50_price=39.0017, p90_price=43.0141, sample=3886, fallback=N/A
- 20D: p10=-0.1422, p50=-0.0041, p90=0.1340, p10_price=33.8995, p50_price=38.9207, p90_price=44.6856, sample=3876, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-08T14:38:45.882904+00:00
- 数据快照: cnsvdata-2026-09-08-3937b120f22f
