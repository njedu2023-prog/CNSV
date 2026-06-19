# CNSV 主程序 V1.1 基础特征增强与资金流核心层开发文档

> 仓库：`njedu2023-prog/CNSV`  
> 上游：`njedu2023-prog/CNSVdata`  
> 标的：`600150.SH / 中国船舶`  
> 阶段定位：V1.0 数据接线层已经跑通，V1.1 进入“基础特征增强 + 资金流核心层”阶段。  
> 开发对象：Codex  
> 重要边界：本阶段仍然不生成正式买卖信号，不输出买入/卖出建议，不自动下单，不连接券商。

---

## 0. 当前状态

V1.0 已经完成：

```text
1. CNSV 主程序能读取 CNSVdata
2. downstream_ready 门禁已接入
3. data_manifest 已接入
4. processed parquet 已能读取
5. latest_data_report.md 已能生成
6. docs/data/latest_data_report.json 已能生成
7. docs/index.html 已能展示
8. Validation = PASS
9. failed_count = 0
10. warn_count = 0
```

当前报告显示：

```text
ready: True
status: PASS
can_continue: True
can_run_backtest: True
can_use_moneyflow_as_strong_factor: True
can_generate_formal_signal: False

daily_rows: 3839
one_min_rows: 1928
moneyflow_rows: 3839
latest_trade_date: 2026-06-18
```

所以 V1.0 地基已经完成，可以进入 V1.1。

---

## 1. V1.1 总目标

V1.1 的目标是：

```text
把 V1.0 的“能读数据”升级为“能产出稳定、可解释、可测试的基础特征层”。
```

重点是：

```text
资金流特征
量价特征
分钟结构特征
趋势特征
波动率特征
特征质量检查
特征报告
```

V1.1 不是交易信号阶段。

---

## 2. V1.1 严格边界

### 2.1 允许开发

```text
1. 增强 price_volume_features.py
2. 增强 minute_structure_features.py
3. 增强 moneyflow_features.py
4. 新增 trend_features.py
5. 新增 volatility_features.py
6. 新增 feature_quality.py
7. 新增 feature_registry.py
8. 新增 feature_report_json.py
9. 新增 feature_report_md.py
10. 新增 feature_report_html.py
11. 新增 generate_feature_report CLI
12. 新增 run_features.yml
13. 新增 pytest 测试
14. 更新 README.md
15. 更新 docs/index.html
```

### 2.2 严格禁止

```text
1. 不生成正式买卖信号
2. 不输出买入建议
3. 不输出卖出建议
4. 不输出目标仓位
5. 不输出目标股数
6. 不输出止损价
7. 不输出止盈价
8. 不开发 20D 路径预测
9. 不开发目标先到概率
10. 不开发正式回测引擎
11. 不开发成交仿真
12. 不进入 live_assist_mode
13. 不连接券商接口
14. 不自动下单
15. 不使用 TUSHARE_TOKEN
16. 不绕过 CNSVdata
17. 不把 feature_report 命名为 signal_report
```

---

## 3. V1.1 新增/强化目录

请在现有 V1.0 基础上新增或强化：

```text
src/cnsv/features/
├── price_volume_features.py
├── minute_structure_features.py
├── moneyflow_features.py
├── trend_features.py
├── volatility_features.py
├── feature_quality.py
├── feature_registry.py
└── feature_bundle.py

src/cnsv/report/
├── feature_report_json.py
├── feature_report_md.py
└── feature_report_html.py

src/cnsv/cli/
├── build_features.py
└── generate_feature_report.py

reports/
├── latest_feature_report.md
└── archive/YYYY-MM-DD_feature_report.md

docs/data/
├── latest_feature_report.json
└── feature_registry.json

.github/workflows/
└── run_features.yml
```

---

## 4. 资金流特征开发要求

文件：

```text
src/cnsv/features/moneyflow_features.py
```

### 4.1 输入

```text
data_bundle["moneyflow"]
data_bundle["daily"]
gate["can_use_moneyflow_as_strong_factor"]
```

moneyflow 参考字段：

```text
trade_date
buy_sm_amount
sell_sm_amount
buy_md_amount
sell_md_amount
buy_lg_amount
sell_lg_amount
buy_elg_amount
sell_elg_amount
net_mf_amount
```

如果字段缺失，不能报假 PASS，必须在 feature_quality 中 WARN 或 FAIL。

### 4.2 必须输出字段

```text
moneyflow_latest_trade_date
net_mf_amount
net_mf_ratio
small_order_net
medium_order_net
large_order_net
extra_large_order_net
main_force_net
main_force_ratio
flow_strength_basic
flow_strength_score
flow_continuity_3d
flow_continuity_5d
flow_continuity_10d
positive_flow_days_5d
positive_flow_days_10d
flow_reversal_1d
flow_reversal_3d
price_flow_confirm
price_flow_divergence
volume_flow_confirm
can_use_as_strong_factor
moneyflow_warning
```

### 4.3 计算定义

```text
small_order_net = buy_sm_amount - sell_sm_amount
medium_order_net = buy_md_amount - sell_md_amount
large_order_net = buy_lg_amount - sell_lg_amount
extra_large_order_net = buy_elg_amount - sell_elg_amount
main_force_net = large_order_net + extra_large_order_net
net_mf_ratio = net_mf_amount / daily.amount
main_force_ratio = main_force_net / daily.amount
```

如果 `daily.amount` 缺失或为 0，输出 null，并给 WARN。

### 4.4 flow_strength_basic

```text
main_force_net > 0 且 net_mf_amount > 0 -> positive
main_force_net < 0 且 net_mf_amount < 0 -> negative
其他 -> mixed
```

### 4.5 flow_strength_score

范围必须限制在：

```text
-100 到 +100
```

建议第一版：

```text
score = 50 * clip(net_mf_ratio / 0.05, -1, 1)
      + 50 * clip(main_force_ratio / 0.05, -1, 1)
```

### 4.6 price_flow_confirm

```text
price_ret_1d > 0 且 net_mf_amount > 0 -> True
price_ret_1d < 0 且 net_mf_amount < 0 -> True
其他 -> False
```

### 4.7 price_flow_divergence

```text
price_ret_1d > 0 且 net_mf_amount < 0 -> True
price_ret_1d < 0 且 net_mf_amount > 0 -> True
其他 -> False
```

### 4.8 volume_flow_confirm

```text
volume_ratio_5d > 1 且 net_mf_amount > 0 -> inflow_confirmed
volume_ratio_5d > 1 且 net_mf_amount < 0 -> outflow_confirmed
其他 -> neutral
```

---

## 5. 量价特征增强

文件：

```text
src/cnsv/features/price_volume_features.py
```

必须输出：

```text
latest_trade_date
latest_open
latest_high
latest_low
latest_close
latest_pre_close
latest_pct_chg
latest_volume
latest_amount

ma5
ma10
ma20
ma60

ret_1d
ret_3d
ret_5d
ret_10d
ret_20d
ret_60d

volume_ma5
volume_ma20
volume_ratio_5d
volume_ratio_20d

amount_ma5
amount_ma20
amount_ratio_5d
amount_ratio_20d

price_position_20d
price_position_60d

new_high_20d
new_low_20d
new_high_60d
new_low_60d
```

`price_position_20d` 定义：

```text
(close - rolling_low_20d) / (rolling_high_20d - rolling_low_20d)
```

分母为 0 时输出 null，并由 feature_quality 记录 WARN。

---

## 6. 分钟结构特征增强

文件：

```text
src/cnsv/features/minute_structure_features.py
```

必须输出：

```text
latest_intraday_date
latest_intraday_open
latest_intraday_high
latest_intraday_low
latest_intraday_close

intraday_range_pct
close_position_in_day_range

morning_return
afternoon_return
last_30min_return
last_60min_return

morning_volume_ratio
afternoon_volume_ratio
last_30min_volume_ratio
last_60min_volume_ratio

intraday_amount_sum
intraday_volume_sum

late_session_strength
late_session_weakness
intraday_reversal_flag
```

规则：

```text
late_session_strength:
last_30min_return > 0 且 close_position_in_day_range > 0.6

late_session_weakness:
last_30min_return < 0 且 close_position_in_day_range < 0.4

intraday_reversal_flag:
close_position_in_day_range < 0.35 且 intraday_high 明显高于 close
```

---

## 7. 趋势特征

新增：

```text
src/cnsv/features/trend_features.py
```

必须输出：

```text
trend_ma5_ma20
trend_ma10_ma60
close_above_ma5
close_above_ma10
close_above_ma20
close_above_ma60
ma5_slope
ma10_slope
ma20_slope
trend_state
```

`trend_state` 建议规则：

```text
close > ma5 > ma10 > ma20 -> strong_uptrend
close > ma20 且 ma5 > ma20 -> uptrend
close < ma5 < ma10 < ma20 -> strong_downtrend
close < ma20 -> downtrend
其他 -> neutral
```

---

## 8. 波动率特征

新增：

```text
src/cnsv/features/volatility_features.py
```

必须输出：

```text
realized_vol_5d
realized_vol_10d
realized_vol_20d
atr_14d
intraday_range_ma5
intraday_range_ma20
volatility_state
```

`volatility_state` 建议规则：

```text
realized_vol_20d 位于过去一年 70% 分位以上 -> high_vol
realized_vol_20d 位于过去一年 30% 分位以下 -> low_vol
其他 -> normal_vol
历史不足 -> unknown
```

---

## 9. 特征质量检查

新增：

```text
src/cnsv/features/feature_quality.py
```

必须检查：

```text
1. 特征是否为空
2. 关键特征是否为 null
3. 是否出现 inf
4. 是否出现 nan
5. moneyflow 是否允许作为强因子
6. 数据行数是否足够
7. 最新交易日是否一致
```

输出结构：

```python
{
    "status": "PASS|WARN|FAIL",
    "failed_count": 0,
    "warn_count": 0,
    "checks": []
}
```

规则：

```text
核心 daily 特征不可计算 -> FAIL
核心 minute 特征不可计算 -> FAIL
moneyflow 不可作为强因子 -> WARN
非核心特征 null -> WARN
出现 inf -> FAIL
```

---

## 10. 特征注册表

新增：

```text
src/cnsv/features/feature_registry.py
```

必须记录：

```text
feature_name
category
description
source
formula
required
used_in_v1_1
```

输出到：

```text
docs/data/feature_registry.json
```

---

## 11. Feature Report

### 11.1 JSON 输出

新增：

```text
docs/data/latest_feature_report.json
```

必须包含：

```json
{
  "meta": {
    "system": "CNSV",
    "version": "1.1.0",
    "report_type": "feature_report",
    "ts_code": "600150.SH",
    "name": "中国船舶",
    "generated_at": "",
    "latest_trade_date": ""
  },
  "cnsvdata_gate": {},
  "data_manifest": {},
  "feature_quality": {
    "status": "PASS",
    "failed_count": 0,
    "warn_count": 0,
    "checks": []
  },
  "features": {
    "price_volume": {},
    "minute_structure": {},
    "moneyflow": {},
    "trend": {},
    "volatility": {}
  },
  "feature_registry": [],
  "forbidden_actions": [
    "formal_signal_generation",
    "auto_order",
    "broker_api"
  ],
  "next_stage": "V1.2 baseline models"
}
```

### 11.2 Markdown 输出

新增：

```text
reports/latest_feature_report.md
reports/archive/YYYY-MM-DD_feature_report.md
```

必须包含：

```text
1. CNSVdata Gate 状态
2. Feature Quality 状态
3. 最新交易日
4. 量价特征摘要
5. 分钟结构特征摘要
6. 资金流特征摘要
7. 趋势特征摘要
8. 波动率特征摘要
9. 资金流是否可作为强因子
10. 禁止动作
11. 下一阶段建议
```

### 11.3 HTML 输出

更新：

```text
docs/index.html
```

至少展示：

```text
Data Report
Feature Report
Gate Status
Feature Quality
Moneyflow Summary
Trend Summary
Volatility Summary
```

---

## 12. CLI 命令

### 12.1 构建特征

```bash
python -m cnsv.cli.build_features
```

必须：

```text
读取 CNSVdata
构建 V1.1 所有特征
输出控制台摘要
```

### 12.2 生成特征报告

新增：

```bash
python -m cnsv.cli.generate_feature_report
```

必须：

```text
1. 读取 CNSVdata
2. 读取 downstream_ready
3. 构建 feature_bundle
4. 运行 feature_quality
5. 输出 latest_feature_report.json
6. 输出 latest_feature_report.md
7. 更新 docs/index.html
```

---

## 13. GitHub Actions

新增：

```text
.github/workflows/run_features.yml
```

内容建议：

```yaml
name: Run CNSV Features

on:
  workflow_dispatch:
  schedule:
    - cron: "15 9 * * 1-5"

permissions:
  contents: write

jobs:
  run-features:
    runs-on: ubuntu-latest
    env:
      PYTHONPATH: ${{ github.workspace }}/src
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - run: pip install -r requirements.txt

      - run: pytest

      - run: python -m cnsv.cli.generate_feature_report

      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add reports docs
          git diff --cached --quiet || git commit -m "report: update CNSV feature report"
          git push
```

说明：

```text
09:15 UTC = 北京时间 17:15
```

---

## 14. 测试要求

新增测试：

```text
tests/test_price_volume_features.py
tests/test_minute_structure_features.py
tests/test_moneyflow_features.py
tests/test_trend_features.py
tests/test_volatility_features.py
tests/test_feature_quality.py
tests/test_feature_registry.py
tests/test_feature_report_json.py
tests/test_feature_cli.py
```

必须测试：

```text
1. net_mf_ratio 计算正确
2. main_force_net 计算正确
3. flow_strength_score 限制在 -100 到 100
4. price_flow_divergence 可识别
5. volume_flow_confirm 可识别
6. trend_state 可识别
7. volatility_state 可识别
8. feature_quality 能识别 nan / inf
9. latest_feature_report.json 结构完整
10. generate_feature_report CLI 可运行
```

测试不得依赖真实网络，必须使用 mock DataFrame。

---

## 15. V1.1 验收标准

完成后必须能运行：

```bash
pip install -r requirements.txt
pytest
python -m cnsv.cli.build_features
python -m cnsv.cli.generate_feature_report
```

必须生成：

```text
docs/data/latest_feature_report.json
reports/latest_feature_report.md
docs/data/feature_registry.json
docs/index.html
```

并且：

```text
feature_quality.status = PASS
failed_count = 0
can_generate_formal_signal = false
forbidden_actions 包含 formal_signal_generation
```

---

## 16. 本阶段不做

V1.1 不做：

```text
1. 正式买入信号
2. 正式卖出信号
3. 目标仓位
4. 目标股数
5. 止损价
6. 止盈价
7. 20D 路径预测
8. 目标先到概率
9. 回测引擎
10. 成交仿真
11. live_assist_mode
12. 自动下单
13. 券商接口
```

---

## 17. 后续阶段

```text
V1.0 = 数据接线层
V1.1 = 基础特征增强层
V1.2 = 基准模型层
V1.3 = 20D 路径预测层
V1.4 = 回测与成交仿真
V1.5 = 试运行辅助报告
```

---

## 18. Codex 完成后必须汇报

```text
一、修改文件清单
二、新增文件清单
三、是否删除文件，如无写无
四、是否改变 CNSVdata 读取路径
五、是否使用 TUSHARE_TOKEN
六、是否生成正式信号
七、pytest 是否通过
八、run_features.yml 是否可运行
九、latest_feature_report.json 是否生成
十、latest_feature_report.md 是否生成
十一、feature_quality 当前状态
十二、moneyflow 是否可作为强因子
十三、是否仍然禁止 formal_signal_generation
十四、下一步建议
```

---

## 19. 给 Codex 的最终执行口令

```text
继续 CNSV 主程序仓库开发。

当前阶段：CNSV V1.1 基础特征增强与资金流核心层。

V1.0 数据接线层已经跑通。现在不要开发正式交易信号，不要开发路径预测，不要开发回测引擎。请只做基础特征增强，重点强化 A 股实战最重要的资金流特征。

请一次性完成：

1. 增强 src/cnsv/features/price_volume_features.py
2. 增强 src/cnsv/features/minute_structure_features.py
3. 增强 src/cnsv/features/moneyflow_features.py
4. 新增 src/cnsv/features/trend_features.py
5. 新增 src/cnsv/features/volatility_features.py
6. 新增 src/cnsv/features/feature_quality.py
7. 新增 src/cnsv/features/feature_registry.py
8. 强化 src/cnsv/features/feature_bundle.py
9. 新增 src/cnsv/report/feature_report_json.py
10. 新增 src/cnsv/report/feature_report_md.py
11. 新增 src/cnsv/report/feature_report_html.py
12. 新增 python -m cnsv.cli.generate_feature_report
13. 更新 python -m cnsv.cli.build_features
14. 新增 .github/workflows/run_features.yml
15. 新增相关 pytest 测试
16. 更新 README.md
17. 更新 docs/index.html

必须生成：
- docs/data/latest_feature_report.json
- reports/latest_feature_report.md
- docs/data/feature_registry.json

严格禁止：
- 不生成正式买卖信号
- 不输出买入/卖出建议
- 不输出目标仓位
- 不输出目标股数
- 不开发 20D 路径预测
- 不开发回测引擎
- 不连接券商
- 不自动下单
- 不使用 TUSHARE_TOKEN
- 不绕过 CNSVdata
- 不把 feature_report 命名为 signal_report

验收标准：
- pytest 必须通过
- python -m cnsv.cli.generate_feature_report 必须可运行
- latest_feature_report.json 必须生成
- latest_feature_report.md 必须生成
- feature_quality.status 必须为 PASS
- can_generate_formal_signal 必须仍为 false
- forbidden_actions 必须包含 formal_signal_generation
```

---

## 20. 最重要原则

```text
V1.1 的核心不是预测，而是把特征层做扎实。
```

尤其是：

```text
资金流是 A 股波段系统的第一核心输入。
```

但本阶段仍然只是特征，不是信号。
