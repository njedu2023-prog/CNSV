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
- 最新交易日: 2026-09-24
- 最新收盘价: 38.0900
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0742, p50=0.0000, p90=0.0742, p10_price=35.3662, p50_price=38.0900, p90_price=41.0236, sample=3903, fallback=N/A
- 10D: p10=-0.1049, p50=0.0000, p90=0.1049, p10_price=34.2958, p50_price=38.0900, p90_price=42.3039, sample=3898, fallback=N/A
- 20D: p10=-0.1484, p50=0.0000, p90=0.1484, p10_price=32.8372, p50_price=38.0900, p90_price=44.1831, sample=3888, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0688, p50=-0.0016, p90=0.0719, p10_price=35.5583, p50_price=38.0293, p90_price=40.9282, sample=3903, fallback=N/A
- 10D: p10=-0.1007, p50=-0.0036, p90=0.1039, p10_price=34.4395, p50_price=37.9532, p90_price=42.2609, sample=3898, fallback=N/A
- 20D: p10=-0.1488, p50=-0.0028, p90=0.1433, p10_price=32.8226, p50_price=37.9834, p90_price=43.9566, sample=3888, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0782, p50=-0.0070, p90=0.0841, p10_price=35.2253, p50_price=37.8226, p90_price=41.4301, sample=194, fallback=NO
- 10D: p10=-0.1153, p50=-0.0201, p90=0.0829, p10_price=33.9431, p50_price=37.3335, p90_price=41.3810, sample=191, fallback=NO
- 20D: p10=-0.1611, p50=-0.0327, p90=0.1261, p10_price=32.4226, p50_price=36.8647, p90_price=43.2082, sample=191, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0904, p50=-0.0009, p90=0.0887, p10_price=34.7984, p50_price=38.0575, p90_price=41.6219, sample=3903, fallback=N/A
- 10D: p10=-0.1293, p50=-0.0018, p90=0.1258, p10_price=33.4700, p50_price=38.0234, p90_price=43.1963, sample=3898, fallback=N/A
- 20D: p10=-0.1835, p50=-0.0036, p90=0.1763, p10_price=31.7028, p50_price=37.9531, p90_price=45.4358, sample=3888, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-24T15:15:25.478119+00:00
- 数据快照: cnsvdata-2026-09-24-e6aca438d85f
