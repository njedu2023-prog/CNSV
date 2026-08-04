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
- 最新交易日: 2026-08-04
- 最新收盘价: 34.4800
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0774, p50=0.0000, p90=0.0774, p10_price=31.9116, p50_price=34.4800, p90_price=37.2551, sample=3866, fallback=N/A
- 10D: p10=-0.1095, p50=0.0000, p90=0.1095, p10_price=30.9047, p50_price=34.4800, p90_price=38.4690, sample=3861, fallback=N/A
- 20D: p10=-0.1548, p50=0.0000, p90=0.1548, p10_price=29.5346, p50_price=34.4800, p90_price=40.2535, sample=3851, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0691, p50=-0.0016, p90=0.0716, p10_price=32.1785, p50_price=34.4239, p90_price=37.0400, sample=3866, fallback=N/A
- 10D: p10=-0.1015, p50=-0.0038, p90=0.1030, p10_price=31.1531, p50_price=34.3496, p90_price=38.2205, sample=3861, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0034, p90=0.1422, p10_price=29.7038, p50_price=34.3629, p90_price=39.7475, sample=3851, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0797, p50=-0.0070, p90=0.0863, p10_price=31.8392, p50_price=34.2380, p90_price=37.5894, sample=187, fallback=NO
- 10D: p10=-0.1155, p50=-0.0167, p90=0.0838, p10_price=30.7203, p50_price=33.9080, p90_price=37.4929, sample=187, fallback=NO
- 20D: p10=-0.1657, p50=-0.0385, p90=0.1301, p10_price=29.2139, p50_price=33.1789, p90_price=39.2704, sample=186, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0800, p50=-0.0010, p90=0.0779, p10_price=31.8303, p50_price=34.4448, p90_price=37.2739, sample=3866, fallback=N/A
- 10D: p10=-0.1146, p50=-0.0021, p90=0.1104, p10_price=30.7463, p50_price=34.4069, p90_price=38.5034, sample=3861, fallback=N/A
- 20D: p10=-0.1630, p50=-0.0042, p90=0.1546, p10_price=29.2951, p50_price=34.3368, p90_price=40.2462, sample=3851, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-04T12:24:48.561825+00:00
- 数据快照: cnsvdata-2026-08-04-a78da8414d61
