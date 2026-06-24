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
- 最新交易日: 2026-06-23
- 最新收盘价: 35.8100
- 趋势状态: downtrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0714, p50=0.0000, p90=0.0714, p10_price=33.3421, p50_price=35.8100, p90_price=38.4606, sample=3836, fallback=N/A
- 10D: p10=-0.1010, p50=0.0000, p90=0.1010, p10_price=32.3703, p50_price=35.8100, p90_price=39.6152, sample=3831, fallback=N/A
- 20D: p10=-0.1428, p50=0.0000, p90=0.1428, p10_price=31.0442, p50_price=35.8100, p90_price=41.3074, sample=3821, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0689, p50=-0.0016, p90=0.0716, p10_price=33.4271, p50_price=35.7523, p90_price=38.4688, sample=3836, fallback=N/A
- 10D: p10=-0.1012, p50=-0.0038, p90=0.1035, p10_price=32.3624, p50_price=35.6746, p90_price=39.7150, sample=3831, fallback=N/A
- 20D: p10=-0.1494, p50=-0.0028, p90=0.1430, p10_price=30.8407, p50_price=35.7082, p90_price=41.3165, sample=3821, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1134, p50=-0.0076, p90=0.0693, p10_price=31.9707, p50_price=35.5376, p90_price=38.3788, sample=89, fallback=NO
- 10D: p10=-0.1318, p50=0.0007, p90=0.1470, p10_price=31.3871, p50_price=35.8333, p90_price=41.4816, sample=89, fallback=NO
- 20D: p10=-0.1750, p50=0.0151, p90=0.1244, p10_price=30.0599, p50_price=36.3553, p90_price=40.5532, sample=88, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0667, p50=-0.0010, p90=0.0647, p10_price=33.5002, p50_price=35.7753, p90_price=38.2048, sample=3836, fallback=N/A
- 10D: p10=-0.0958, p50=-0.0020, p90=0.0918, p10_price=32.5378, p50_price=35.7379, p90_price=39.2527, sample=3831, fallback=N/A
- 20D: p10=-0.1364, p50=-0.0039, p90=0.1287, p10_price=31.2440, p50_price=35.6715, p90_price=40.7266, sample=3821, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-06-24T03:31:00.419670+00:00
- 数据快照: cnsvdata-2026-06-23-f91718793826
