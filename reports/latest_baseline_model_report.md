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
- 最新交易日: 2026-06-30
- 最新收盘价: 33.7900
- 趋势状态: strong_downtrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0731, p50=0.0000, p90=0.0731, p10_price=31.4066, p50_price=33.7900, p90_price=36.3543, sample=3841, fallback=N/A
- 10D: p10=-0.1034, p50=0.0000, p90=0.1034, p10_price=30.4693, p50_price=33.7900, p90_price=37.4727, sample=3836, fallback=N/A
- 20D: p10=-0.1463, p50=0.0000, p90=0.1463, p10_price=29.1913, p50_price=33.7900, p90_price=39.1132, sample=3826, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0716, p10_price=31.5364, p50_price=33.7337, p90_price=36.2983, sample=3841, fallback=N/A
- 10D: p10=-0.1012, p50=-0.0038, p90=0.1033, p10_price=30.5387, p50_price=33.6612, p90_price=37.4655, sample=3836, fallback=N/A
- 20D: p10=-0.1493, p50=-0.0032, p90=0.1430, p10_price=29.1022, p50_price=33.6833, p90_price=38.9855, sample=3826, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1425, p50=0.0089, p90=0.0784, p10_price=29.3015, p50_price=34.0920, p90_price=36.5449, sample=68, fallback=NO
- 10D: p10=-0.1048, p50=0.0005, p90=0.1253, p10_price=30.4286, p50_price=33.8064, p90_price=38.3020, sample=68, fallback=NO
- 20D: p10=-0.2033, p50=-0.0169, p90=0.1592, p10_price=27.5739, p50_price=33.2230, p90_price=39.6230, sample=65, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0721, p50=-0.0010, p90=0.0700, p10_price=31.4402, p50_price=33.7546, p90_price=36.2393, sample=3841, fallback=N/A
- 10D: p10=-0.1034, p50=-0.0020, p90=0.0993, p10_price=30.4710, p50_price=33.7212, p90_price=37.3180, sample=3836, fallback=N/A
- 20D: p10=-0.1472, p50=-0.0040, p90=0.1392, p10_price=29.1645, p50_price=33.6552, p90_price=38.8374, sample=3826, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-06-30T16:32:03.155453+00:00
- 数据快照: cnsvdata-2026-06-30-3b979aad980c
