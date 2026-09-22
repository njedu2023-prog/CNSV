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
- 最新交易日: 2026-09-22
- 最新收盘价: 40.1200
- 趋势状态: strong_uptrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0744, p50=0.0000, p90=0.0744, p10_price=37.2433, p50_price=40.1200, p90_price=43.2189, sample=3901, fallback=N/A
- 10D: p10=-0.1052, p50=0.0000, p90=0.1052, p10_price=36.1130, p50_price=40.1200, p90_price=44.5716, sample=3896, fallback=N/A
- 20D: p10=-0.1488, p50=0.0000, p90=0.1488, p10_price=34.5729, p50_price=40.1200, p90_price=46.5571, sample=3886, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0688, p50=-0.0016, p90=0.0719, p10_price=37.4534, p50_price=40.0560, p90_price=43.1120, sample=3901, fallback=N/A
- 10D: p10=-0.1008, p50=-0.0036, p90=0.1040, p10_price=36.2719, p50_price=39.9763, p90_price=44.5159, sample=3896, fallback=N/A
- 20D: p10=-0.1488, p50=-0.0029, p90=0.1433, p10_price=34.5715, p50_price=40.0045, p90_price=46.2995, sample=3886, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.1200, p50=-0.0055, p90=0.1273, p10_price=35.5844, p50_price=39.9014, p90_price=45.5689, sample=102, fallback=NO
- 10D: p10=-0.1582, p50=-0.0113, p90=0.2015, p10_price=34.2486, p50_price=39.6674, p90_price=49.0787, sample=101, fallback=NO
- 20D: p10=-0.2212, p50=0.0037, p90=0.2335, p10_price=32.1600, p50_price=40.2698, p90_price=50.6735, sample=100, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0839, p50=-0.0009, p90=0.0822, p10_price=36.8926, p50_price=40.0858, p90_price=43.5553, sample=3901, fallback=N/A
- 10D: p10=-0.1200, p50=-0.0017, p90=0.1165, p10_price=35.5836, p50_price=40.0507, p90_price=45.0786, sample=3896, fallback=N/A
- 20D: p10=-0.1705, p50=-0.0037, p90=0.1632, p10_price=33.8316, p50_price=39.9735, p90_price=47.2303, sample=3886, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-22T15:02:04.541978+00:00
- 数据快照: cnsvdata-2026-09-22-211484174936
