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
- 最新交易日: 2026-08-19
- 最新收盘价: 33.1400
- 趋势状态: strong_downtrend
- 波动率状态: low_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0710, p50=0.0000, p90=0.0710, p10_price=30.8680, p50_price=33.1400, p90_price=35.5793, sample=3877, fallback=N/A
- 10D: p10=-0.1004, p50=0.0000, p90=0.1004, p10_price=29.9731, p50_price=33.1400, p90_price=36.6415, sample=3872, fallback=N/A
- 20D: p10=-0.1420, p50=0.0000, p90=0.1420, p10_price=28.7517, p50_price=33.1400, p90_price=38.1980, sample=3862, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0715, p10_price=30.9297, p50_price=33.0843, p90_price=35.5974, sample=3877, fallback=N/A
- 10D: p10=-0.1012, p50=-0.0038, p90=0.1029, p10_price=29.9498, p50_price=33.0137, p90_price=36.7309, sample=3872, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0034, p90=0.1420, p10_price=28.5514, p50_price=33.0282, p90_price=38.1964, sample=3862, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0607, p50=0.0050, p90=0.0560, p10_price=31.1894, p50_price=33.3045, p90_price=35.0500, sample=224, fallback=NO
- 10D: p10=-0.0760, p50=-0.0071, p90=0.1100, p10_price=30.7161, p50_price=32.9060, p90_price=36.9951, sample=224, fallback=NO
- 20D: p10=-0.1105, p50=-0.0038, p90=0.1389, p10_price=29.6726, p50_price=33.0157, p90_price=38.0800, sample=224, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0468, p50=-0.0011, p90=0.0447, p10_price=31.6238, p50_price=33.1046, p90_price=34.6547, sample=3877, fallback=N/A
- 10D: p10=-0.0673, p50=-0.0021, p90=0.0631, p10_price=30.9818, p50_price=33.0697, p90_price=35.2984, sample=3872, fallback=N/A
- 20D: p10=-0.0962, p50=-0.0042, p90=0.0879, p10_price=30.1005, p50_price=33.0027, p90_price=36.1846, sample=3862, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-19T12:24:55.965392+00:00
- 数据快照: cnsvdata-2026-08-19-d140bde463c5
