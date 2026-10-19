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
- 最新交易日: 2026-10-16
- 最新收盘价: 35.7700
- 趋势状态: strong_downtrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0667, p50=0.0000, p90=0.0667, p10_price=33.4614, p50_price=35.7700, p90_price=38.2379, sample=3913, fallback=N/A
- 10D: p10=-0.0944, p50=0.0000, p90=0.0944, p10_price=32.5493, p50_price=35.7700, p90_price=39.3094, sample=3908, fallback=N/A
- 20D: p10=-0.1334, p50=0.0000, p90=0.1334, p10_price=31.3018, p50_price=35.7700, p90_price=40.8761, sample=3898, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0689, p50=-0.0016, p90=0.0716, p10_price=33.3881, p50_price=35.7118, p90_price=38.4261, sample=3913, fallback=N/A
- 10D: p10=-0.1004, p50=-0.0036, p90=0.1036, p10_price=32.3532, p50_price=35.6410, p90_price=39.6751, sample=3908, fallback=N/A
- 20D: p10=-0.1487, p50=-0.0026, p90=0.1433, p10_price=30.8272, p50_price=35.6754, p90_price=41.2793, sample=3898, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0710, p50=0.0009, p90=0.0724, p10_price=33.3192, p50_price=35.8009, p90_price=38.4539, sample=154, fallback=NO
- 10D: p10=-0.0898, p50=-0.0010, p90=0.0923, p10_price=32.6976, p50_price=35.7345, p90_price=39.2292, sample=154, fallback=NO
- 20D: p10=-0.1753, p50=-0.0038, p90=0.1309, p10_price=30.0181, p50_price=35.6328, p90_price=40.7715, sample=154, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0822, p50=-0.0009, p90=0.0804, p10_price=32.9459, p50_price=35.7370, p90_price=38.7646, sample=3913, fallback=N/A
- 10D: p10=-0.1176, p50=-0.0018, p90=0.1140, p10_price=31.8006, p50_price=35.7052, p90_price=40.0892, sample=3908, fallback=N/A
- 20D: p10=-0.1670, p50=-0.0035, p90=0.1600, p10_price=30.2699, p50_price=35.6454, p90_price=41.9755, sample=3898, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-10-19T19:23:34.218837+00:00
- 数据快照: cnsvdata-2026-10-16-28295e80612f
