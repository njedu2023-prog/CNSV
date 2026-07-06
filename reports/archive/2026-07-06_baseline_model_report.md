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
- 最新交易日: 2026-07-06
- 最新收盘价: 37.6400
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0784, p50=0.0000, p90=0.0784, p10_price=34.8012, p50_price=37.6400, p90_price=40.7104, sample=3845, fallback=N/A
- 10D: p10=-0.1109, p50=0.0000, p90=0.1109, p10_price=33.6890, p50_price=37.6400, p90_price=42.0544, sample=3840, fallback=N/A
- 20D: p10=-0.1568, p50=0.0000, p90=0.1568, p10_price=32.1765, p50_price=37.6400, p90_price=44.0312, sample=3830, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0718, p10_price=35.1307, p50_price=37.5772, p90_price=40.4422, sample=3845, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0038, p90=0.1031, p10_price=34.0200, p50_price=37.4965, p90_price=41.7260, sample=3840, fallback=N/A
- 20D: p10=-0.1493, p50=-0.0032, p90=0.1430, p10_price=32.4192, p50_price=37.5211, p90_price=43.4272, sample=3830, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0705, p50=-0.0011, p90=0.0745, p10_price=35.0776, p50_price=37.5986, p90_price=40.5533, sample=74, fallback=NO
- 10D: p10=-0.0953, p50=-0.0165, p90=0.0796, p10_price=34.2176, p50_price=37.0258, p90_price=40.7595, sample=74, fallback=NO
- 20D: p10=-0.1543, p50=-0.0197, p90=0.1454, p10_price=32.2579, p50_price=36.9051, p90_price=43.5317, sample=74, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0951, p50=-0.0010, p90=0.0931, p10_price=34.2245, p50_price=37.6024, p90_price=41.3137, sample=3845, fallback=N/A
- 10D: p10=-0.1363, p50=-0.0021, p90=0.1322, p10_price=32.8447, p50_price=37.5628, p90_price=42.9585, sample=3840, fallback=N/A
- 20D: p10=-0.1937, p50=-0.0040, p90=0.1857, p10_price=31.0131, p50_price=37.4897, p90_price=45.3188, sample=3830, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-06T16:51:37.340296+00:00
- 数据快照: cnsvdata-2026-07-06-8c729029a501
