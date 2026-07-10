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
- 最新交易日: 2026-07-10
- 最新收盘价: 37.0400
- 趋势状态: strong_uptrend
- 波动率状态: high_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0801, p50=0.0000, p90=0.0801, p10_price=34.1882, p50_price=37.0400, p90_price=40.1297, sample=3849, fallback=N/A
- 10D: p10=-0.1133, p50=0.0000, p90=0.1133, p10_price=33.0723, p50_price=37.0400, p90_price=41.4837, sample=3844, fallback=N/A
- 20D: p10=-0.1602, p50=0.0000, p90=0.1602, p10_price=31.5560, p50_price=37.0400, p90_price=43.4771, sample=3834, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0719, p10_price=34.5718, p50_price=36.9797, p90_price=39.8028, sample=3849, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0037, p90=0.1033, p10_price=33.4788, p50_price=36.9048, p90_price=41.0713, sample=3844, fallback=N/A
- 20D: p10=-0.1493, p50=-0.0029, p90=0.1429, p10_price=31.9042, p50_price=36.9334, p90_price=42.7303, sample=3834, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0889, p50=-0.0015, p90=0.1069, p10_price=33.8879, p50_price=36.9837, p90_price=41.2182, sample=97, fallback=NO
- 10D: p10=-0.1168, p50=-0.0097, p90=0.1679, p10_price=32.9557, p50_price=36.6838, p90_price=43.8117, sample=97, fallback=NO
- 20D: p10=-0.1827, p50=0.0043, p90=0.2224, p10_price=30.8559, p50_price=37.1981, p90_price=46.2670, sample=97, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0963, p50=-0.0010, p90=0.0944, p10_price=33.6396, p50_price=37.0046, p90_price=40.7063, sample=3849, fallback=N/A
- 10D: p10=-0.1379, p50=-0.0020, p90=0.1339, p10_price=32.2676, p50_price=36.9658, p90_price=42.3481, sample=3844, fallback=N/A
- 20D: p10=-0.1960, p50=-0.0039, p90=0.1881, p10_price=30.4476, p50_price=36.8942, p90_price=44.7058, sample=3834, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-10T16:23:51.992447+00:00
- 数据快照: cnsvdata-2026-07-10-3ad77ca29fb1
