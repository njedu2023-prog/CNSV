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
- 最新交易日: 2026-06-22
- 最新收盘价: 37.3300
- 趋势状态: uptrend
- 波动率状态: normal_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0696, p50=0.0000, p90=0.0696, p10_price=34.8194, p50_price=37.3300, p90_price=40.0216, sample=3835, fallback=N/A
- 10D: p10=-0.0985, p50=0.0000, p90=0.0985, p10_price=33.8296, p50_price=37.3300, p90_price=41.1926, sample=3830, fallback=N/A
- 20D: p10=-0.1392, p50=0.0000, p90=0.1392, p10_price=32.4777, p50_price=37.3300, p90_price=42.9073, sample=3820, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0689, p50=-0.0016, p90=0.0716, p10_price=34.8454, p50_price=37.2705, p90_price=40.1017, sample=3835, fallback=N/A
- 10D: p10=-0.1013, p50=-0.0038, p90=0.1035, p10_price=33.7352, p50_price=37.1877, p90_price=41.4009, sample=3830, fallback=N/A
- 20D: p10=-0.1494, p50=-0.0028, p90=0.1431, p10_price=32.1494, p50_price=37.2255, p90_price=43.0711, sample=3820, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0747, p50=-0.0155, p90=0.0753, p10_price=34.6424, p50_price=36.7569, p90_price=40.2511, sample=46, fallback=NO
- 10D: p10=-0.0796, p50=-0.0178, p90=0.1127, p10_price=34.4725, p50_price=36.6707, p90_price=41.7831, sample=46, fallback=NO
- 20D: p10=-0.1116, p50=0.0051, p90=0.1399, p10_price=33.3892, p50_price=37.5209, p90_price=42.9375, sample=46, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0616, p50=-0.0010, p90=0.0597, p10_price=35.0997, p50_price=37.2938, p90_price=39.6251, sample=3835, fallback=N/A
- 10D: p10=-0.0886, p50=-0.0020, p90=0.0845, p10_price=34.1651, p50_price=37.2545, p90_price=40.6234, sample=3830, fallback=N/A
- 20D: p10=-0.1262, p50=-0.0039, p90=0.1184, p10_price=32.9054, p50_price=37.1862, p90_price=42.0238, sample=3820, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-06-23T05:26:20.102976+00:00
- 数据快照: cnsvdata-2026-06-22-691897aa5146
