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
- 最新交易日: 2026-08-24
- 最新收盘价: 33.8000
- 趋势状态: downtrend
- 波动率状态: low_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0709, p50=0.0000, p90=0.0709, p10_price=31.4852, p50_price=33.8000, p90_price=36.2850, sample=3880, fallback=N/A
- 10D: p10=-0.1003, p50=0.0000, p90=0.1003, p10_price=30.5734, p50_price=33.8000, p90_price=37.3671, sample=3875, fallback=N/A
- 20D: p10=-0.1419, p50=0.0000, p90=0.1419, p10_price=29.3289, p50_price=33.8000, p90_price=38.9528, sample=3865, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0715, p10_price=31.5457, p50_price=33.7434, p90_price=36.3050, sample=3880, fallback=N/A
- 10D: p10=-0.1012, p50=-0.0039, p90=0.1029, p10_price=30.5474, p50_price=33.6675, p90_price=37.4622, sample=3875, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0034, p90=0.1420, p10_price=29.1200, p50_price=33.6862, p90_price=38.9556, sample=3865, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0560, p50=-0.0012, p90=0.0474, p10_price=31.9581, p50_price=33.7578, p90_price=35.4413, sample=190, fallback=NO
- 10D: p10=-0.0891, p50=-0.0049, p90=0.0904, p10_price=30.9177, p50_price=33.6353, p90_price=36.9993, sample=188, fallback=NO
- 20D: p10=-0.1545, p50=-0.0177, p90=0.1341, p10_price=28.9615, p50_price=33.2075, p90_price=38.6494, sample=188, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0438, p50=-0.0011, p90=0.0416, p10_price=32.3527, p50_price=33.7638, p90_price=35.2365, sample=3880, fallback=N/A
- 10D: p10=-0.0630, p50=-0.0022, p90=0.0587, p10_price=31.7363, p50_price=33.7273, p90_price=35.8433, sample=3875, fallback=N/A
- 20D: p10=-0.0900, p50=-0.0041, p90=0.0817, p10_price=30.8902, p50_price=33.6601, p90_price=36.6783, sample=3865, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-24T12:29:01.809610+00:00
- 数据快照: cnsvdata-2026-08-24-2dd0ae9dd0a6
