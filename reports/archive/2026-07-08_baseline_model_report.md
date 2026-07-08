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
- 最新交易日: 2026-07-08
- 最新收盘价: 35.9800
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0797, p50=0.0000, p90=0.0797, p10_price=33.2241, p50_price=35.9800, p90_price=38.9645, sample=3847, fallback=N/A
- 10D: p10=-0.1127, p50=0.0000, p90=0.1127, p10_price=32.1454, p50_price=35.9800, p90_price=40.2721, sample=3842, fallback=N/A
- 20D: p10=-0.1594, p50=0.0000, p90=0.1594, p10_price=30.6793, p50_price=35.9800, p90_price=42.1965, sample=3832, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0720, p10_price=33.5819, p50_price=35.9215, p90_price=38.6643, sample=3847, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0037, p90=0.1030, p10_price=32.5202, p50_price=35.8461, p90_price=39.8838, sample=3842, fallback=N/A
- 20D: p10=-0.1493, p50=-0.0030, p90=0.1430, p10_price=30.9902, p50_price=35.8718, p90_price=41.5104, sample=3832, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0705, p50=-0.0011, p90=0.0745, p10_price=33.5306, p50_price=35.9405, p90_price=38.7648, sample=74, fallback=NO
- 10D: p10=-0.0953, p50=-0.0165, p90=0.0796, p10_price=32.7085, p50_price=35.3928, p90_price=38.9619, sample=74, fallback=NO
- 20D: p10=-0.1543, p50=-0.0197, p90=0.1454, p10_price=30.8353, p50_price=35.2775, p90_price=41.6119, sample=74, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0961, p50=-0.0010, p90=0.0942, p10_price=32.6822, p50_price=35.9452, p90_price=39.5340, sample=3847, fallback=N/A
- 10D: p10=-0.1377, p50=-0.0020, p90=0.1336, p10_price=31.3514, p50_price=35.9068, p90_price=41.1239, sample=3842, fallback=N/A
- 20D: p10=-0.1957, p50=-0.0040, p90=0.1877, p10_price=29.5857, p50_price=35.8374, p90_price=43.4100, sample=3832, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-08T16:01:50.377441+00:00
- 数据快照: cnsvdata-2026-07-08-cfbe1e187b83
