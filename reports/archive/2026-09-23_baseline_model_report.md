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
- 最新交易日: 2026-09-23
- 最新收盘价: 38.5900
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0746, p50=0.0000, p90=0.0746, p10_price=35.8159, p50_price=38.5900, p90_price=41.5790, sample=3902, fallback=N/A
- 10D: p10=-0.1055, p50=0.0000, p90=0.1055, p10_price=34.7261, p50_price=38.5900, p90_price=42.8839, sample=3897, fallback=N/A
- 20D: p10=-0.1492, p50=0.0000, p90=0.1492, p10_price=33.2412, p50_price=38.5900, p90_price=44.7995, sample=3887, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0688, p50=-0.0016, p90=0.0719, p10_price=36.0251, p50_price=38.5288, p90_price=41.4666, sample=3902, fallback=N/A
- 10D: p10=-0.1008, p50=-0.0036, p90=0.1039, p10_price=34.8901, p50_price=38.4514, p90_price=42.8170, sample=3897, fallback=N/A
- 20D: p10=-0.1488, p50=-0.0028, p90=0.1433, p10_price=33.2533, p50_price=38.4803, p90_price=44.5337, sample=3887, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0782, p50=-0.0070, p90=0.0841, p10_price=35.6877, p50_price=38.3191, p90_price=41.9740, sample=194, fallback=NO
- 10D: p10=-0.1153, p50=-0.0201, p90=0.0829, p10_price=34.3887, p50_price=37.8236, p90_price=41.9242, sample=191, fallback=NO
- 20D: p10=-0.1611, p50=-0.0327, p90=0.1261, p10_price=32.8482, p50_price=37.3486, p90_price=43.7754, sample=191, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0895, p50=-0.0008, p90=0.0878, p10_price=35.2849, p50_price=38.5573, p90_price=42.1332, sample=3902, fallback=N/A
- 10D: p10=-0.1281, p50=-0.0017, p90=0.1246, p10_price=33.9506, p50_price=38.5232, p90_price=43.7115, sample=3897, fallback=N/A
- 20D: p10=-0.1819, p50=-0.0036, p90=0.1746, p10_price=32.1726, p50_price=38.4503, p90_price=45.9530, sample=3887, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-23T15:06:12.928062+00:00
- 数据快照: cnsvdata-2026-09-23-c432b80fbdd4
