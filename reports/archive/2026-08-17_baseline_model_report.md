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
- 最新交易日: 2026-08-17
- 最新收盘价: 33.6500
- 趋势状态: downtrend
- 波动率状态: low_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0716, p50=0.0000, p90=0.0716, p10_price=31.3255, p50_price=33.6500, p90_price=36.1470, sample=3875, fallback=N/A
- 10D: p10=-0.1012, p50=0.0000, p90=0.1012, p10_price=30.4103, p50_price=33.6500, p90_price=37.2348, sample=3870, fallback=N/A
- 20D: p10=-0.1432, p50=0.0000, p90=0.1432, p10_price=29.1615, p50_price=33.6500, p90_price=38.8293, sample=3860, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0716, p10_price=31.4056, p50_price=33.5937, p90_price=36.1462, sample=3875, fallback=N/A
- 10D: p10=-0.1013, p50=-0.0037, p90=0.1029, p10_price=30.4096, p50_price=33.5247, p90_price=37.2967, sample=3870, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0034, p90=0.1420, p10_price=28.9906, p50_price=33.5360, p90_price=38.7853, sample=3860, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0501, p50=0.0012, p90=0.0458, p10_price=32.0062, p50_price=33.6893, p90_price=35.2256, sample=97, fallback=NO
- 10D: p10=-0.0829, p50=0.0104, p90=0.0784, p10_price=30.9715, p50_price=34.0031, p90_price=36.3927, sample=97, fallback=NO
- 20D: p10=-0.1019, p50=0.0263, p90=0.1248, p10_price=30.3899, p50_price=34.5451, p90_price=38.1233, sample=97, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0461, p50=-0.0011, p90=0.0439, p10_price=32.1349, p50_price=33.6143, p90_price=35.1618, sample=3875, fallback=N/A
- 10D: p10=-0.0662, p50=-0.0021, p90=0.0620, p10_price=31.4931, p50_price=33.5794, p90_price=35.8038, sample=3870, fallback=N/A
- 20D: p10=-0.0947, p50=-0.0042, p90=0.0864, p10_price=30.6098, p50_price=33.5103, p90_price=36.6857, sample=3860, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-17T12:24:45.556920+00:00
- 数据快照: cnsvdata-2026-08-17-f9237db6a733
