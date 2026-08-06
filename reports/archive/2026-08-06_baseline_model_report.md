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
- 最新交易日: 2026-08-06
- 最新收盘价: 34.9000
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0767, p50=0.0000, p90=0.0767, p10_price=32.3220, p50_price=34.9000, p90_price=37.6836, sample=3868, fallback=N/A
- 10D: p10=-0.1085, p50=0.0000, p90=0.1085, p10_price=31.3108, p50_price=34.9000, p90_price=38.9006, sample=3863, fallback=N/A
- 20D: p10=-0.1535, p50=0.0000, p90=0.1535, p10_price=29.9345, p50_price=34.9000, p90_price=40.6892, sample=3853, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0016, p90=0.0716, p10_price=32.5712, p50_price=34.8438, p90_price=37.4910, sample=3868, fallback=N/A
- 10D: p10=-0.1014, p50=-0.0037, p90=0.1030, p10_price=31.5341, p50_price=34.7722, p90_price=38.6852, sample=3863, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0035, p90=0.1421, p10_price=30.0660, p50_price=34.7768, p90_price=40.2304, sample=3853, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0797, p50=-0.0070, p90=0.0863, p10_price=32.2270, p50_price=34.6551, p90_price=38.0472, sample=187, fallback=NO
- 10D: p10=-0.1155, p50=-0.0167, p90=0.0838, p10_price=31.0945, p50_price=34.3211, p90_price=37.9496, sample=187, fallback=NO
- 20D: p10=-0.1648, p50=-0.0361, p90=0.1293, p10_price=29.5972, p50_price=33.6634, p90_price=39.7169, sample=187, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0782, p50=-0.0010, p90=0.0762, p10_price=32.2736, p50_price=34.8645, p90_price=37.6634, sample=3868, fallback=N/A
- 10D: p10=-0.1121, p50=-0.0021, p90=0.1080, p10_price=31.1976, p50_price=34.8270, p90_price=38.8785, sample=3863, fallback=N/A
- 20D: p10=-0.1595, p50=-0.0042, p90=0.1512, p10_price=29.7542, p50_price=34.7546, p90_price=40.5954, sample=3853, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-06T12:24:44.172977+00:00
- 数据快照: cnsvdata-2026-08-06-b35a41d86792
