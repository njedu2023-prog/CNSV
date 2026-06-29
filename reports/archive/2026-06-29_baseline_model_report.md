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
- 最新交易日: 2026-06-29
- 最新收盘价: 33.5900
- 趋势状态: strong_downtrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0732, p50=0.0000, p90=0.0732, p10_price=31.2194, p50_price=33.5900, p90_price=36.1406, sample=3840, fallback=N/A
- 10D: p10=-0.1035, p50=0.0000, p90=0.1035, p10_price=30.2872, p50_price=33.5900, p90_price=37.2530, sample=3835, fallback=N/A
- 20D: p10=-0.1464, p50=0.0000, p90=0.1464, p10_price=29.0161, p50_price=33.5900, p90_price=38.8849, sample=3825, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0716, p10_price=31.3497, p50_price=33.5347, p90_price=36.0836, sample=3840, fallback=N/A
- 10D: p10=-0.1012, p50=-0.0038, p90=0.1033, p10_price=30.3576, p50_price=33.4630, p90_price=37.2456, sample=3835, fallback=N/A
- 20D: p10=-0.1494, p50=-0.0031, p90=0.1430, p10_price=28.9297, p50_price=33.4859, p90_price=38.7549, sample=3825, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0729, p50=0.0005, p90=0.0675, p10_price=31.2298, p50_price=33.6076, p90_price=35.9374, sample=152, fallback=NO
- 10D: p10=-0.0898, p50=-0.0016, p90=0.0919, p10_price=30.7048, p50_price=33.5365, p90_price=36.8246, sample=152, fallback=NO
- 20D: p10=-0.1784, p50=-0.0038, p90=0.1315, p10_price=28.1028, p50_price=33.4612, p90_price=38.3091, sample=150, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0722, p50=-0.0010, p90=0.0702, p10_price=31.2496, p50_price=33.5553, p90_price=36.0311, sample=3840, fallback=N/A
- 10D: p10=-0.1036, p50=-0.0020, p90=0.0996, p10_price=30.2840, p50_price=33.5221, p90_price=37.1063, sample=3835, fallback=N/A
- 20D: p10=-0.1475, p50=-0.0040, p90=0.1396, p10_price=28.9829, p50_price=33.4567, p90_price=38.6211, sample=3825, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-06-29T16:52:49.129070+00:00
- 数据快照: cnsvdata-2026-06-29-d9c53da4c68b
