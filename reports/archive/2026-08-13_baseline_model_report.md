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
- 最新交易日: 2026-08-13
- 最新收盘价: 33.7800
- 趋势状态: downtrend
- 波动率状态: low_vol
- 资金流强弱: negative

## 基准模型

### B0_random_walk
- 5D: p10=-0.0715, p50=0.0000, p90=0.0715, p10_price=31.4501, p50_price=33.7800, p90_price=36.2825, sample=3873, fallback=N/A
- 10D: p10=-0.1011, p50=0.0000, p90=0.1011, p10_price=30.5328, p50_price=33.7800, p90_price=37.3726, sample=3868, fallback=N/A
- 20D: p10=-0.1429, p50=0.0000, p90=0.1429, p10_price=29.2810, p50_price=33.7800, p90_price=38.9703, sample=3858, fallback=N/A

### B1_historical_distribution
- 5D: p10=-0.0690, p50=-0.0017, p90=0.0716, p10_price=31.5269, p50_price=33.7237, p90_price=36.2867, sample=3873, fallback=N/A
- 10D: p10=-0.1013, p50=-0.0037, p90=0.1029, p10_price=30.5257, p50_price=33.6567, p90_price=37.4416, sample=3868, fallback=N/A
- 20D: p10=-0.1491, p50=-0.0035, p90=0.1421, p10_price=29.1022, p50_price=33.6630, p90_price=38.9364, sample=3858, fallback=N/A

### B2_state_grouped_distribution
- 5D: p10=-0.0563, p50=-0.0012, p90=0.0474, p10_price=31.9294, p50_price=33.7378, p90_price=35.4213, sample=188, fallback=NO
- 10D: p10=-0.0891, p50=-0.0049, p90=0.0904, p10_price=30.8994, p50_price=33.6154, p90_price=36.9774, sample=188, fallback=NO
- 20D: p10=-0.1545, p50=-0.0177, p90=0.1341, p10_price=28.9444, p50_price=33.1879, p90_price=38.6265, sample=188, fallback=NO

### B3_volatility_adjusted
- 5D: p10=-0.0493, p50=-0.0010, p90=0.0472, p10_price=32.1544, p50_price=33.7448, p90_price=35.4139, sample=3873, fallback=N/A
- 10D: p10=-0.0709, p50=-0.0021, p90=0.0667, p10_price=31.4685, p50_price=33.7099, p90_price=36.1109, sample=3868, fallback=N/A
- 20D: p10=-0.1013, p50=-0.0042, p90=0.0929, p10_price=30.5260, p50_price=33.6392, p90_price=37.0700, sample=3858, fallback=N/A

## 禁止动作
- 正式交易动作生成
- 自动下单
- 券商接口
- is_trade_signal: NO
- can_generate_formal_signal: NO

## 下一阶段
- V1.2.2 baseline validation / walk-forward validation

## 生成信息
- generated_at: 2026-08-13T12:29:27.206183+00:00
- 数据快照: cnsvdata-2026-08-13-a75cf0a66be6
