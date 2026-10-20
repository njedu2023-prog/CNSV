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
- 最新交易日: 2026-10-20
- 最新收盘价: 35.2200
- 趋势状态: strong_downtrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0665, p50=0.0000, p90=0.0665, p10_price=32.9527, p50_price=35.2200, p90_price=37.6433, sample=3915, fallback=N/A
- 10D: p10=-0.0941, p50=0.0000, p90=0.0941, p10_price=32.0569, p50_price=35.2200, p90_price=38.6952, sample=3910, fallback=N/A
- 20D: p10=-0.1331, p50=0.0000, p90=0.1331, p10_price=30.8314, p50_price=35.2200, p90_price=40.2333, sample=3900, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0716, p10_price=32.8721, p50_price=35.1613, p90_price=37.8350, sample=3915, fallback=N/A
- 10D: p10=-0.1006, p50=-0.0036, p90=0.1036, p10_price=31.8484, p50_price=35.0924, p90_price=39.0627, sample=3910, fallback=N/A
- 20D: p10=-0.1487, p50=-0.0027, p90=0.1432, p10_price=30.3540, p50_price=35.1240, p90_price=40.6444, sample=3900, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0700, p50=0.0007, p90=0.0717, p10_price=32.8378, p50_price=35.2455, p90_price=37.8393, sample=155, fallback=NO
- 10D: p10=-0.0898, p50=-0.0010, p90=0.0923, p10_price=32.1949, p50_price=35.1850, p90_price=38.6260, sample=154, fallback=NO
- 20D: p10=-0.1753, p50=-0.0038, p90=0.1309, p10_price=29.5565, p50_price=35.0849, p90_price=40.1446, sample=154, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0820, p50=-0.0010, p90=0.0800, p10_price=32.4485, p50_price=35.1861, p90_price=38.1546, sample=3915, fallback=N/A
- 10D: p10=-0.1172, p50=-0.0019, p90=0.1135, p10_price=31.3257, p50_price=35.1548, p90_price=39.4521, sample=3910, fallback=N/A
- 20D: p10=-0.1663, p50=-0.0035, p90=0.1592, p10_price=29.8237, p50_price=35.0956, p90_price=41.2994, sample=3900, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-10-20T15:11:51.815786+00:00
- 数据快照: cnsvdata-2026-10-20-5ee6f35d3d06
