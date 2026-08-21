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
- 最新交易日: 2026-08-21
- 最新收盘价: 33.6800
- 趋势状态: downtrend
- 波动率状态: low_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0713, p50=0.0000, p90=0.0713, p10_price=31.3629, p50_price=33.6800, p90_price=36.1683, sample=3879, fallback=N/A
- 10D: p10=-0.1008, p50=0.0000, p90=0.1008, p10_price=30.4504, p50_price=33.6800, p90_price=37.2521, sample=3874, fallback=N/A
- 20D: p10=-0.1426, p50=0.0000, p90=0.1426, p10_price=29.2051, p50_price=33.6800, p90_price=38.8405, sample=3864, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0715, p10_price=31.4337, p50_price=33.6234, p90_price=36.1766, sample=3879, fallback=N/A
- 10D: p10=-0.1012, p50=-0.0039, p90=0.1029, p10_price=30.4386, p50_price=33.5493, p90_price=37.3293, sample=3874, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0034, p90=0.1420, p10_price=29.0166, p50_price=33.5664, p90_price=38.8178, sample=3864, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0601, p50=0.0019, p90=0.0605, p10_price=31.7167, p50_price=33.7424, p90_price=35.7805, sample=80, fallback=NO
- 10D: p10=-0.1096, p50=-0.0042, p90=0.1009, p10_price=30.1834, p50_price=33.5402, p90_price=37.2543, sample=80, fallback=NO
- 20D: p10=-0.1316, p50=-0.0091, p90=0.1833, p10_price=29.5271, p50_price=33.3742, p90_price=40.4563, sample=80, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0443, p50=-0.0011, p90=0.0421, p10_price=32.2219, p50_price=33.6439, p90_price=35.1286, sample=3879, fallback=N/A
- 10D: p10=-0.0637, p50=-0.0021, p90=0.0594, p10_price=31.6017, p50_price=33.6078, p90_price=35.7413, sample=3874, fallback=N/A
- 20D: p10=-0.0910, p50=-0.0042, p90=0.0827, p10_price=30.7501, p50_price=33.5405, p90_price=36.5840, sample=3864, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-21T12:29:14.161344+00:00
- 数据快照: cnsvdata-2026-08-21-707c3ab56104
