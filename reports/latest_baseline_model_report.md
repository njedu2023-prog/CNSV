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
- 最新交易日: 2026-08-20
- 最新收盘价: 32.9900
- 趋势状态: strong_downtrend
- 波动率状态: low_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0708, p50=0.0000, p90=0.0708, p10_price=30.7349, p50_price=32.9900, p90_price=35.4105, sample=3878, fallback=N/A
- 10D: p10=-0.1001, p50=0.0000, p90=0.1001, p10_price=29.8466, p50_price=32.9900, p90_price=36.4645, sample=3873, fallback=N/A
- 20D: p10=-0.1416, p50=0.0000, p90=0.1416, p10_price=28.6340, p50_price=32.9900, p90_price=38.0087, sample=3863, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0715, p10_price=30.7897, p50_price=32.9345, p90_price=35.4359, sample=3878, fallback=N/A
- 10D: p10=-0.1012, p50=-0.0038, p90=0.1029, p10_price=29.8146, p50_price=32.8633, p90_price=36.5646, sample=3873, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0034, p90=0.1420, p10_price=28.4222, p50_price=32.8785, p90_price=38.0230, sample=3863, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0748, p50=-0.0026, p90=0.0733, p10_price=30.6118, p50_price=32.9054, p90_price=35.5003, sample=57, fallback=NO
- 10D: p10=-0.0885, p50=0.0007, p90=0.0994, p10_price=30.1947, p50_price=33.0136, p90_price=36.4395, sample=57, fallback=NO
- 20D: p10=-0.1051, p50=0.0026, p90=0.1074, p10_price=29.6991, p50_price=33.0746, p90_price=36.7300, sample=57, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0442, p50=-0.0011, p90=0.0421, p10_price=31.5631, p50_price=32.9545, p90_price=34.4073, sample=3878, fallback=N/A
- 10D: p10=-0.0636, p50=-0.0021, p90=0.0593, p10_price=30.9565, p50_price=32.9196, p90_price=35.0071, sample=3873, fallback=N/A
- 20D: p10=-0.0909, p50=-0.0042, p90=0.0826, p10_price=30.1225, p50_price=32.8531, p90_price=35.8312, sample=3863, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-20T12:29:44.856421+00:00
- 数据快照: cnsvdata-2026-08-20-bcc99b2d6f98
