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
- 最新交易日: 2026-06-25
- 最新收盘价: 35.3300
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0700, p50=0.0000, p90=0.0700, p10_price=32.9405, p50_price=35.3300, p90_price=37.8928, sample=3838, fallback=N/A
- 10D: p10=-0.0990, p50=0.0000, p90=0.0990, p10_price=31.9987, p50_price=35.3300, p90_price=39.0081, sample=3833, fallback=N/A
- 20D: p10=-0.1401, p50=0.0000, p90=0.1401, p10_price=30.7127, p50_price=35.3300, p90_price=40.6415, sample=3823, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0688, p50=-0.0016, p90=0.0716, p10_price=32.9801, p50_price=35.2725, p90_price=37.9529, sample=3838, fallback=N/A
- 10D: p10=-0.1012, p50=-0.0037, p90=0.1034, p10_price=31.9294, p50_price=35.2006, p90_price=39.1788, sample=3833, fallback=N/A
- 20D: p10=-0.1494, p50=-0.0029, p90=0.1430, p10_price=30.4278, p50_price=35.2270, p90_price=40.7626, sample=3823, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0806, p50=-0.0038, p90=0.0847, p10_price=32.5930, p50_price=35.1967, p90_price=38.4511, sample=172, fallback=NO
- 10D: p10=-0.1188, p50=-0.0068, p90=0.1188, p10_price=31.3723, p50_price=35.0903, p90_price=39.7855, sample=172, fallback=NO
- 20D: p10=-0.1593, p50=0.0037, p90=0.1554, p10_price=30.1280, p50_price=35.4616, p90_price=41.2713, sample=172, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0643, p50=-0.0010, p90=0.0623, p10_price=33.1306, p50_price=35.2951, p90_price=37.6012, sample=3838, fallback=N/A
- 10D: p10=-0.0924, p50=-0.0020, p90=0.0883, p10_price=32.2130, p50_price=35.2592, p90_price=38.5933, sample=3833, fallback=N/A
- 20D: p10=-0.1316, p50=-0.0039, p90=0.1237, p10_price=30.9744, p50_price=35.1920, p90_price=39.9838, sample=3823, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-06-25T16:36:50.616937+00:00
- 数据快照: cnsvdata-2026-06-25-813c4c0ad64f
