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
- 最新交易日: 2026-07-09
- 最新收盘价: 36.0600
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0796, p50=0.0000, p90=0.0796, p10_price=33.3016, p50_price=36.0600, p90_price=39.0468, sample=3848, fallback=N/A
- 10D: p10=-0.1125, p50=0.0000, p90=0.1125, p10_price=32.2218, p50_price=36.0600, p90_price=40.3554, sample=3843, fallback=N/A
- 20D: p10=-0.1592, p50=0.0000, p90=0.1592, p10_price=30.7543, p50_price=36.0600, p90_price=42.2811, sample=3833, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0719, p10_price=33.6569, p50_price=36.0013, p90_price=38.7500, sample=3848, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0037, p90=0.1030, p10_price=32.5928, p50_price=35.9279, p90_price=39.9724, sample=3843, fallback=N/A
- 20D: p10=-0.1493, p50=-0.0029, p90=0.1429, p10_price=31.0596, p50_price=35.9549, p90_price=41.6012, sample=3833, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0774, p50=-0.0070, p90=0.0863, p10_price=33.3744, p50_price=35.8095, p90_price=39.3119, sample=186, fallback=NO
- 10D: p10=-0.1155, p50=-0.0163, p90=0.0840, p10_price=32.1265, p50_price=35.4766, p90_price=39.2198, sample=186, fallback=NO
- 20D: p10=-0.1657, p50=-0.0385, p90=0.1301, p10_price=30.5525, p50_price=34.6993, p90_price=41.0699, sample=186, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0959, p50=-0.0010, p90=0.0940, p10_price=32.7626, p50_price=36.0256, p90_price=39.6135, sample=3848, fallback=N/A
- 10D: p10=-0.1374, p50=-0.0020, p90=0.1333, p10_price=31.4316, p50_price=35.9868, p90_price=41.2021, sample=3843, fallback=N/A
- 20D: p10=-0.1952, p50=-0.0040, p90=0.1873, p10_price=29.6655, p50_price=35.9173, p90_price=43.4867, sample=3833, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-09T16:41:38.373435+00:00
- 数据快照: cnsvdata-2026-07-09-5aef277f9b1f
