# CNSV V1.2 基准模型报告

本报告仅展示 5D/10D/20D 终端收益分布基准模型，不生成交易动作。

## CNSVdata 数据门禁
- 状态: PASS
- 就绪: YES
- 允许继续: YES

## 特征质量
- 状态: WARN
- FAIL 数量: 0
- WARN 数量: 1

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
- 最新交易日: 2026-09-03
- 最新收盘价: 34.3200
- 趋势状态: strong_uptrend
- 波动率状态: low_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0698, p50=0.0000, p90=0.0698, p10_price=32.0060, p50_price=34.3200, p90_price=36.8013, sample=3888, fallback=N/A
- 10D: p10=-0.0987, p50=0.0000, p90=0.0987, p10_price=31.0938, p50_price=34.3200, p90_price=37.8809, sample=3883, fallback=N/A
- 20D: p10=-0.1396, p50=0.0000, p90=0.1396, p10_price=29.8480, p50_price=34.3200, p90_price=39.4620, sample=3873, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0715, p10_price=32.0328, p50_price=34.2635, p90_price=36.8629, sample=3888, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0037, p90=0.1028, p10_price=31.0201, p50_price=34.1943, p90_price=38.0362, sample=3883, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0034, p90=0.1417, p10_price=29.5689, p50_price=34.2041, p90_price=39.5426, sample=3873, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0702, p50=0.0034, p90=0.0545, p10_price=31.9936, p50_price=34.4378, p90_price=36.2425, sample=85, fallback=NO
- 10D: p10=-0.1037, p50=0.0000, p90=0.1431, p10_price=30.9391, p50_price=34.3200, p90_price=39.6008, sample=85, fallback=NO
- 20D: p10=-0.1295, p50=0.0035, p90=0.1794, p10_price=30.1520, p50_price=34.4408, p90_price=41.0625, sample=85, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0437, p50=-0.0010, p90=0.0416, p10_price=32.8528, p50_price=34.2845, p90_price=35.7785, sample=3888, fallback=N/A
- 10D: p10=-0.0629, p50=-0.0021, p90=0.0587, p10_price=32.2279, p50_price=34.2478, p90_price=36.3944, sample=3883, fallback=N/A
- 20D: p10=-0.0900, p50=-0.0042, p90=0.0816, p10_price=31.3676, p50_price=34.1773, p90_price=37.2386, sample=3873, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-03T17:18:53.601897+00:00
- 数据快照: cnsvdata-2026-09-03-a5e0273eb75d
