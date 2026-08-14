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
- 最新交易日: 2026-08-14
- 最新收盘价: 33.4200
- 趋势状态: downtrend
- 波动率状态: low_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0715, p50=0.0000, p90=0.0715, p10_price=31.1137, p50_price=33.4200, p90_price=35.8972, sample=3874, fallback=N/A
- 10D: p10=-0.1011, p50=0.0000, p90=0.1011, p10_price=30.2057, p50_price=33.4200, p90_price=36.9763, sample=3869, fallback=N/A
- 20D: p10=-0.1430, p50=0.0000, p90=0.1430, p10_price=28.9666, p50_price=33.4200, p90_price=38.5581, sample=3859, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0716, p10_price=31.1910, p50_price=33.3642, p90_price=35.8995, sample=3874, fallback=N/A
- 10D: p10=-0.1013, p50=-0.0037, p90=0.1029, p10_price=30.2011, p50_price=33.2976, p90_price=37.0422, sample=3869, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0034, p90=0.1420, p10_price=28.7922, p50_price=33.3065, p90_price=38.5208, sample=3859, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0563, p50=-0.0012, p90=0.0474, p10_price=31.5891, p50_price=33.3783, p90_price=35.0438, sample=188, fallback=NO
- 10D: p10=-0.0891, p50=-0.0049, p90=0.0904, p10_price=30.5701, p50_price=33.2572, p90_price=36.5834, sample=188, fallback=NO
- 20D: p10=-0.1545, p50=-0.0177, p90=0.1341, p10_price=28.6359, p50_price=32.8342, p90_price=38.2148, sample=188, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0478, p50=-0.0011, p90=0.0457, p10_price=31.8603, p50_price=33.3849, p90_price=34.9823, sample=3874, fallback=N/A
- 10D: p10=-0.0687, p50=-0.0021, p90=0.0645, p10_price=31.2010, p50_price=33.3502, p90_price=35.6474, sample=3869, fallback=N/A
- 20D: p10=-0.0982, p50=-0.0042, p90=0.0899, p10_price=30.2946, p50_price=33.2811, p90_price=36.5620, sample=3859, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-14T12:24:46.757554+00:00
- 数据快照: cnsvdata-2026-08-14-16617095a372
