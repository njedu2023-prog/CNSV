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
- 最新交易日: 2026-07-28
- 最新收盘价: 33.4900
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0762, p50=0.0000, p90=0.0762, p10_price=31.0322, p50_price=33.4900, p90_price=36.1425, sample=3861, fallback=N/A
- 10D: p10=-0.1078, p50=0.0000, p90=0.1078, p10_price=30.0678, p50_price=33.4900, p90_price=37.3018, sample=3856, fallback=N/A
- 20D: p10=-0.1524, p50=0.0000, p90=0.1524, p10_price=28.7548, p50_price=33.4900, p90_price=39.0050, sample=3846, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0017, p90=0.0716, p10_price=31.2529, p50_price=33.4340, p90_price=35.9769, sample=3861, fallback=N/A
- 10D: p10=-0.1016, p50=-0.0040, p90=0.1030, p10_price=30.2552, p50_price=33.3578, p90_price=37.1234, sample=3856, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0034, p90=0.1424, p10_price=28.8501, p50_price=33.3770, p90_price=38.6159, sample=3846, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1034, p50=-0.0076, p90=0.0659, p10_price=30.1989, p50_price=33.2353, p90_price=35.7705, sample=95, fallback=NO
- 10D: p10=-0.1299, p50=0.0007, p90=0.1428, p10_price=29.4095, p50_price=33.5118, p90_price=38.6323, sample=93, fallback=NO
- 20D: p10=-0.1588, p50=0.0096, p90=0.1191, p10_price=28.5713, p50_price=33.8130, p90_price=37.7275, sample=91, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0994, p50=-0.0011, p90=0.0973, p10_price=30.3199, p50_price=33.4539, p90_price=36.9118, sample=3861, fallback=N/A
- 10D: p10=-0.1424, p50=-0.0022, p90=0.1380, p10_price=29.0458, p50_price=33.4168, p90_price=38.4455, sample=3856, fallback=N/A
- 20D: p10=-0.2020, p50=-0.0041, p90=0.1938, p10_price=27.3635, p50_price=33.3525, p90_price=40.6523, sample=3846, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-28T12:24:54.931383+00:00
- 数据快照: cnsvdata-2026-07-28-abe5c3e7f153
