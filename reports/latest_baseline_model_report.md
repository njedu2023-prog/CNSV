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
- 最新交易日: 2026-08-10
- 最新收盘价: 34.8300
- 趋势状态: uptrend
- 波动率状态: normal_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0755, p50=0.0000, p90=0.0755, p10_price=32.2968, p50_price=34.8300, p90_price=37.5619, sample=3870, fallback=N/A
- 10D: p10=-0.1068, p50=0.0000, p90=0.1068, p10_price=31.3022, p50_price=34.8300, p90_price=38.7553, sample=3865, fallback=N/A
- 20D: p10=-0.1510, p50=0.0000, p90=0.1510, p10_price=29.9478, p50_price=34.8300, p90_price=40.5081, sample=3855, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0716, p10_price=32.5065, p50_price=34.7733, p90_price=37.4156, sample=3870, fallback=N/A
- 10D: p10=-0.1014, p50=-0.0036, p90=0.1029, p10_price=31.4723, p50_price=34.7033, p90_price=38.6067, sample=3865, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0035, p90=0.1421, p10_price=30.0061, p50_price=34.7070, p90_price=40.1485, sample=3855, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0689, p50=-0.0070, p90=0.0668, p10_price=32.5107, p50_price=34.5886, p90_price=37.2366, sample=148, fallback=NO
- 10D: p10=-0.1071, p50=-0.0125, p90=0.0790, p10_price=31.2931, p50_price=34.3957, p90_price=37.6928, sample=148, fallback=NO
- 20D: p10=-0.1514, p50=-0.0109, p90=0.1003, p10_price=29.9359, p50_price=34.4535, p90_price=38.5049, sample=148, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0550, p50=-0.0010, p90=0.0530, p10_price=32.9649, p50_price=34.7945, p90_price=36.7256, sample=3870, fallback=N/A
- 10D: p10=-0.0791, p50=-0.0021, p90=0.0749, p10_price=32.1825, p50_price=34.7580, p90_price=37.5395, sample=3865, fallback=N/A
- 20D: p10=-0.1128, p50=-0.0042, p90=0.1045, p10_price=31.1132, p50_price=34.6846, p90_price=38.6660, sample=3855, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-10T12:29:39.918314+00:00
- 数据快照: cnsvdata-2026-08-10-24f43be9527f
