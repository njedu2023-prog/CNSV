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
- 最新交易日: 2026-07-02
- 最新收盘价: 34.3600
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0751, p50=0.0000, p90=0.0751, p10_price=31.8735, p50_price=34.3600, p90_price=37.0405, sample=3843, fallback=N/A
- 10D: p10=-0.1062, p50=0.0000, p90=0.1062, p10_price=30.8970, p50_price=34.3600, p90_price=38.2112, sample=3838, fallback=N/A
- 20D: p10=-0.1502, p50=0.0000, p90=0.1502, p10_price=29.5669, p50_price=34.3600, p90_price=39.9301, sample=3828, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0716, p10_price=32.0689, p50_price=34.3025, p90_price=36.9097, sample=3843, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0039, p90=0.1032, p10_price=31.0547, p50_price=34.2267, p90_price=38.0937, sample=3838, fallback=N/A
- 20D: p10=-0.1493, p50=-0.0033, p90=0.1430, p10_price=29.5937, p50_price=34.2482, p90_price=39.6430, sample=3828, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1128, p50=-0.0076, p90=0.0682, p10_price=30.6946, p50_price=34.0986, p90_price=36.7869, sample=91, fallback=NO
- 10D: p10=-0.1318, p50=0.0007, p90=0.1470, p10_price=30.1162, p50_price=34.3823, p90_price=39.8019, sample=89, fallback=NO
- 20D: p10=-0.1750, p50=0.0151, p90=0.1244, p10_price=28.8428, p50_price=34.8833, p90_price=38.9112, sample=88, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0795, p50=-0.0011, p90=0.0774, p10_price=31.7350, p50_price=34.3237, p90_price=37.1235, sample=3843, fallback=N/A
- 10D: p10=-0.1140, p50=-0.0021, p90=0.1098, p10_price=30.6591, p50_price=34.2891, p90_price=38.3489, sample=3838, fallback=N/A
- 20D: p10=-0.1621, p50=-0.0040, p90=0.1541, p10_price=29.2174, p50_price=34.2222, p90_price=40.0844, sample=3828, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-02T16:05:07.117498+00:00
- 数据快照: cnsvdata-2026-07-02-3828318b81f8
