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
- 最新交易日: 2026-10-27
- 最新收盘价: 34.6400
- 趋势状态: strong_downtrend
- 波动率状态: normal_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0661, p50=0.0000, p90=0.0661, p10_price=32.4231, p50_price=34.6400, p90_price=37.0085, sample=3920, fallback=N/A
- 10D: p10=-0.0935, p50=0.0000, p90=0.0935, p10_price=31.5469, p50_price=34.6400, p90_price=38.0363, sample=3915, fallback=N/A
- 20D: p10=-0.1323, p50=0.0000, p90=0.1323, p10_price=30.3481, p50_price=34.6400, p90_price=39.5389, sample=3905, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0716, p10_price=32.3297, p50_price=34.5817, p90_price=37.2115, sample=3920, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0037, p90=0.1035, p10_price=31.3097, p50_price=34.5131, p90_price=38.4180, sample=3915, fallback=N/A
- 20D: p10=-0.1488, p50=-0.0029, p90=0.1432, p10_price=29.8521, p50_price=34.5390, p90_price=39.9716, sample=3905, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0648, p50=0.0004, p90=0.0578, p10_price=32.4653, p50_price=34.6526, p90_price=36.7014, sample=63, fallback=NO
- 10D: p10=-0.0828, p50=0.0077, p90=0.1111, p10_price=31.8869, p50_price=34.9068, p90_price=38.7116, sample=63, fallback=NO
- 20D: p10=-0.1404, p50=0.0271, p90=0.1097, p10_price=30.1030, p50_price=35.5927, p90_price=38.6546, sample=63, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0716, p50=-0.0010, p90=0.0696, p10_price=32.2459, p50_price=34.6051, p90_price=37.1370, sample=3920, fallback=N/A
- 10D: p10=-0.1026, p50=-0.0020, p90=0.0986, p10_price=31.2625, p50_price=34.5711, p90_price=38.2299, sample=3915, fallback=N/A
- 20D: p10=-0.1456, p50=-0.0037, p90=0.1383, p10_price=29.9461, p50_price=34.5128, p90_price=39.7759, sample=3905, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-10-29T18:44:24.398494+00:00
- 数据快照: cnsvdata-2026-10-27-1be584d823cc
