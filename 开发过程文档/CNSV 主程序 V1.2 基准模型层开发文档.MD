# CNSV 主程序 V1.2 基准模型层开发文档【修正版】

> 仓库：`njedu2023-prog/CNSV`  
> 上游数据仓库：`njedu2023-prog/CNSVdata`  
> 标的：`600150.SH / 中国船舶`  
> 当前阶段：V1.0 数据接线层已完成，V1.1 基础特征增强与资金流核心层已完成，进入 V1.2 基准模型层。  
> 开发对象：Codex  
> 文档定位：本文件是 CNSV 主程序第三阶段开发规格。V1.2 的目标是建立透明、可解释、可测试、可验收的基准模型体系，为后续 20D 路径预测、回测与试运行辅助打基础。  
> 特别说明：本文件不是 V1.1 特征开发文档，不再开发 feature 层主体功能；V1.2 重点是 baseline models。

---

## 0. 当前阶段状态

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

现在进入：

```text
V1.2：基准模型层
```

V1.2 的重点不是再继续扩展特征，而是基于已有 V1.1 特征和 CNSVdata 数据，建立可比较、可解释、可验收的基准模型体系。

---

## 1. V1.2 一句话目标

V1.2 只做一件事：

```text
建立 CNSV 的透明基准模型层。
```

也就是先回答：

```text
不用复杂模型，仅用基础统计和透明方法，中国船舶未来 5D / 10D / 20D 的收益分布大概是什么？
```

以后所有复杂模型都必须和这些基准模型比较。  
如果复杂模型不能稳定打败基准模型，就不能进入正式候选。

---

## 2. V1.2 严格边界

### 2.1 允许开发

```text
1. B0 随机游走 / 不变价格模型
2. B1 历史无条件收益分布模型
3. B2 状态分组历史收益分布模型
4. B3 简单波动率调整模型
5. 5D / 10D / 20D 终点收益分布
6. 分位数输出
7. 正收益概率 / 负收益概率
8. 样本数量统计
9. fallback 机制
10. baseline_evaluator
11. baseline_registry
12. latest_baseline_model_report.json
13. latest_baseline_model_report.md
14. docs/baseline.html
15. run_baseline_models.yml
16. pytest 测试
```

### 2.2 严格禁止

```text
1. 不生成正式买入信号
2. 不生成正式卖出信号
3. 不输出买入建议
4. 不输出卖出建议
5. 不输出目标仓位
6. 不输出目标股数
7. 不输出止损价
8. 不输出止盈价
9. 不开发 20D 路径采样
10. 不开发触碰概率
11. 不开发目标先到概率
12. 不开发止损先到概率
13. 不开发正式回测引擎
14. 不开发成交仿真
15. 不进入 live_assist_mode
16. 不连接券商接口
17. 不自动下单
18. 不使用 TUSHARE_TOKEN
19. 不绕过 CNSVdata
20. 不把 baseline_model_report 命名为 signal_report
```

---

## 3. 输入数据

V1.2 必须复用 V1.0 / V1.1 已经完成的链路。

输入来源：

```text
CNSVdata processed parquet
V1.0 data_bundle
V1.1 feature_bundle
latest_feature_report.json
```

主要使用：

```text
data_bundle["daily"]
data_bundle["moneyflow"]
feature_bundle["price_volume"]
feature_bundle["moneyflow"]
feature_bundle["trend"]
feature_bundle["volatility"]
```

不得直接拉 Tushare。

---

## 4. 预测目标定义

V1.2 只做终点收益分布，不做路径预测。

核心定义：

```text
terminal_return_h = ln(close[t+h] / close[t])
```

其中：

```text
h = 5, 10, 20 个 A 股交易日
```

输出 horizon：

```text
5D
10D
20D
```

V1.2 暂不做：

```text
60D
120D
路径预测
触碰概率
目标先到概率
止损先到概率
交易信号
```

---

## 5. 基准模型 B0：随机游走 / 不变价格模型

新增文件：

```text
src/cnsv/models/baseline_b0_random_walk.py
```

### 5.1 模型定义

B0 是最低基准模型。

```text
未来期望收益 = 0
未来中位价格 = 当前收盘价
分布宽度用近期历史波动估计
```

### 5.2 输入

```text
daily close
当前 latest_close
历史收益波动
horizons = [5, 10, 20]
```

### 5.3 输出字段

```text
model_id
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
sample_size
```

### 5.4 要求

```text
p50_return 应接近 0
p50_price 应接近 current_close
所有价格必须 > 0
```

---

## 6. 基准模型 B1：历史无条件收益分布

新增文件：

```text
src/cnsv/models/baseline_b1_historical_distribution.py
```

### 6.1 模型定义

使用历史所有 h 日收益作为未来 h 日收益的经验分布。

### 6.2 输入

```text
daily close
horizons = [5, 10, 20]
```

### 6.3 输出字段

```text
model_id
horizon
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

### 6.4 要求

```text
不得随机打乱时间序列
不得使用未来数据构造当前状态
分位数必须满足 p05 <= p10 <= p25 <= p50 <= p75 <= p90 <= p95
```

---

## 7. 基准模型 B2：状态分组历史收益分布

新增文件：

```text
src/cnsv/models/baseline_b2_state_grouped_distribution.py
```

### 7.1 模型定义

同样是历史收益分布，但按当前状态筛选历史样本。

状态来自 V1.1 特征：

```text
trend_state
volatility_state
flow_strength_basic
price_flow_confirm
price_flow_divergence
```

第一版至少使用：

```text
trend_state
volatility_state
flow_strength_basic
```

### 7.2 state_key

示例：

```text
uptrend|normal_vol|positive
downtrend|high_vol|negative
neutral|normal_vol|mixed
```

### 7.3 输出字段

```text
model_id
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

### 7.4 fallback 规则

如果：

```text
state_sample_size < 30
```

则：

```text
fallback 到 B1 historical_distribution
fallback_used = true
fallback_reason = "state_sample_size_lt_30"
```

这时不是 FAIL，而是 WARN。

---

## 8. 基准模型 B3：简单波动率调整模型

新增文件：

```text
src/cnsv/models/baseline_b3_volatility_adjusted.py
```

### 8.1 模型定义

基于 B1 的历史收益分布，但用当前波动率状态调整分布宽度。

第一版不做 GARCH，不做复杂波动率模型。

### 8.2 输入

```text
daily close
historical_std
realized_vol_20d
long_term_vol
current_close
horizons = [5, 10, 20]
```

### 8.3 volatility_scale

```text
volatility_scale = realized_vol_20d / long_term_vol
```

必须限制范围：

```text
0.5 <= volatility_scale <= 2.0
```

### 8.4 输出字段

```text
model_id
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

### 8.5 要求

```text
volatility_scale 超出范围时必须 clip
clip 情况需要记录 warning
价格必须 > 0
不能出现 nan / inf
```

---

## 9. 模型目录结构

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

## 10. baseline_runner

新增文件：

```text
src/cnsv/models/baseline_runner.py
```

必须实现：

```python
def run_all_baselines(data_bundle: dict, feature_bundle: dict, horizons: list[int]) -> dict:
    ...
```

输出结构：

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

## 11. baseline_evaluator

新增文件：

```text
src/cnsv/models/baseline_evaluator.py
```

必须检查：

```text
1. B0/B1/B2/B3 是否全部输出
2. 每个模型是否包含 5D/10D/20D
3. 分位数是否顺序正确
4. 价格是否为正
5. sample_size 是否足够
6. fallback 是否被标注
7. 是否出现 nan
8. 是否出现 inf
9. 是否误生成 signal 字段
```

输出：

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
缺核心模型 -> FAIL
缺 horizon -> FAIL
分位数顺序错误 -> FAIL
价格 <= 0 -> FAIL
nan / inf -> FAIL
出现 signal / buy / sell / position 字段 -> FAIL
样本不足但 fallback 正确 -> WARN
```

---

## 12. baseline_registry

新增文件：

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

所有 V1.2 模型必须：

```text
is_trade_signal = false
stage = V1.2_baseline_model
```

输出到：

```text
docs/data/baseline_registry.json
```

---

## 13. Baseline Report

### 13.1 JSON 报告

新增：

```text
docs/data/latest_baseline_model_report.json
```

结构必须包含：

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

### 13.2 Markdown 报告

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

### 13.3 HTML 页面

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

`baseline.html` 读取：

```text
docs/data/latest_baseline_model_report.json
```

展示：

```text
B0/B1/B2/B3
5D/10D/20D 分位数
当前状态
baseline_quality
fallback 情况
forbidden_actions
```

不得写死数据。

---

## 14. CLI 命令

新增：

```bash
python -m cnsv.cli.run_baseline_models
```

必须执行：

```text
1. 读取 CNSVdata
2. 读取 downstream_ready
3. 构建或读取 feature_bundle
4. 运行 B0/B1/B2/B3
5. 运行 baseline_evaluator
6. 输出 latest_baseline_model_report.json
7. 输出 latest_baseline_model_report.md
8. 输出 baseline.html
9. 更新 index.html
```

---

## 15. GitHub Actions

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

北京时间：

```text
17:25
```

---

## 16. 测试要求

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
8. baseline_evaluator 能识别误生成 signal 字段
9. latest_baseline_model_report.json 结构完整
10. run_baseline_models CLI 可运行
11. forbidden_actions 包含 formal_signal_generation
```

测试不得依赖真实网络，必须使用 mock DataFrame / mock feature_bundle。

---

## 17. V1.2 验收标准

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
B0/B1/B2/B3 全部输出
5D/10D/20D 全部输出
```

---

## 18. 本阶段不做

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

## 19. 与后续阶段关系

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

## 20. Codex 完成后必须汇报

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
十三、5D/10D/20D 是否全部输出
十四、是否仍然禁止 formal_signal_generation
十五、是否存在 fallback
十六、下一步建议
```

---

## 21. 给 Codex 的最终执行口令

```text
继续 CNSV 主程序仓库开发。

当前阶段：CNSV V1.2 基准模型层。

注意：当前 GitHub 文件曾出现“文件名 V1.2、正文 V1.1”的问题。请以本文档为准。V1.2 不再继续开发 feature 层主体功能，而是开发 baseline models。

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
14. 新增 baseline 相关 pytest 测试
15. 更新 README.md
16. 更新 docs/index.html
17. 新增 docs/baseline.html

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
- B0/B1/B2/B3 必须全部输出
- 5D/10D/20D 必须全部输出
```

---

## 22. 最重要原则

```text
V1.2 的核心不是预测交易，而是建立以后所有模型必须打败的透明基准。
```

没有基准模型，后面任何复杂模型都没有比较对象。

基准模型是 CNSV 专业化的必经层。
