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
- 最新交易日: 2026-08-07
- 最新收盘价: 34.8500
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0756, p50=0.0000, p90=0.0756, p10_price=32.3121, p50_price=34.8500, p90_price=37.5873, sample=3869, fallback=N/A
- 10D: p10=-0.1069, p50=0.0000, p90=0.1069, p10_price=31.3158, p50_price=34.8500, p90_price=38.7831, sample=3864, fallback=N/A
- 20D: p10=-0.1512, p50=0.0000, p90=0.1512, p10_price=29.9590, p50_price=34.8500, p90_price=40.5395, sample=3854, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0716, p10_price=32.5248, p50_price=34.7933, p90_price=37.4372, sample=3869, fallback=N/A
- 10D: p10=-0.1014, p50=-0.0037, p90=0.1030, p10_price=31.4896, p50_price=34.7228, p90_price=38.6293, sample=3864, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0037, p90=0.1421, p10_price=30.0231, p50_price=34.7199, p90_price=40.1722, sample=3854, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0797, p50=-0.0070, p90=0.0863, p10_price=32.1808, p50_price=34.6054, p90_price=37.9927, sample=187, fallback=NO
- 10D: p10=-0.1155, p50=-0.0167, p90=0.0838, p10_price=31.0499, p50_price=34.2719, p90_price=37.8952, sample=187, fallback=NO
- 20D: p10=-0.1648, p50=-0.0361, p90=0.1293, p10_price=29.5548, p50_price=33.6152, p90_price=39.6600, sample=187, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0756, p50=-0.0010, p90=0.0736, p10_price=32.3114, p50_price=34.8145, p90_price=37.5116, sample=3869, fallback=N/A
- 10D: p10=-0.1084, p50=-0.0021, p90=0.1043, p10_price=31.2691, p50_price=34.7776, p90_price=38.6797, sample=3864, fallback=N/A
- 20D: p10=-0.1543, p50=-0.0042, p90=0.1459, p10_price=29.8671, p50_price=34.7043, p90_price=40.3249, sample=3854, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-07T12:24:44.409927+00:00
- 数据快照: cnsvdata-2026-08-07-b72389af014e
