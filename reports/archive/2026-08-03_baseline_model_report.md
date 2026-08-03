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
- 最新交易日: 2026-08-03
- 最新收盘价: 35.1000
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0772, p50=0.0000, p90=0.0772, p10_price=32.4917, p50_price=35.1000, p90_price=37.9177, sample=3865, fallback=N/A
- 10D: p10=-0.1092, p50=0.0000, p90=0.1092, p10_price=31.4689, p50_price=35.1000, p90_price=39.1501, sample=3860, fallback=N/A
- 20D: p10=-0.1544, p50=0.0000, p90=0.1544, p10_price=30.0772, p50_price=35.1000, p90_price=40.9616, sample=3850, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0016, p90=0.0716, p10_price=32.7568, p50_price=35.0429, p90_price=37.7061, sample=3865, fallback=N/A
- 10D: p10=-0.1015, p50=-0.0038, p90=0.1030, p10_price=31.7126, p50_price=34.9662, p90_price=38.9078, sample=3860, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0034, p90=0.1422, p10_price=30.2377, p50_price=34.9811, p90_price=40.4642, sample=3850, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0797, p50=-0.0070, p90=0.0863, p10_price=32.4117, p50_price=34.8537, p90_price=38.2653, sample=187, fallback=NO
- 10D: p10=-0.1155, p50=-0.0167, p90=0.0838, p10_price=31.2727, p50_price=34.5177, p90_price=38.1670, sample=187, fallback=NO
- 20D: p10=-0.1657, p50=-0.0385, p90=0.1301, p10_price=29.7392, p50_price=33.7755, p90_price=39.9766, sample=186, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0794, p50=-0.0010, p90=0.0774, p10_price=32.4196, p50_price=35.0639, p90_price=37.9237, sample=3865, fallback=N/A
- 10D: p10=-0.1139, p50=-0.0021, p90=0.1096, p10_price=31.3224, p50_price=35.0252, p90_price=39.1657, sample=3860, fallback=N/A
- 20D: p10=-0.1619, p50=-0.0041, p90=0.1536, p10_price=29.8543, p50_price=34.9549, p90_price=40.9269, sample=3850, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-03T13:22:36.191553+00:00
- 数据快照: cnsvdata-2026-08-03-51ed10774c34
