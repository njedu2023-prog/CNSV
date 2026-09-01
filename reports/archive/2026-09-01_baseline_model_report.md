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
- 最新交易日: 2026-09-01
- 最新收盘价: 34.4300
- 趋势状态: uptrend
- 波动率状态: low_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0696, p50=0.0000, p90=0.0696, p10_price=32.1141, p50_price=34.4300, p90_price=36.9129, sample=3886, fallback=N/A
- 10D: p10=-0.0985, p50=0.0000, p90=0.0985, p10_price=31.2011, p50_price=34.4300, p90_price=37.9930, sample=3881, fallback=N/A
- 20D: p10=-0.1393, p50=0.0000, p90=0.1393, p10_price=29.9541, p50_price=34.4300, p90_price=39.5748, sample=3871, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0715, p10_price=32.1350, p50_price=34.3740, p90_price=36.9811, sample=3886, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0038, p90=0.1029, p10_price=31.1191, p50_price=34.2998, p90_price=38.1601, sample=3881, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0034, p90=0.1419, p10_price=29.6628, p50_price=34.3140, p90_price=39.6785, sample=3871, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0508, p50=0.0070, p90=0.0789, p10_price=32.7239, p50_price=34.6706, p90_price=37.2579, sample=44, fallback=NO
- 10D: p10=-0.0605, p50=0.0101, p90=0.0851, p10_price=32.4087, p50_price=34.7799, p90_price=37.4888, sample=44, fallback=NO
- 20D: p10=-0.1518, p50=-0.0167, p90=0.1420, p10_price=29.5796, p50_price=33.8600, p90_price=39.6822, sample=44, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0437, p50=-0.0010, p90=0.0416, p10_price=32.9578, p50_price=34.3944, p90_price=35.8936, sample=3886, fallback=N/A
- 10D: p10=-0.0629, p50=-0.0021, p90=0.0587, p10_price=32.3302, p50_price=34.3570, p90_price=36.5109, sample=3881, fallback=N/A
- 20D: p10=-0.0900, p50=-0.0042, p90=0.0817, p10_price=31.4678, p50_price=34.2872, p90_price=37.3592, sample=3871, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-01T14:58:43.253646+00:00
- 数据快照: cnsvdata-2026-09-01-2fdda0a5521c
