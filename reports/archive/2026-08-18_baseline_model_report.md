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
- 最新交易日: 2026-08-18
- 最新收盘价: 33.4900
- 趋势状态: downtrend
- 波动率状态: low_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0715, p50=0.0000, p90=0.0715, p10_price=31.1800, p50_price=33.4900, p90_price=35.9712, sample=3876, fallback=N/A
- 10D: p10=-0.1011, p50=0.0000, p90=0.1011, p10_price=30.2704, p50_price=33.4900, p90_price=37.0520, sample=3871, fallback=N/A
- 20D: p10=-0.1429, p50=0.0000, p90=0.1429, p10_price=29.0293, p50_price=33.4900, p90_price=38.6362, sample=3861, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0715, p10_price=31.2563, p50_price=33.4339, p90_price=35.9738, sample=3876, fallback=N/A
- 10D: p10=-0.1012, p50=-0.0038, p90=0.1029, p10_price=30.2657, p50_price=33.3633, p90_price=37.1189, sample=3871, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0034, p90=0.1420, p10_price=28.8529, p50_price=33.3769, p90_price=38.6003, sample=3861, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0563, p50=-0.0012, p90=0.0474, p10_price=31.6553, p50_price=33.4482, p90_price=35.1172, sample=188, fallback=NO
- 10D: p10=-0.0891, p50=-0.0049, p90=0.0904, p10_price=30.6341, p50_price=33.3268, p90_price=36.6600, sample=188, fallback=NO
- 20D: p10=-0.1545, p50=-0.0177, p90=0.1341, p10_price=28.6959, p50_price=32.9030, p90_price=38.2949, sample=188, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0462, p50=-0.0011, p90=0.0441, p10_price=31.9776, p50_price=33.4544, p90_price=34.9993, sample=3876, fallback=N/A
- 10D: p10=-0.0664, p50=-0.0021, p90=0.0622, p10_price=31.3370, p50_price=33.4195, p90_price=35.6403, sample=3871, fallback=N/A
- 20D: p10=-0.0950, p50=-0.0042, p90=0.0867, p10_price=30.4560, p50_price=33.3511, p90_price=36.5215, sample=3861, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-18T12:29:48.820021+00:00
- 数据快照: cnsvdata-2026-08-18-3fca4c1cf0bc
