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
- 最新交易日: 2026-06-18
- 最新收盘价: 36.1400
- 趋势状态: downtrend
- 波动率状态: normal_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0729, p50=0.0000, p90=0.0729, p10_price=33.6000, p50_price=36.1400, p90_price=38.8720, sample=3834, fallback=N/A
- 10D: p10=-0.1031, p50=0.0000, p90=0.1031, p10_price=32.6010, p50_price=36.1400, p90_price=40.0632, sample=3829, fallback=N/A
- 20D: p10=-0.1457, p50=0.0000, p90=0.1457, p10_price=31.2386, p50_price=36.1400, p90_price=41.8105, sample=3819, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0689, p50=-0.0016, p90=0.0716, p10_price=33.7340, p50_price=36.0818, p90_price=38.8234, sample=3834, fallback=N/A
- 10D: p10=-0.1013, p50=-0.0038, p90=0.1035, p10_price=32.6591, p50_price=36.0012, p90_price=40.0812, sample=3829, fallback=N/A
- 20D: p10=-0.1494, p50=-0.0028, p90=0.1431, p10_price=31.1242, p50_price=36.0404, p90_price=41.6990, sample=3819, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0620, p50=-0.0098, p90=0.0640, p10_price=33.9677, p50_price=35.7889, p90_price=38.5290, sample=105, fallback=NO
- 10D: p10=-0.1313, p50=-0.0036, p90=0.0818, p10_price=31.6941, p50_price=36.0087, p90_price=39.2201, sample=105, fallback=NO
- 20D: p10=-0.1234, p50=0.0159, p90=0.1199, p10_price=31.9459, p50_price=36.7185, p90_price=40.7437, sample=105, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0568, p50=-0.0010, p90=0.0548, p10_price=34.1459, p50_price=36.1043, p90_price=38.1751, sample=3834, fallback=N/A
- 10D: p10=-0.0817, p50=-0.0020, p90=0.0776, p10_price=33.3058, p50_price=36.0666, p90_price=39.0562, sample=3829, fallback=N/A
- 20D: p10=-0.1164, p50=-0.0039, p90=0.1087, p10_price=32.1702, p50_price=36.0010, p90_price=40.2879, sample=3819, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-06-21T19:26:22.906869+00:00
- 数据快照: cnsvdata-2026-06-18-4c7619afdb56
