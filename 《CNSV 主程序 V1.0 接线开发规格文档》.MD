# CNSV 主程序 V1.0 接线开发规格文档

> 仓库：`njedu2023-prog/CNSV`  
> 上游数据仓库：`njedu2023-prog/CNSVdata`  
> 标的：`600150.SH / 中国船舶`  
> 当前阶段：CNSVdata 数据底座已完成当前阶段验收，CNSV 主程序进入 V1.0 接线开发阶段。  
> 开发对象：Codex  
> 文档定位：这是 CNSV 主程序第一阶段的开发执行文档，不是 CNSVdata 开发文档，不替代《CNSV 中国船舶实盘人工量化波段系统总需求文档 V3.2》。

---

## 0. 本文档必须解决的问题

CNSVdata 已经完成当前阶段数据底座验收。

CNSV 主程序现在要做的不是重新拉数据，也不是马上开发正式买卖信号，而是先完成：

```text
安全读取 CNSVdata
识别数据是否可用
建立主程序基础目录
建立数据加载层
建立基础特征层
生成数据状态报告
建立 CI 验收
严格禁止正式信号
```

一句话：

```text
CNSV V1.0 的目标不是预测和交易，而是把主程序地基搭准。
```

---

## 1. 当前项目关系

```text
CNSVdata = 上游数据底座
CNSV = 主程序 / 模型层 / 决策层 / 报告层
```

CNSVdata 负责：

```text
数据采集
数据清洗
processed parquet
preview
manifest
quality
acceptance
downstream_ready
failure_summary
history
backfill
```

CNSV 负责：

```text
读取 CNSVdata
校验数据准入
构建基础特征
运行模型
生成研究报告
生成回测报告
生成试运行辅助报告
未来生成受控人工辅助信号
```

V1.0 阶段只完成前四项：

```text
读取 CNSVdata
校验数据准入
构建基础特征摘要
生成数据状态报告
```

---

## 2. V1.0 严格边界

### 2.1 允许开发

```text
1. 建立 CNSV 主程序基础目录结构
2. 读取 CNSVdata 的 metadata/downstream_ready.json
3. 读取 CNSVdata 的 metadata/data_manifest.json
4. 读取 CNSVdata 的 processed parquet
5. 校验 downstream_ready 的 ready/status/allowed_usage
6. 建立数据加载层
7. 建立基础数据验证层
8. 建立基础量价特征摘要
9. 建立基础分钟结构特征摘要
10. 建立基础资金流特征摘要
11. 生成 latest_data_report.json
12. 生成 latest_data_report.md
13. 生成 docs/index.html
14. 建立 pytest 测试
15. 建立 check_data GitHub Actions
```

### 2.2 严格禁止

```text
1. 不直接拉取 Tushare
2. 不配置 TUSHARE_TOKEN
3. 不绕过 CNSVdata
4. 不连接券商接口
5. 不自动下单
6. 不生成正式买卖信号
7. 不生成高置信强信号
8. 不输出正式交易建议
9. 不开发 live_assist_mode 正式模式
10. 不开发 champion/challenger 自动上线机制
11. 不开发深度学习模型
12. 不把报告命名为 latest_signal
13. 不把 data_report 伪装成 signal
14. 不一次性铺开 V3.2 全部终局功能
```

---

## 3. CNSVdata 接入规则

### 3.1 默认数据源

CNSV 默认从 GitHub raw 读取 CNSVdata：

```text
https://raw.githubusercontent.com/njedu2023-prog/CNSVdata/refs/heads/main
```

### 3.2 第一读取入口

CNSV 主程序必须先读取：

```text
metadata/downstream_ready.json
```

禁止先读 parquet。

正确顺序：

```text
1. metadata/downstream_ready.json
2. metadata/data_manifest.json
3. data/quality/failure_summary_latest.md
4. data/processed/*.parquet
```

### 3.3 downstream_ready 门禁

必须执行以下规则：

```text
ready = false:
  阻断，不读取 parquet，不生成数据报告，只输出阻断原因。

status = FAIL:
  阻断，不读取 parquet，不生成数据报告，只输出失败原因。

status = WARN:
  允许接线开发和观察级读取，但不得生成正式信号。

status = PASS:
  允许正常读取，允许生成数据报告，允许进入后续回测准备。
```

### 3.4 allowed_usage 规则

必须读取并遵守：

```text
allowed_usage.can_develop_cnsv_main_program
allowed_usage.can_run_daily_ingest
allowed_usage.can_run_backtest
allowed_usage.can_use_moneyflow_as_strong_factor
allowed_usage.can_generate_formal_signal
```

执行规则：

```text
can_develop_cnsv_main_program = false:
  主程序停止。

can_run_daily_ingest = false:
  不得执行日常读取。

can_run_backtest = false:
  不得运行正式回测。

can_use_moneyflow_as_strong_factor = false:
  moneyflow 只能低置信使用。

can_generate_formal_signal = false:
  不得生成正式买卖信号。
```

特别强调：

```text
即使 CNSVdata.status = PASS，只要 can_generate_formal_signal = false，CNSV V1.0 也不得生成正式信号。
```

---

## 4. V1.0 必须读取的上游文件

```text
metadata/downstream_ready.json
metadata/data_manifest.json

data/quality/data_quality_latest.json
data/quality/data_gaps_latest.json
data/quality/acceptance_latest.json
data/quality/downstream_smoke_latest.json
data/quality/failure_summary_latest.md

data/processed/trade_calendar.parquet
data/processed/cnsv_daily.parquet
data/processed/cnsv_1min.parquet
data/processed/cnsv_5min.parquet
data/processed/cnsv_15min.parquet
data/processed/cnsv_30min.parquet
data/processed/cnsv_60min.parquet
data/processed/cnsv_moneyflow.parquet
data/processed/corporate_actions.parquet
data/processed/structural_breaks.parquet
```

---

## 5. CNSV V1.0 目录结构

请建立以下目录和文件：

```text
CNSV/
├── .github/
│   └── workflows/
│       ├── check_data.yml
│       └── publish_pages.yml
├── config/
│   ├── data_source.yml
│   ├── runtime.yml
│   └── report.yml
├── src/
│   └── cnsv/
│       ├── __init__.py
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── check_data.py
│       │   ├── build_features.py
│       │   └── generate_data_report.py
│       ├── data/
│       │   ├── __init__.py
│       │   ├── downloader.py
│       │   ├── downstream_ready.py
│       │   ├── data_manifest.py
│       │   ├── loader.py
│       │   ├── validator.py
│       │   └── trade_calendar.py
│       ├── features/
│       │   ├── __init__.py
│       │   ├── price_volume_features.py
│       │   ├── minute_structure_features.py
│       │   ├── moneyflow_features.py
│       │   └── feature_bundle.py
│       ├── report/
│       │   ├── __init__.py
│       │   ├── report_json.py
│       │   ├── report_md.py
│       │   └── report_html.py
│       └── utils/
│           ├── __init__.py
│           ├── io.py
│           └── errors.py
├── reports/
│   └── archive/
├── docs/
│   ├── index.html
│   └── data/
├── tests/
│   ├── test_downstream_ready.py
│   ├── test_data_manifest.py
│   ├── test_loader.py
│   ├── test_features.py
│   ├── test_report_json.py
│   └── test_cli.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 6. 配置文件

### 6.1 config/data_source.yml

```yaml
cnsvdata:
  repo: "njedu2023-prog/CNSVdata"
  branch: "main"
  raw_base_url: "https://raw.githubusercontent.com/njedu2023-prog/CNSVdata/refs/heads/main"

required_remote_files:
  downstream_ready: "metadata/downstream_ready.json"
  data_manifest: "metadata/data_manifest.json"
  failure_summary: "data/quality/failure_summary_latest.md"
  trade_calendar: "data/processed/trade_calendar.parquet"
  daily: "data/processed/cnsv_daily.parquet"
  one_min: "data/processed/cnsv_1min.parquet"
  five_min: "data/processed/cnsv_5min.parquet"
  fifteen_min: "data/processed/cnsv_15min.parquet"
  thirty_min: "data/processed/cnsv_30min.parquet"
  sixty_min: "data/processed/cnsv_60min.parquet"
  moneyflow: "data/processed/cnsv_moneyflow.parquet"
  corporate_actions: "data/processed/corporate_actions.parquet"
  structural_breaks: "data/processed/structural_breaks.parquet"

local_cache:
  enabled: true
  root: ".cache/cnsvdata"
```

### 6.2 config/runtime.yml

```yaml
runtime:
  default_mode: "research_mode"
  require_downstream_ready: true
  fail_on_downstream_fail: true
  allow_formal_signal: false
  allow_live_assist: false
  allow_backtest_when_ready_pass: true
```

### 6.3 config/report.yml

```yaml
report:
  output_json: "docs/data/latest_data_report.json"
  output_md: "reports/latest_data_report.md"
  archive_dir: "reports/archive"
  html_index: "docs/index.html"
```

---

## 7. 数据模块开发要求

### 7.1 src/cnsv/data/downloader.py

实现：

```python
def fetch_text(url: str) -> str:
    ...

def fetch_json(url: str) -> dict:
    ...

def fetch_parquet(url: str):
    ...
```

要求：

```text
支持 raw.githubusercontent.com
支持 timeout
错误信息必须包含 URL
不得吞异常
```

### 7.2 src/cnsv/data/downstream_ready.py

实现：

```python
def load_downstream_ready(source_config: dict) -> dict:
    ...

def evaluate_downstream_gate(payload: dict) -> dict:
    ...
```

返回：

```python
{
    "ready": bool,
    "status": "PASS|WARN|FAIL",
    "can_continue": bool,
    "can_develop": bool,
    "can_run_daily_ingest": bool,
    "can_run_backtest": bool,
    "can_use_moneyflow_as_strong_factor": bool,
    "can_generate_formal_signal": bool,
    "blocking_reason": str | None,
    "warnings": list[str],
}
```

### 7.3 src/cnsv/data/data_manifest.py

实现：

```python
def load_data_manifest(source_config: dict) -> dict:
    ...

def validate_manifest(manifest: dict) -> dict:
    ...
```

必须检查：

```text
snapshot_id
generated_at
latest_trade_date
files
required parquet
sha256
rows
```

### 7.4 src/cnsv/data/loader.py

实现：

```python
def load_all_core_data(source_config: dict) -> dict:
    ...
```

返回：

```python
{
    "downstream_ready": dict,
    "data_manifest": dict,
    "trade_calendar": DataFrame,
    "daily": DataFrame,
    "one_min": DataFrame,
    "five_min": DataFrame,
    "fifteen_min": DataFrame,
    "thirty_min": DataFrame,
    "sixty_min": DataFrame,
    "moneyflow": DataFrame,
    "corporate_actions": DataFrame,
    "structural_breaks": DataFrame,
}
```

必须先读 downstream_ready，判断通过后再读 parquet。

### 7.5 src/cnsv/data/validator.py

实现：

```python
def validate_loaded_data(bundle: dict) -> dict:
    ...
```

检查：

```text
daily 非空
1min 非空
moneyflow 非空
latest_trade_date 一致
daily close 与 1min 最新 close 接近
核心字段齐全
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

---

## 8. 基础特征模块

V1.0 只做特征摘要，不做预测。

### 8.1 price_volume_features.py

输出：

```text
latest_close
latest_pct_chg
latest_volume
latest_amount
ma5
ma10
ma20
ret_1d
ret_5d
ret_20d
volume_ratio_5d
amount_ratio_5d
```

### 8.2 minute_structure_features.py

输出：

```text
latest_intraday_high
latest_intraday_low
latest_intraday_close
intraday_range_pct
close_position_in_day_range
last_30min_return
last_60min_return
intraday_volume_sum
intraday_amount_sum
```

### 8.3 moneyflow_features.py

输出：

```text
net_mf_amount
main_force_available
moneyflow_latest_trade_date
moneyflow_lag_days
moneyflow_strength_basic
moneyflow_warning
can_use_as_strong_factor
```

如果 `allowed_usage.can_use_moneyflow_as_strong_factor = false`，必须标注低置信。

### 8.4 feature_bundle.py

实现：

```python
def build_feature_bundle(data_bundle: dict, gate: dict) -> dict:
    ...
```

输出：

```python
{
    "price_volume": {},
    "minute_structure": {},
    "moneyflow": {},
    "feature_status": "PASS|WARN|FAIL"
}
```

---

## 9. 报告输出

### 9.1 JSON 报告

输出：

```text
docs/data/latest_data_report.json
```

必须包含：

```json
{
  "meta": {
    "system": "CNSV",
    "version": "1.0.0",
    "ts_code": "600150.SH",
    "name": "中国船舶",
    "mode": "research_mode",
    "report_type": "data_status_report"
  },
  "cnsvdata_gate": {
    "ready": true,
    "status": "PASS",
    "can_continue": true,
    "can_run_backtest": true,
    "can_use_moneyflow_as_strong_factor": true,
    "can_generate_formal_signal": false,
    "blocking_reason": null,
    "warnings": []
  },
  "data_manifest": {
    "snapshot_id": "",
    "latest_trade_date": "",
    "generated_at": "",
    "file_count": 0
  },
  "loaded_data_summary": {
    "daily_rows": 0,
    "one_min_rows": 0,
    "moneyflow_rows": 0,
    "latest_trade_date": ""
  },
  "validation": {
    "status": "PASS",
    "failed_count": 0,
    "warn_count": 0,
    "checks": []
  },
  "features": {
    "price_volume": {},
    "minute_structure": {},
    "moneyflow": {}
  },
  "allowed_actions": {
    "can_develop_cnsv_main_program": true,
    "can_run_daily_ingest": true,
    "can_run_backtest": true,
    "can_generate_formal_signal": false
  },
  "forbidden_actions": [
    "formal_signal_generation",
    "auto_order",
    "broker_api"
  ]
}
```

### 9.2 Markdown 报告

输出：

```text
reports/latest_data_report.md
reports/archive/YYYY-MM-DD_data_report.md
```

必须包含：

```text
CNSVdata Gate 状态
是否允许继续
是否允许回测
是否允许使用 moneyflow 强因子
是否允许正式信号
snapshot_id
latest_trade_date
数据行数
量价摘要
分钟结构摘要
资金流摘要
禁止动作
下一步建议
```

### 9.3 HTML 页面

输出：

```text
docs/index.html
```

要求：

```text
读取 docs/data/latest_data_report.json
展示 Gate 状态
展示 latest_trade_date
展示数据行数
展示基础特征
展示 forbidden_actions
```

不允许写死数据。

---

## 10. CLI 命令

### 10.1 检查数据

```bash
python -m cnsv.cli.check_data
```

作用：

```text
读取 downstream_ready
读取 manifest
验证是否允许继续
输出 gate 状态
```

### 10.2 构建特征

```bash
python -m cnsv.cli.build_features
```

作用：

```text
读取 CNSVdata
构建基础量价、分钟、资金流特征
输出控制台摘要
```

### 10.3 生成数据报告

```bash
python -m cnsv.cli.generate_data_report
```

作用：

```text
读取 downstream_ready
读取 manifest
读取 parquet
验证数据
构建特征
输出 JSON
输出 Markdown
输出 HTML
```

---

## 11. GitHub Actions

### 11.1 .github/workflows/check_data.yml

```yaml
name: Check CNSV Data

on:
  workflow_dispatch:
  schedule:
    - cron: "5 9 * * 1-5"

permissions:
  contents: write

jobs:
  check-data:
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

      - run: python -m cnsv.cli.generate_data_report

      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add reports docs
          git diff --cached --quiet || git commit -m "report: update CNSV data status report"
          git push
```

说明：

```text
09:05 UTC = 北京时间 17:05
```

CNSVdata Acceptance 约北京时间 16:50 跑，CNSV 17:05 读取合理。

### 11.2 .github/workflows/publish_pages.yml

第一版可简单发布 `docs/`。

---

## 12. requirements.txt

必须包含：

```text
pandas
pyarrow
requests
PyYAML
pytest
```

可选：

```text
jinja2
```

---

## 13. pyproject.toml

建议新增：

```toml
[project]
name = "cnsv"
version = "1.0.0"
description = "CNSV main program for 600150.SH manual quantitative swing trading assistance"
requires-python = ">=3.11"

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

---

## 14. 测试要求

### 14.1 test_downstream_ready.py

必须测试：

```text
ready=false -> can_continue=false
status=FAIL -> can_continue=false
status=WARN -> can_continue=true 但限制用途
status=PASS -> can_continue=true
can_generate_formal_signal=false -> 禁止正式信号
```

### 14.2 test_data_manifest.py

必须测试：

```text
manifest 缺 snapshot_id -> FAIL
manifest 缺 files -> FAIL
manifest 正常 -> PASS
```

### 14.3 test_loader.py

必须测试：

```text
先读 downstream_ready
ready=false 不继续读 parquet
ready=true 才读 parquet
```

### 14.4 test_features.py

必须测试：

```text
daily 基础特征
minute 基础特征
moneyflow 强因子禁用时降级
```

### 14.5 test_report_json.py

必须测试：

```text
latest_data_report.json 包含 meta
包含 cnsvdata_gate
包含 validation
包含 features
包含 forbidden_actions
```

### 14.6 test_cli.py

必须测试：

```text
CLI 模块可 import
main 函数可调用
```

测试不得依赖真实网络，必须 mock。

---

## 15. V1.0 验收标准

完成后必须满足：

```bash
pip install -r requirements.txt
pytest
python -m cnsv.cli.check_data
python -m cnsv.cli.build_features
python -m cnsv.cli.generate_data_report
```

必须生成：

```text
reports/latest_data_report.md
docs/data/latest_data_report.json
docs/index.html
```

行为必须正确：

```text
ready=false -> 阻断
status=FAIL -> 阻断
status=WARN -> 降级继续
status=PASS -> 正常读取
can_generate_formal_signal=false -> 不生成正式信号
```

---

## 16. 本阶段不做的功能

以下功能不属于 V1.0：

```text
1. 20D 路径预测
2. 目标先到概率
3. 止损先到概率
4. 正式买卖信号
5. 目标仓位
6. 目标股数
7. 风险预算仓位模型
8. 成交仿真
9. Purged walk-forward 回测
10. champion/challenger 模型治理
11. live_assist_mode
12. high confidence signal
13. broker API
14. 自动下单
```

这些以后再做。

---

## 17. 与 V3.2 总需求文档的关系

```text
V3.2 总需求文档 = 终局蓝图
V1.0 接线开发规格 = 当前 Codex 执行任务
```

Codex 必须优先完成 V1.0 接线，不得擅自一次性开发 V3.2 的全部终局功能。

---

## 18. Codex 完成后必须汇报

```text
一、修改文件清单
二、新增文件清单
三、是否删除文件，如无写无
四、是否改变 CNSVdata 读取路径
五、是否配置或使用 TUSHARE_TOKEN
六、是否生成正式信号
七、pytest 是否通过
八、check_data.yml 是否可运行
九、是否生成 latest_data_report.json
十、是否生成 latest_data_report.md
十一、downstream_ready 读取逻辑是否实现
十二、ready=false 是否能阻断
十三、can_generate_formal_signal=false 是否能禁止正式信号
十四、下一步建议
```

---

## 19. 给 Codex 的最终执行口令

```text
继续 CNSV 主程序仓库开发。

当前阶段：CNSV 主程序 V1.0 接线开发。

上游 CNSVdata 已完成当前阶段数据底座验收。CNSV 主程序现在只做第一阶段接线，不做正式交易信号。

请按《CNSV 主程序 V1.0 接线开发规格文档》一次性完成：

1. 建立 CNSV 主程序基础目录结构；
2. 新增 config/data_source.yml、config/runtime.yml、config/report.yml；
3. 新增 src/cnsv/data/downstream_ready.py；
4. 新增 src/cnsv/data/data_manifest.py；
5. 新增 src/cnsv/data/downloader.py；
6. 新增 src/cnsv/data/loader.py；
7. 新增 src/cnsv/data/validator.py；
8. 新增 src/cnsv/features/price_volume_features.py；
9. 新增 src/cnsv/features/minute_structure_features.py；
10. 新增 src/cnsv/features/moneyflow_features.py；
11. 新增 src/cnsv/features/feature_bundle.py；
12. 新增 src/cnsv/report/report_json.py；
13. 新增 src/cnsv/report/report_md.py；
14. 新增 src/cnsv/report/report_html.py；
15. 新增 CLI：
    - python -m cnsv.cli.check_data
    - python -m cnsv.cli.build_features
    - python -m cnsv.cli.generate_data_report
16. 新增 .github/workflows/check_data.yml；
17. 新增 .github/workflows/publish_pages.yml；
18. 新增 pytest 测试；
19. 更新 README.md；
20. 确保生成：
    - reports/latest_data_report.md
    - docs/data/latest_data_report.json
    - docs/index.html

严格禁止：
- 不直接拉 Tushare；
- 不使用 TUSHARE_TOKEN；
- 不绕过 CNSVdata；
- 不生成正式买卖信号；
- 不生成 high confidence signal；
- 不连接券商；
- 不自动下单；
- 不把报告命名为 latest_signal；
- 不一次性开发 V3.2 的全部终局功能。

验收标准：
- pytest 必须通过；
- ready=false 必须阻断；
- status=FAIL 必须阻断；
- status=WARN 必须降级；
- status=PASS 正常读取；
- can_generate_formal_signal=false 必须禁止正式信号；
- latest_data_report.json 必须生成；
- latest_data_report.md 必须生成；
- check_data.yml 必须可运行。
```

---

## 20. 最重要原则

```text
CNSV 主程序第一步不是预测，而是安全读取。
```

V1.0 的成功标准：

```text
能正确读取 CNSVdata；
能识别数据是否可用；
数据不可用时能阻断；
数据可用时能生成基础数据报告；
能严格禁止正式信号。
```

后续阶段：

```text
V1.1 基础特征增强
V1.2 基准模型
V1.3 20D 路径预测
V1.4 回测与成交仿真
V1.5 试运行辅助报告
```
