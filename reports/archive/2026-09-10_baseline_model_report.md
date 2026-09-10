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
- 最新交易日: 2026-09-10
- 最新收盘价: 40.8200
- 趋势状态: strong_uptrend
- 波动率状态: high_vol
- 资金流强弱: positive

## 基准模型

### B0_random_walk
- 5D: p10=-0.0768, p50=0.0000, p90=0.0768, p10_price=37.8038, p50_price=40.8200, p90_price=44.0768, sample=3893, fallback=N/A
- 10D: p10=-0.1086, p50=0.0000, p90=0.1086, p10_price=36.6208, p50_price=40.8200, p90_price=45.5008, sample=3888, fallback=N/A
- 20D: p10=-0.1535, p50=0.0000, p90=0.1535, p10_price=35.0106, p50_price=40.8200, p90_price=47.5934, sample=3878, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0689, p50=-0.0016, p90=0.0720, p10_price=38.1018, p50_price=40.7549, p90_price=43.8666, sample=3893, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0036, p90=0.1035, p10_price=36.8964, p50_price=40.6721, p90_price=45.2695, sample=3888, fallback=N/A
- 20D: p10=-0.1489, p50=-0.0033, p90=0.1421, p10_price=35.1718, p50_price=40.6872, p90_price=47.0510, sample=3878, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0944, p50=-0.0041, p90=0.1059, p10_price=37.1414, p50_price=40.6521, p90_price=45.3794, sample=99, fallback=NO
- 10D: p10=-0.1154, p50=-0.0146, p90=0.1657, p10_price=36.3712, p50_price=40.2297, p90_price=48.1757, sample=99, fallback=NO
- 20D: p10=-0.1801, p50=0.0021, p90=0.2218, p10_price=34.0923, p50_price=40.9063, p90_price=50.9577, sample=99, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0708, p50=-0.0009, p90=0.0691, p10_price=38.0293, p50_price=40.7846, p90_price=43.7395, sample=3893, fallback=N/A
- 10D: p10=-0.1015, p50=-0.0019, p90=0.0976, p10_price=36.8803, p50_price=40.7415, p90_price=45.0070, sample=3888, fallback=N/A
- 20D: p10=-0.1444, p50=-0.0040, p90=0.1364, p10_price=35.3314, p50_price=40.6573, p90_price=46.7861, sample=3878, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-09-10T14:31:10.137204+00:00
- 数据快照: cnsvdata-2026-09-10-febf058c742a
