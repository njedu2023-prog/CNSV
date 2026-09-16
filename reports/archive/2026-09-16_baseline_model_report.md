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
- 最新交易日: 2026-09-16
- 最新收盘价: 37.7900
- 趋势状态: uptrend
- 波动率状态: high_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0749, p50=0.0000, p90=0.0749, p10_price=35.0619, p50_price=37.7900, p90_price=40.7304, sample=3897, fallback=N/A
- 10D: p10=-0.1060, p50=0.0000, p90=0.1060, p10_price=33.9904, p50_price=37.7900, p90_price=42.0144, sample=3892, fallback=N/A
- 20D: p10=-0.1499, p50=0.0000, p90=0.1499, p10_price=32.5307, p50_price=37.7900, p90_price=43.8996, sample=3882, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0688, p50=-0.0016, p90=0.0720, p10_price=35.2759, p50_price=37.7298, p90_price=40.6093, sample=3897, fallback=N/A
- 10D: p10=-0.1010, p50=-0.0036, p90=0.1038, p10_price=34.1597, p50_price=37.6541, p90_price=41.9231, sample=3892, fallback=N/A
- 20D: p10=-0.1489, p50=-0.0031, p90=0.1426, p10_price=32.5628, p50_price=37.6714, p90_price=43.5827, sample=3882, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0794, p50=-0.0071, p90=0.0863, p10_price=34.9063, p50_price=37.5237, p90_price=41.1975, sample=191, fallback=NO
- 10D: p10=-0.1153, p50=-0.0201, p90=0.0829, p10_price=33.6758, p50_price=37.0395, p90_price=41.0551, sample=191, fallback=NO
- 20D: p10=-0.1611, p50=-0.0327, p90=0.1261, p10_price=32.1672, p50_price=36.5743, p90_price=42.8679, sample=191, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0780, p50=-0.0009, p90=0.0762, p10_price=34.9558, p50_price=37.7573, p90_price=40.7832, sample=3897, fallback=N/A
- 10D: p10=-0.1116, p50=-0.0018, p90=0.1080, p10_price=33.7989, p50_price=37.7221, p90_price=42.1006, sample=3892, fallback=N/A
- 20D: p10=-0.1587, p50=-0.0038, p90=0.1510, p10_price=32.2456, p50_price=37.6452, p90_price=43.9489, sample=3882, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-16T15:02:29.207393+00:00
- 数据快照: cnsvdata-2026-09-16-21c3b9e055f6
