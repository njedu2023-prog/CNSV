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
- 最新交易日: 2026-10-30
- 最新收盘价: 33.3900
- 趋势状态: strong_downtrend
- 波动率状态: normal_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0656, p50=0.0000, p90=0.0656, p10_price=31.2692, p50_price=33.3900, p90_price=35.6547, sample=3923, fallback=N/A
- 10D: p10=-0.0928, p50=0.0000, p90=0.0928, p10_price=30.4307, p50_price=33.3900, p90_price=36.6371, sample=3918, fallback=N/A
- 20D: p10=-0.1312, p50=0.0000, p90=0.1312, p10_price=29.2831, p50_price=33.3900, p90_price=38.0729, sample=3908, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0716, p10_price=31.1635, p50_price=33.3325, p90_price=35.8678, sample=3923, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0038, p90=0.1035, p10_price=30.1780, p50_price=33.2630, p90_price=37.0314, sample=3918, fallback=N/A
- 20D: p10=-0.1488, p50=-0.0031, p90=0.1431, p10_price=28.7726, p50_price=33.2853, p90_price=38.5268, sample=3908, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0648, p50=0.0004, p90=0.0578, p10_price=31.2938, p50_price=33.4022, p90_price=35.3771, sample=63, fallback=NO
- 10D: p10=-0.0828, p50=0.0077, p90=0.1111, p10_price=30.7363, p50_price=33.6471, p90_price=37.3147, sample=63, fallback=NO
- 20D: p10=-0.1404, p50=0.0271, p90=0.1097, p10_price=29.0167, p50_price=34.3084, p90_price=37.2598, sample=63, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0692, p50=-0.0010, p90=0.0671, p10_price=31.1589, p50_price=33.3556, p90_price=35.7071, sample=3923, fallback=N/A
- 10D: p10=-0.0991, p50=-0.0020, p90=0.0950, p10_price=30.2390, p50_price=33.3217, p90_price=36.7185, sample=3918, fallback=N/A
- 20D: p10=-0.1408, p50=-0.0038, p90=0.1332, p10_price=29.0057, p50_price=33.2638, p90_price=38.1469, sample=3908, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-10-31T15:47:31.581358+00:00
- 数据快照: cnsvdata-2026-10-30-e4b07ef535de
