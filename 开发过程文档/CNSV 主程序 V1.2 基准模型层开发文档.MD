# CNSV 主程序 V1.2 基准模型层开发文档

> 仓库：`njedu2023-prog/CNSV`  
> 上游数据仓库：`njedu2023-prog/CNSVdata`  
> 标的：`600150.SH / 中国船舶`  
> 当前阶段：V1.0 数据接线层已完成，V1.1 基础特征增强与资金流核心层已完成，进入 V1.2 基准模型层。  
> 开发对象：Codex  
> 文档定位：本文件是 CNSV 主程序第三阶段开发规格。V1.2 的目标是建立透明、可解释、可测试、可验收的基准模型体系，为后续 20D 路径预测、回测和试运行辅助打基础。

---

## 0. 当前阶段背景

CNSV 当前已经完成：

```text
V1.0：数据接线层
- 读取 CNSVdata
- downstream_ready 门禁
- data_manifest 读取
- processed parquet 读取
- latest_data_report.json / md / html
- 禁止正式信号

V1.1：基础特征增强与资金流核心层
- price_volume 特征
- minute_structure 特征
- moneyflow 特征
- trend 特征
- volatility 特征
- feature_quality
- feature_registry
- latest_feature_report.json / md / html
```

当前已经可以做到：

```text
数据可读
特征可算
资金流可作为强因子
报告可生成
HTML 可展示
pytest / workflow 可运行
```

现在进入 V1.2。

---

## 1. V1.2 一句话目标

V1.2 只做一件事：

```text
建立 CNSV 的透明基准模型层。
```

不要一上来开发复杂模型。

不要生成正式交易信号。

不要输出买入卖出建议。

V1.2 的核心是：

```text
先知道“不用复杂模型时，中国船舶未来收益分布大概是什么样”。
```

后续所有复杂模型，都必须和这些基准模型比较，只有稳定优于基准，才有资格进入候选模型。

---

## 2. V1.2 严格边界

### 2.1 允许开发

```text
1. 基准模型 B0：随机游走 / 不变价格模型
2. 基准模型 B1：历史无条件收益分布模型
3. 基准模型 B2：状态分组历史收益分布模型
4. 基准模型 B3：简单波动率调整模型
5. 20D 基础终点收益分布
6. 5D / 10D / 20D 研究型收益分布
7. 基础分位数输出
8. 基础区间覆盖率检查
9. 基准模型报告
10. baseline_model_report.json
11. baseline_model_report.md
12. baseline.html / index 页面入口
13. pytest 测试
14. run_baseline_models.yml workflow
```

### 2.2 严格禁止

```text
1. 不生成正式买入信号
2. 不生成正式卖出信号
3. 不输出目标仓位
4. 不输出目标股数
5. 不输出止损价
6. 不输出止盈价
7. 不输出交易建议
8. 不进入 live_assist_mode
9. 不开发自动下单
10. 不连接券商接口
11. 不使用 TUSHARE_TOKEN
12. 不绕过 CNSVdata
13. 不开发复杂深度学习模型
14. 不开发强化学习模型
15. 不开发 champion/challenger 上线机制
16. 不把 baseline report 命名为 signal report
17. 不把概率分布解释成交易指令
```

---

## 3. V1.2 模型定义

### 3.1 预测目标

V1.2 只预测研究型收益分布，不生成交易动作。

预测目标：

```text
5D terminal_return
10D terminal_return
20D terminal_return
```

核心收益定义：

```text
terminal_return_h = ln(close[t+h] / close[t])
```

其中：

```text
h = 5, 10, 20 个 A 股交易日
```

V1.2 暂不做：

```text
60D 正式预测
120D 正式预测
路径预测
触碰概率
目标先到概率
止损先到概率
```

这些属于后续阶段。

---

## 4. 基准模型体系

### 4.1 B0：随机游走 / 不变价格模型

文件：

```text
src/cnsv/models/baseline_b0_random_walk.py
```

定义：

```text
未来期望收益 = 0
未来终点价格 = 当前收盘价
收益分布可用近期历史波动估计
```

输出字段：

```text
model_id: B0_random_walk
horizon
current_close
expected_return
expected_price
volatility_estimate
p10_return
p50_return
p90_return
p10_price
p50_price
p90_price
```

要求：

```text
B0 是最低基准。
任何复杂模型至少要比 B0 更有解释力。
```

---

### 4.2 B1：历史无条件收益分布模型

文件：

```text
src/cnsv/models/baseline_b1_historical_distribution.py
```

定义：

```text
使用历史所有 h 日收益作为未来 h 日收益分布。
```

对每个 horizon：

```text
5D
10D
20D
```

计算：

```text
sample_size
mean_return
median_return
std_return
p05_return
p10_return
p25_return
p50_return
p75_return
p90_return
p95_return
positive_prob
negative_prob
expected_price
p10_price
p50_price
p90_price
```

要求：

```text
不得使用未来数据泄露。
每个 t 的 h 日收益只能用历史 close[t+h] / close[t] 计算。
```

---

### 4.3 B2：状态分组历史收益分布模型

文件：

```text
src/cnsv/models/baseline_b2_state_grouped_distribution.py
```

目标：

```text
在不同状态下，历史未来收益分布不同。
```

分组状态来自 V1.1 feature：

```text
trend_state
volatility_state
flow_strength_basic
price_flow_confirm
price_flow_divergence
```

第一版至少支持以下状态组合：

```text
trend_state
volatility_state
flow_strength_basic
```

例如：

```text
uptrend + normal_vol + positive_flow
downtrend + high_vol + negative_flow
neutral + normal_vol + mixed_flow
```

输出字段：

```text
model_id: B2_state_grouped_distribution
horizon
state_key
state_sample_size
fallback_used
fallback_reason
mean_return
median_return
p10_return
p50_return
p90_return
positive_prob
expected_price
p10_price
p50_price
p90_price
```

样本不足规则：

```text
如果 state_sample_size < 30：
  fallback 到 B1 historical_distribution
  fallback_used = true
```

---

### 4.4 B3：简单波动率调整模型

文件：

```text
src/cnsv/models/baseline_b3_volatility_adjusted.py
```

目标：

```text
用当前波动状态调整未来分布宽度。
```

第一版不做 GARCH，只做简单波动率缩放。

输入：

```text
realized_vol_20d
历史 h 日收益 std
```

定义：

```text
adjusted_std = historical_std * current_vol / long_term_vol
```

输出：

```text
model_id: B3_volatility_adjusted
horizon
mean_return
adjusted_std
volatility_scale
p10_return
p50_return
p90_return
p10_price
p50_price
p90_price
```

限制：

```text
volatility_scale 必须有上下限，例如 0.5 到 2.0。
```

---

## 5. 模型目录结构

新增：

```text
src/cnsv/models/
├── __init__.py
├── baseline_b0_random_walk.py
├── baseline_b1_historical_distribution.py
├── baseline_b2_state_grouped_distribution.py
├── baseline_b3_volatility_adjusted.py
├── baseline_registry.py
├── baseline_runner.py
├── baseline_evaluator.py
└── baseline_schema.py
```

---

## 6. baseline_runner

文件：

```text
src/cnsv/models/baseline_runner.py
```

必须实现：

```python
def run_all_baselines(data_bundle: dict, feature_bundle: dict, horizons: list[int]) -> dict:
    ...
```

输入：

```text
data_bundle
feature_bundle
horizons = [5, 10, 20]
```

输出：

```python
{
    "status": "PASS|WARN|FAIL",
    "generated_at": "",
    "latest_trade_date": "",
    "current_close": 0,
    "horizons": [5, 10, 20],
    "models": {
        "B0_random_walk": {},
        "B1_historical_distribution": {},
        "B2_state_grouped_distribution": {},
        "B3_volatility_adjusted": {}
    },
    "warnings": [],
    "failed_count": 0,
    "warn_count": 0
}
```

---

## 7. baseline_evaluator

文件：

```text
src/cnsv/models/baseline_evaluator.py
```

V1.2 不做完整样本外回测，但必须做基础自检。

必须检查：

```text
1. 每个模型是否输出完整
2. 每个 horizon 是否存在
3. 分位数是否顺序正确：p10 <= p50 <= p90
4. 价格是否为正
5. sample_size 是否足够
6. fallback 是否被标注
7. 不能出现 nan / inf
```

输出：

```python
{
    "status": "PASS|WARN|FAIL",
    "checks": [],
    "failed_count": 0,
    "warn_count": 0
}
```

规则：

```text
缺核心模型 -> FAIL
分位数顺序错误 -> FAIL
价格小于等于 0 -> FAIL
样本不足但有 fallback -> WARN
nan / inf -> FAIL
```

---

## 8. baseline_registry

文件：

```text
src/cnsv/models/baseline_registry.py
```

必须记录：

```text
model_id
model_name
description
input_data
input_features
horizons
output_fields
is_trade_signal
stage
```

所有 V1.2 模型：

```text
is_trade_signal = false
stage = V1.2_baseline_model
```

输出到：

```text
docs/data/baseline_registry.json
```

---

## 9. Baseline Report

### 9.1 JSON 报告

新增：

```text
docs/data/latest_baseline_model_report.json
```

结构：

```json
{
  "meta": {
    "system": "CNSV",
    "version": "1.2.0",
    "report_type": "baseline_model_report",
    "ts_code": "600150.SH",
    "name": "中国船舶",
    "generated_at": "",
    "latest_trade_date": "",
    "is_trade_signal": false
  },
  "cnsvdata_gate": {},
  "feature_quality": {},
  "baseline_quality": {
    "status": "PASS",
    "failed_count": 0,
    "warn_count": 0,
    "checks": []
  },
  "current_state": {
    "latest_close": 0,
    "trend_state": "",
    "volatility_state": "",
    "flow_strength_basic": "",
    "can_use_moneyflow_as_strong_factor": true
  },
  "baseline_models": {
    "B0_random_walk": {},
    "B1_historical_distribution": {},
    "B2_state_grouped_distribution": {},
    "B3_volatility_adjusted": {}
  },
  "baseline_registry": [],
  "forbidden_actions": [
    "formal_signal_generation",
    "auto_order",
    "broker_api"
  ],
  "next_stage": "V1.3 20D path distribution"
}
```

### 9.2 Markdown 报告

新增：

```text
reports/latest_baseline_model_report.md
reports/archive/YYYY-MM-DD_baseline_model_report.md
```

必须包含：

```text
1. Gate 状态
2. Feature Quality 状态
3. Baseline Quality 状态
4. 最新交易日
5. 当前收盘价
6. 当前 trend_state
7. 当前 volatility_state
8. 当前 flow_strength_basic
9. B0 模型摘要
10. B1 模型摘要
11. B2 模型摘要
12. B3 模型摘要
13. 5D / 10D / 20D 分布摘要
14. 样本数量
15. fallback 情况
16. 禁止动作
17. 下一阶段建议
```

### 9.3 HTML 页面

新增：

```text
docs/baseline.html
```

并更新：

```text
docs/index.html
```

`index.html` 增加入口：

```text
Data Report
Feature Report
Baseline Model Report
```

baseline.html 读取：

```text
docs/data/latest_baseline_model_report.json
```

展示：

```text
B0/B1/B2/B3
5D/10D/20D 分位数
当前状态
baseline_quality
forbidden_actions
```

不得写死数据。

---

## 10. CLI 命令

新增：

```bash
python -m cnsv.cli.run_baseline_models
```

必须执行：

```text
1. 读取 CNSVdata
2. 读取 downstream_ready
3. 构建 feature_bundle
4. 运行 B0/B1/B2/B3
5. 运行 baseline_evaluator
6. 输出 latest_baseline_model_report.json
7. 输出 latest_baseline_model_report.md
8. 输出 baseline.html
9. 更新 index.html
```

---

## 11. GitHub Actions

新增：

```text
.github/workflows/run_baseline_models.yml
```

建议内容：

```yaml
name: Run CNSV Baseline Models

on:
  workflow_dispatch:
  schedule:
    - cron: "25 9 * * 1-5"

permissions:
  contents: write

jobs:
  run-baseline-models:
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

      - run: python -m cnsv.cli.run_baseline_models

      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add reports docs
          git diff --cached --quiet || git commit -m "report: update CNSV baseline model report"
          git push
```

说明：

```text
09:25 UTC = 北京时间 17:25
```

执行顺序：

```text
CNSVdata Acceptance：约 16:50
CNSV check_data：约 17:05
CNSV run_features：约 17:15
CNSV run_baseline_models：约 17:25
```

---

## 12. 测试要求

新增测试：

```text
tests/test_baseline_b0_random_walk.py
tests/test_baseline_b1_historical_distribution.py
tests/test_baseline_b2_state_grouped_distribution.py
tests/test_baseline_b3_volatility_adjusted.py
tests/test_baseline_runner.py
tests/test_baseline_evaluator.py
tests/test_baseline_registry.py
tests/test_baseline_report_json.py
tests/test_baseline_cli.py
```

必须测试：

```text
1. B0 输出完整
2. B1 分位数顺序正确
3. B2 样本不足时 fallback 到 B1
4. B3 volatility_scale 有上下限
5. 所有价格输出为正
6. 不出现 nan / inf
7. baseline_evaluator 能识别分位数顺序错误
8. latest_baseline_model_report.json 结构完整
9. run_baseline_models CLI 可运行
10. forbidden_actions 包含 formal_signal_generation
```

测试不得依赖真实网络。

必须使用 mock DataFrame / mock feature_bundle。

---

## 13. V1.2 验收标准

完成后必须能运行：

```bash
pip install -r requirements.txt
pytest
python -m cnsv.cli.run_baseline_models
```

必须生成：

```text
docs/data/latest_baseline_model_report.json
docs/data/baseline_registry.json
reports/latest_baseline_model_report.md
docs/baseline.html
docs/index.html
```

并且：

```text
baseline_quality.status = PASS
failed_count = 0
is_trade_signal = false
can_generate_formal_signal = false
forbidden_actions 包含 formal_signal_generation
```

---

## 14. 本阶段不做

V1.2 不做：

```text
1. 正式买入信号
2. 正式卖出信号
3. 目标仓位
4. 目标股数
5. 止损价
6. 止盈价
7. 20D 路径采样
8. 触碰概率
9. 目标先到概率
10. 止损先到概率
11. 正式回测结论
12. 成交仿真
13. live_assist_mode
14. 自动下单
15. 券商接口
```

V1.2 是基准模型，不是交易系统。

---

## 15. 与后续阶段关系

```text
V1.0 = 数据接线层
V1.1 = 基础特征增强层
V1.2 = 基准模型层
V1.3 = 20D 路径预测层
V1.4 = 回测与成交仿真
V1.5 = 试运行辅助报告
```

V1.2 完成后，才允许进入 V1.3。

---

## 16. Codex 完成后必须汇报

请按以下格式汇报：

```text
一、修改文件清单
二、新增文件清单
三、是否删除文件，如无写无
四、是否改变 CNSVdata 读取路径
五、是否使用 TUSHARE_TOKEN
六、是否生成正式信号
七、pytest 是否通过
八、run_baseline_models.yml 是否可运行
九、latest_baseline_model_report.json 是否生成
十、latest_baseline_model_report.md 是否生成
十一、baseline_quality 当前状态
十二、B0/B1/B2/B3 是否全部输出
十三、是否仍然禁止 formal_signal_generation
十四、是否存在 fallback
十五、下一步建议
```

---

## 17. 给 Codex 的最终执行口令

```text
继续 CNSV 主程序仓库开发。

当前阶段：CNSV V1.2 基准模型层。

V1.0 数据接线层已经跑通，V1.1 基础特征增强与资金流核心层已经完成。现在不要开发正式交易信号，不要开发路径预测，不要开发回测引擎。请只做透明基准模型层。

请一次性完成：

1. 新增 src/cnsv/models/baseline_b0_random_walk.py
2. 新增 src/cnsv/models/baseline_b1_historical_distribution.py
3. 新增 src/cnsv/models/baseline_b2_state_grouped_distribution.py
4. 新增 src/cnsv/models/baseline_b3_volatility_adjusted.py
5. 新增 src/cnsv/models/baseline_registry.py
6. 新增 src/cnsv/models/baseline_runner.py
7. 新增 src/cnsv/models/baseline_evaluator.py
8. 新增 src/cnsv/models/baseline_schema.py
9. 新增 src/cnsv/report/baseline_report_json.py
10. 新增 src/cnsv/report/baseline_report_md.py
11. 新增 src/cnsv/report/baseline_report_html.py
12. 新增 python -m cnsv.cli.run_baseline_models
13. 新增 .github/workflows/run_baseline_models.yml
14. 新增 tests/test_baseline_b0_random_walk.py
15. 新增 tests/test_baseline_b1_historical_distribution.py
16. 新增 tests/test_baseline_b2_state_grouped_distribution.py
17. 新增 tests/test_baseline_b3_volatility_adjusted.py
18. 新增 tests/test_baseline_runner.py
19. 新增 tests/test_baseline_evaluator.py
20. 新增 tests/test_baseline_registry.py
21. 新增 tests/test_baseline_report_json.py
22. 新增 tests/test_baseline_cli.py
23. 更新 README.md
24. 更新 docs/index.html
25. 新增 docs/baseline.html

必须生成：
- docs/data/latest_baseline_model_report.json
- docs/data/baseline_registry.json
- reports/latest_baseline_model_report.md
- docs/baseline.html

严格禁止：
- 不生成正式买卖信号
- 不输出买入/卖出建议
- 不输出目标仓位
- 不输出目标股数
- 不输出止损价/止盈价
- 不开发 20D 路径采样
- 不开发触碰概率
- 不开发目标先到概率
- 不开发回测引擎
- 不连接券商
- 不自动下单
- 不使用 TUSHARE_TOKEN
- 不绕过 CNSVdata
- 不把 baseline_model_report 命名为 signal_report

验收标准：
- pytest 必须通过
- python -m cnsv.cli.run_baseline_models 必须可运行
- latest_baseline_model_report.json 必须生成
- latest_baseline_model_report.md 必须生成
- baseline_quality.status 必须为 PASS
- is_trade_signal 必须为 false
- can_generate_formal_signal 必须仍为 false
- forbidden_actions 必须包含 formal_signal_generation
```

---

## 18. 最重要原则

```text
V1.2 的核心不是预测交易，而是建立以后所有模型必须打败的透明基准。
```

没有基准模型，后面任何复杂模型都没有比较对象。

基准模型是 CNSV 专业化的必经层。
