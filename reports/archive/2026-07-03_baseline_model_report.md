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
- 最新交易日: 2026-07-03
- 最新收盘价: 37.1500
- 趋势状态: neutral
- 波动率状态: high_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0800, p50=0.0000, p90=0.0800, p10_price=34.2927, p50_price=37.1500, p90_price=40.2454, sample=3844, fallback=N/A
- 10D: p10=-0.1132, p50=0.0000, p90=0.1132, p10_price=33.1746, p50_price=37.1500, p90_price=41.6018, sample=3839, fallback=N/A
- 20D: p10=-0.1601, p50=0.0000, p90=0.1601, p10_price=31.6552, p50_price=37.1500, p90_price=43.5986, sample=3829, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0716, p10_price=34.6731, p50_price=37.0880, p90_price=39.9084, sample=3844, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0038, p90=0.1031, p10_price=33.5767, p50_price=37.0073, p90_price=41.1849, sample=3839, fallback=N/A
- 20D: p10=-0.1493, p50=-0.0032, p90=0.1430, p10_price=31.9969, p50_price=37.0304, p90_price=42.8619, sample=3829, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0766, p50=0.0069, p90=0.0909, p10_price=34.4103, p50_price=37.4058, p90_price=40.6872, sample=32, fallback=NO
- 10D: p10=-0.0865, p50=0.0082, p90=0.0902, p10_price=34.0730, p50_price=37.4575, p90_price=40.6565, sample=32, fallback=NO
- 20D: p10=-0.0896, p50=-0.0143, p90=0.1558, p10_price=33.9672, p50_price=36.6223, p90_price=43.4143, sample=32, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0966, p50=-0.0010, p90=0.0946, p10_price=33.7283, p50_price=37.1118, p90_price=40.8346, sample=3844, fallback=N/A
- 10D: p10=-0.1384, p50=-0.0021, p90=0.1343, p10_price=32.3475, p50_price=37.0737, p90_price=42.4904, sample=3839, fallback=N/A
- 20D: p10=-0.1967, p50=-0.0040, p90=0.1887, p10_price=30.5163, p50_price=37.0011, p90_price=44.8641, sample=3829, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-07-03T15:52:10.065229+00:00
- 数据快照: cnsvdata-2026-07-03-3fd3a1502203
