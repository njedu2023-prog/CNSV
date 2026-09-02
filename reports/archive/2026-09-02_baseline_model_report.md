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
- 最新交易日: 2026-09-02
- 最新收盘价: 33.9300
- 趋势状态: downtrend
- 波动率状态: low_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0698, p50=0.0000, p90=0.0698, p10_price=31.6420, p50_price=33.9300, p90_price=36.3834, sample=3887, fallback=N/A
- 10D: p10=-0.0987, p50=0.0000, p90=0.0987, p10_price=30.7401, p50_price=33.9300, p90_price=37.4509, sample=3882, fallback=N/A
- 20D: p10=-0.1396, p50=0.0000, p90=0.1396, p10_price=29.5083, p50_price=33.9300, p90_price=39.0142, sample=3872, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0715, p10_price=31.6686, p50_price=33.8748, p90_price=36.4440, sample=3887, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0037, p90=0.1028, p10_price=30.6674, p50_price=33.8037, p90_price=37.6049, sample=3882, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0034, p90=0.1418, p10_price=29.2325, p50_price=33.8155, p90_price=39.0978, sample=3872, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0558, p50=-0.0011, p90=0.0470, p10_price=32.0883, p50_price=33.8938, p90_price=35.5634, sample=192, fallback=NO
- 10D: p10=-0.0889, p50=-0.0041, p90=0.0897, p10_price=31.0427, p50_price=33.7910, p90_price=37.1152, sample=191, fallback=NO
- 20D: p10=-0.1545, p50=-0.0177, p90=0.1341, p10_price=29.0729, p50_price=33.3353, p90_price=38.7980, sample=188, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0437, p50=-0.0010, p90=0.0416, p10_price=32.4794, p50_price=33.8949, p90_price=35.3722, sample=3887, fallback=N/A
- 10D: p10=-0.0629, p50=-0.0021, p90=0.0587, p10_price=31.8611, p50_price=33.8583, p90_price=35.9806, sample=3882, fallback=N/A
- 20D: p10=-0.0900, p50=-0.0042, p90=0.0816, p10_price=31.0109, p50_price=33.7890, p90_price=36.8160, sample=3872, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-02T14:34:08.749737+00:00
- 数据快照: cnsvdata-2026-09-02-9103eafbefc0
