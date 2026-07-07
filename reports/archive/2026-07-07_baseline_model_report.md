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
- 最新交易日: 2026-07-07
- 最新收盘价: 37.3300
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0784, p50=0.0000, p90=0.0784, p10_price=34.5148, p50_price=37.3300, p90_price=40.3748, sample=3846, fallback=N/A
- 10D: p10=-0.1109, p50=0.0000, p90=0.1109, p10_price=33.4118, p50_price=37.3300, p90_price=41.7076, sample=3841, fallback=N/A
- 20D: p10=-0.1568, p50=0.0000, p90=0.1568, p10_price=31.9119, p50_price=37.3300, p90_price=43.6680, sample=3831, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0720, p10_price=34.8417, p50_price=37.2685, p90_price=40.1153, sample=3846, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0038, p90=0.1030, p10_price=33.7402, p50_price=37.1888, p90_price=41.3803, sample=3841, fallback=N/A
- 20D: p10=-0.1493, p50=-0.0031, p90=0.1430, p10_price=32.1525, p50_price=37.2144, p90_price=43.0694, sample=3831, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0705, p50=-0.0011, p90=0.0745, p10_price=34.7887, p50_price=37.2890, p90_price=40.2193, sample=74, fallback=NO
- 10D: p10=-0.0953, p50=-0.0165, p90=0.0796, p10_price=33.9358, p50_price=36.7208, p90_price=40.4238, sample=74, fallback=NO
- 20D: p10=-0.1543, p50=-0.0197, p90=0.1454, p10_price=31.9922, p50_price=36.6012, p90_price=43.1732, sample=74, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0925, p50=-0.0010, p90=0.0905, p10_price=34.0324, p50_price=37.2937, p90_price=40.8675, sample=3846, fallback=N/A
- 10D: p10=-0.1325, p50=-0.0020, p90=0.1284, p10_price=32.6974, p50_price=37.2538, p90_price=42.4451, sample=3841, fallback=N/A
- 20D: p10=-0.1883, p50=-0.0040, p90=0.1804, p10_price=30.9222, p50_price=37.1816, p90_price=44.7081, sample=3831, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-07T16:28:43.715539+00:00
- 数据快照: cnsvdata-2026-07-07-82ecf1af0fa1
