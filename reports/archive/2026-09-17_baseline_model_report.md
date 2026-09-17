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
- 最新交易日: 2026-09-17
- 最新收盘价: 38.9600
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0757, p50=0.0000, p90=0.0757, p10_price=36.1192, p50_price=38.9600, p90_price=42.0242, sample=3898, fallback=N/A
- 10D: p10=-0.1071, p50=0.0000, p90=0.1071, p10_price=35.0041, p50_price=38.9600, p90_price=43.3630, sample=3893, fallback=N/A
- 20D: p10=-0.1514, p50=0.0000, p90=0.1514, p10_price=33.4856, p50_price=38.9600, p90_price=45.3294, sample=3883, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0688, p50=-0.0016, p90=0.0719, p10_price=36.3687, p50_price=38.8973, p90_price=41.8663, sample=3898, fallback=N/A
- 10D: p10=-0.1010, p50=-0.0036, p90=0.1041, p10_price=35.2188, p50_price=38.8201, p90_price=43.2326, sample=3893, fallback=N/A
- 20D: p10=-0.1489, p50=-0.0031, p90=0.1429, p10_price=33.5712, p50_price=38.8393, p90_price=44.9469, sample=3883, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0811, p50=-0.0072, p90=0.0771, p10_price=35.9261, p50_price=38.6788, p90_price=42.0814, sample=72, fallback=NO
- 10D: p10=-0.0849, p50=-0.0037, p90=0.1392, p10_price=35.7885, p50_price=38.8156, p90_price=44.7786, sample=72, fallback=NO
- 20D: p10=-0.1552, p50=-0.0317, p90=0.1401, p10_price=33.3609, p50_price=37.7433, p90_price=44.8189, sample=72, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0791, p50=-0.0009, p90=0.0774, p10_price=35.9963, p50_price=38.9258, p90_price=42.0937, sample=3898, fallback=N/A
- 10D: p10=-0.1132, p50=-0.0018, p90=0.1097, p10_price=34.7889, p50_price=38.8913, p90_price=43.4773, sample=3893, fallback=N/A
- 20D: p10=-0.1609, p50=-0.0038, p90=0.1534, p10_price=33.1681, p50_price=38.8124, p90_price=45.4172, sample=3883, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-17T15:05:46.249627+00:00
- 数据快照: cnsvdata-2026-09-17-d10bceef25d0
