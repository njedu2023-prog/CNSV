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
- 最新交易日: 2026-08-28
- 最新收盘价: 34.7800
- 趋势状态: uptrend
- 波动率状态: low_vol
- 资金流强弱: mixed

## 基准模型

### B0_random_walk
- 5D: p10=-0.0707, p50=0.0000, p90=0.0707, p10_price=32.4054, p50_price=34.7800, p90_price=37.3286, sample=3884, fallback=N/A
- 10D: p10=-0.1000, p50=0.0000, p90=0.1000, p10_price=31.4700, p50_price=34.7800, p90_price=38.4382, sample=3879, fallback=N/A
- 20D: p10=-0.1414, p50=0.0000, p90=0.1414, p10_price=30.1929, p50_price=34.7800, p90_price=40.0640, sample=3869, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0016, p90=0.0715, p10_price=32.4611, p50_price=34.7227, p90_price=37.3571, sample=3884, fallback=N/A
- 10D: p10=-0.1011, p50=-0.0038, p90=0.1029, p10_price=31.4346, p50_price=34.6469, p90_price=38.5482, sample=3879, fallback=N/A
- 20D: p10=-0.1490, p50=-0.0034, p90=0.1419, p10_price=29.9643, p50_price=34.6629, p90_price=40.0830, sample=3869, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0402, p50=0.0013, p90=0.0502, p10_price=33.4080, p50_price=34.8260, p90_price=36.5692, sample=51, fallback=NO
- 10D: p10=-0.0595, p50=-0.0108, p90=0.0710, p10_price=32.7716, p50_price=34.4074, p90_price=37.3395, sample=51, fallback=NO
- 20D: p10=-0.1130, p50=0.0016, p90=0.1691, p10_price=31.0647, p50_price=34.8371, p90_price=41.1863, sample=51, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0437, p50=-0.0010, p90=0.0416, p10_price=33.2923, p50_price=34.7438, p90_price=36.2586, sample=3884, fallback=N/A
- 10D: p10=-0.0630, p50=-0.0021, p90=0.0587, p10_price=32.6580, p50_price=34.7059, p90_price=36.8821, sample=3879, fallback=N/A
- 20D: p10=-0.0900, p50=-0.0042, p90=0.0817, p10_price=31.7872, p50_price=34.6360, p90_price=37.7400, sample=3869, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-31T18:03:15.701319+00:00
- 数据快照: cnsvdata-2026-08-28-291bc662d426
