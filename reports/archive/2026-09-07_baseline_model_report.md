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
- 最新交易日: 2026-09-07
- 最新收盘价: 38.3800
- 趋势状态: strong_uptrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0771, p50=0.0000, p90=0.0771, p10_price=35.5329, p50_price=38.3800, p90_price=41.4552, sample=3890, fallback=N/A
- 10D: p10=-0.1090, p50=0.0000, p90=0.1090, p10_price=34.4164, p50_price=38.3800, p90_price=42.8001, sample=3885, fallback=N/A
- 20D: p10=-0.1542, p50=0.0000, p90=0.1542, p10_price=32.8970, p50_price=38.3800, p90_price=44.7768, sample=3875, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0716, p10_price=35.8228, p50_price=38.3176, p90_price=41.2292, sample=3890, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0036, p90=0.1029, p10_price=34.6902, p50_price=38.2403, p90_price=42.5417, sample=3885, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0034, p90=0.1414, p10_price=33.0679, p50_price=38.2507, p90_price=44.2102, sample=3875, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1221, p50=-0.0055, p90=0.1311, p10_price=33.9670, p50_price=38.1709, p90_price=43.7559, sample=100, fallback=NO
- 10D: p10=-0.1583, p50=-0.0117, p90=0.2017, p10_price=32.7620, p50_price=37.9339, p90_price=46.9552, sample=100, fallback=NO
- 20D: p10=-0.2212, p50=0.0037, p90=0.2335, p10_price=30.7652, p50_price=38.5233, p90_price=48.4758, sample=100, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0724, p50=-0.0010, p90=0.0704, p10_price=35.7006, p50_price=38.3422, p90_price=41.1792, sample=3890, fallback=N/A
- 10D: p10=-0.1038, p50=-0.0020, p90=0.0997, p10_price=34.5974, p50_price=38.3016, p90_price=42.4025, sample=3885, fallback=N/A
- 20D: p10=-0.1476, p50=-0.0041, p90=0.1394, p10_price=33.1128, p50_price=38.2221, p90_price=44.1198, sample=3875, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-07T15:55:51.984031+00:00
- 数据快照: cnsvdata-2026-09-07-af99539c6b66
