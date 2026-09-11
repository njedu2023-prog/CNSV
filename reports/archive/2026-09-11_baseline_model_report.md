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
- 最新交易日: 2026-09-11
- 最新收盘价: 39.7500
- 趋势状态: strong_uptrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0767, p50=0.0000, p90=0.0767, p10_price=36.8148, p50_price=39.7500, p90_price=42.9192, sample=3894, fallback=N/A
- 10D: p10=-0.1085, p50=0.0000, p90=0.1085, p10_price=35.6635, p50_price=39.7500, p90_price=44.3048, sample=3889, fallback=N/A
- 20D: p10=-0.1534, p50=0.0000, p90=0.1534, p10_price=34.0964, p50_price=39.7500, p90_price=46.3411, sample=3879, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0689, p50=-0.0016, p90=0.0720, p10_price=37.1037, p50_price=39.6869, p90_price=42.7165, sample=3894, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0036, p90=0.1035, p10_price=35.9295, p50_price=39.6065, p90_price=44.0849, sample=3889, fallback=N/A
- 20D: p10=-0.1489, p50=-0.0032, p90=0.1423, p10_price=34.2504, p50_price=39.6220, p90_price=45.8272, sample=3879, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1221, p50=-0.0055, p90=0.1311, p10_price=35.1794, p50_price=39.5334, p90_price=45.3178, sample=100, fallback=NO
- 10D: p10=-0.1583, p50=-0.0117, p90=0.2017, p10_price=33.9314, p50_price=39.2880, p90_price=48.6313, sample=100, fallback=NO
- 20D: p10=-0.2212, p50=0.0037, p90=0.2335, p10_price=31.8634, p50_price=39.8984, p90_price=50.2061, sample=100, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0736, p50=-0.0009, p90=0.0719, p10_price=36.9288, p50_price=39.7161, p90_price=42.7138, sample=3894, fallback=N/A
- 10D: p10=-0.1055, p50=-0.0019, p90=0.1017, p10_price=35.7704, p50_price=39.6750, p90_price=44.0057, sample=3889, fallback=N/A
- 20D: p10=-0.1500, p50=-0.0039, p90=0.1421, p10_price=34.2121, p50_price=39.5934, p90_price=45.8211, sample=3879, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-11T14:30:17.305589+00:00
- 数据快照: cnsvdata-2026-09-11-4c522d2d4f75
