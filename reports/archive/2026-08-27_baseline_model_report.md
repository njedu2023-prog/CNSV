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
- 最新交易日: 2026-08-26
- 最新收盘价: 34.1100
- 趋势状态: downtrend
- 波动率状态: low_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0707, p50=0.0000, p90=0.0707, p10_price=31.7802, p50_price=34.1100, p90_price=36.6106, sample=3882, fallback=N/A
- 10D: p10=-0.1001, p50=0.0000, p90=0.1001, p10_price=30.8624, p50_price=34.1100, p90_price=37.6993, sample=3877, fallback=N/A
- 20D: p10=-0.1415, p50=0.0000, p90=0.1415, p10_price=29.6095, p50_price=34.1100, p90_price=39.2945, sample=3867, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0715, p10_price=31.8353, p50_price=34.0530, p90_price=36.6375, sample=3882, fallback=N/A
- 10D: p10=-0.1012, p50=-0.0038, p90=0.1029, p10_price=30.8283, p50_price=33.9790, p90_price=37.8057, sample=3877, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0034, p90=0.1419, p10_price=29.3871, p50_price=33.9951, p90_price=39.3118, sample=3867, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0601, p50=0.0019, p90=0.0605, p10_price=32.1216, p50_price=34.1732, p90_price=36.2373, sample=80, fallback=NO
- 10D: p10=-0.1096, p50=-0.0042, p90=0.1009, p10_price=30.5688, p50_price=33.9684, p90_price=37.7299, sample=80, fallback=NO
- 20D: p10=-0.1316, p50=-0.0091, p90=0.1833, p10_price=29.9041, p50_price=33.8003, p90_price=40.9729, sample=80, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0437, p50=-0.0011, p90=0.0416, p10_price=32.6501, p50_price=34.0738, p90_price=35.5597, sample=3882, fallback=N/A
- 10D: p10=-0.0630, p50=-0.0022, p90=0.0587, p10_price=32.0279, p50_price=34.0367, p90_price=36.1715, sample=3877, fallback=N/A
- 20D: p10=-0.0900, p50=-0.0041, p90=0.0817, p10_price=31.1742, p50_price=33.9688, p90_price=37.0139, sample=3867, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-27T20:36:12.110531+00:00
- 数据快照: cnsvdata-2026-08-26-759127bad201
