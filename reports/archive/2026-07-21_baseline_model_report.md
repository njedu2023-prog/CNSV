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
- 最新交易日: 2026-07-21
- 最新收盘价: 32.9600
- 趋势状态: strong_downtrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0833, p50=0.0000, p90=0.0833, p10_price=30.3267, p50_price=32.9600, p90_price=35.8219, sample=3856, fallback=N/A
- 10D: p10=-0.1178, p50=0.0000, p90=0.1178, p10_price=29.2986, p50_price=32.9600, p90_price=37.0789, sample=3851, fallback=N/A
- 20D: p10=-0.1665, p50=0.0000, p90=0.1665, p10_price=27.9038, p50_price=32.9600, p90_price=38.9323, sample=3841, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0017, p90=0.0718, p10_price=30.7583, p50_price=32.9046, p90_price=35.4128, sample=3856, fallback=N/A
- 10D: p10=-0.1015, p50=-0.0038, p90=0.1030, p10_price=29.7798, p50_price=32.8353, p90_price=36.5362, sample=3851, fallback=N/A
- 20D: p10=-0.1492, p50=-0.0033, p90=0.1427, p10_price=28.3928, p50_price=32.8516, p90_price=38.0142, sample=3841, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1424, p50=0.0097, p90=0.0888, p10_price=28.5840, p50_price=33.2822, p90_price=36.0210, sample=69, fallback=NO
- 10D: p10=-0.1041, p50=0.0003, p90=0.1241, p10_price=29.7008, p50_price=32.9705, p90_price=37.3163, sample=69, fallback=NO
- 20D: p10=-0.2008, p50=-0.0167, p90=0.1520, p10_price=26.9641, p50_price=32.4135, p90_price=38.3696, sample=68, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.1037, p50=-0.0011, p90=0.1015, p10_price=29.7140, p50_price=32.9241, p90_price=36.4809, sample=3856, fallback=N/A
- 10D: p10=-0.1483, p50=-0.0021, p90=0.1440, p10_price=28.4178, p50_price=32.8903, p90_price=38.0668, sample=3851, fallback=N/A
- 20D: p10=-0.2105, p50=-0.0041, p90=0.2023, p10_price=26.7033, p50_price=32.8257, p90_price=40.3518, sample=3841, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-21T12:24:46.561187+00:00
- 数据快照: cnsvdata-2026-07-21-689cfae1b68c
