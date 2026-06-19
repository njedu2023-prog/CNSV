# CNSVdata V1.2 升级后复检与下一阶段补强开发文档

> 适用仓库：`njedu2023-prog/CNSVdata`  
> 当前阶段：V1.1 已完成基础升级，仓库已经从“能跑的数据底座”进入“验收闭环化”的阶段。  
> 下一阶段目标：把 CNSVdata 从“流程已经设计并搭建”升级为“真实运行稳定、失败可定位、历史可追溯、缺口可回补、字段契约可版本化”的专业级量化数据底座。  
> 开发对象：Codex  
> 严格边界：本仓库只做数据采集、标准化、质量检查、快照、血缘、验收、回补和下游读取契约；不做买卖信号、不做交易建议、不做模型预测。

---

## 0. 当前复检结论

当前 CNSVdata 已经明显比 V1.0 完整，已经具备以下能力：

1. `data/preview` 目录已经能看到日线、资金流、交易日历、preview manifest 等人工预览文件。
2. GitHub Actions 已经能够自动更新 daily 数据。
3. 仓库已经具备 `data/processed`、`data/preview`、`metadata`、`data/quality` 等基础目录。
4. 已经有质量检查、验收、下游 smoke read 的开发方向。
5. 项目已经从“空架子”进入“可运行数据底座”的状态。

但从专业量化数据底座角度看，还不能直接判定为 100% 完成。

当前更准确的状态是：

```text
CNSVdata 当前完成度：约 75% - 80%
```

原因：

```text
已经具备基础数据链路和验收框架；
但还需要真实跑通验收、历史快照、失败摘要、自动回补、字段级契约、事件数据做实、下游集成验证。
```

---

## 1. 本次 V1.2 的核心目标

V1.2 不要扩展交易逻辑，不要开发信号系统。

本次重点是把 V1.1 的“验收设计”变成“稳定生产能力”。

核心目标：

```text
1. 验收工作流必须真实跑通
2. 验收结果必须有清晰摘要
3. 每次质量结果必须可追溯
4. 数据缺口必须可检测、可回补
5. 字段契约必须从文件级升级到字段级
6. corporate_actions / structural_breaks 不能只是占位
7. 下游 CNSV 主系统读取必须有明确 READY / NOT_READY 状态
```

---

## 2. 当前最重要的问题

### 2.1 Acceptance 工作流需要真实跑通

如果 `.github/workflows/acceptance.yml` 已经存在，但还没有实际运行成功，则当前只能叫：

```text
验收流程已搭建
```

不能叫：

```text
验收闭环已完成
```

Codex 必须先确保：

```text
Actions -> acceptance.yml -> Run workflow
```

可以真实运行，并产出：

```text
data/quality/data_quality_latest.json
data/quality/acceptance_latest.json
data/quality/downstream_smoke_latest.json
metadata/data_manifest.json
```

如果运行失败，必须输出清晰原因，不允许只给 Python traceback。

---

### 2.2 latest 文件不够，必须有历史快照

当前很多数据文件只保留 latest，例如：

```text
data/quality/acceptance_latest.json
data/quality/downstream_smoke_latest.json
metadata/data_manifest.json
```

这对日常运行方便，但不利于追溯。

一旦未来出现：

```text
某天数据异常
某天策略结果异常
某天模型判断失真
某天分钟线缺失
某天资金流全 0
```

如果只有 latest，就很难回查当时的数据状态。

因此 V1.2 必须增加历史快照。

---

### 2.3 缺少失败摘要

如果验收失败，只在 GitHub Actions 里看到 traceback，后续定位会很慢。

需要新增：

```text
data/quality/failure_summary_latest.md
data/quality/failure_summary_latest.json
```

让人一眼看到：

```text
哪一个文件失败
哪一项检查失败
严重程度
是否阻断下游
建议修复命令
```

---

### 2.4 缺少自动回补机制

数据底座最常见的问题不是“天天彻底失败”，而是：

```text
某个交易日缺失
某个分钟段缺失
moneyflow 延迟
日线更新了但分钟线没更新
manifest 更新了但 quality 没更新
```

因此必须有：

```text
缺口检测
回补脚本
回补后重建 processed
回补后重跑 quality / acceptance / smoke
```

---

### 2.5 字段级 Contract 还不够

当前 contract 多数还是 required_files 级别。

专业下游系统还需要知道：

```text
字段含义
字段单位
字段类型
字段是否允许为空
字段来源
字段是否复权
更新时间
延迟容忍度
是否核心字段
异常时处理方式
```

没有字段级 contract，下游 CNSV 主系统未来会很容易读错字段、读错单位、读错口径。

---

### 2.6 事件数据还需要做实

`corporate_actions.parquet` 和 `structural_breaks.parquet` 如果只是空表或占位文件，对中国船舶波段系统的价值不够。

中国船舶这种标的，事件层很重要：

```text
停复牌
除权除息
重大公告
重组预期
船舶订单
央企整合
行业政策
军工板块事件
异常涨跌停
结构性行情切换
```

这部分如果不做实，后续主系统会缺少解释结构变化的能力。

---

## 3. V1.2 必须完成的任务总表

| 优先级 | 任务 | 目标 |
|---|---|---|
| P0 | 跑通 acceptance workflow | 证明闭环真实可运行 |
| P0 | 新增失败摘要 | 失败后能快速定位 |
| P0 | 下游 READY 状态 | 给 CNSV 主系统明确开关 |
| P1 | 历史快照 | 质量结果可追溯 |
| P1 | 缺口检测 | 发现缺日/缺分钟 |
| P1 | 回补脚本 | 支持补数据 |
| P1 | 字段级 contract | 防止下游读错 |
| P2 | 事件数据做实 | 补 corporate_actions / structural_breaks |
| P2 | README 运维说明 | 人工可执行 |
| P2 | 测试覆盖增强 | 保证升级不漂移 |

---

## 4. 任务一：确保 Acceptance 工作流真实可运行

### 4.1 文件

检查并修复：

```text
.github/workflows/acceptance.yml
```

### 4.2 必须执行的命令顺序

workflow 中必须包含：

```bash
pip install -r requirements.txt
pytest
python scripts/quality_check.py
python scripts/build_data_manifest.py
python scripts/acceptance_check.py
python scripts/smoke_downstream_read.py
```

建议顺序：

```text
1. pytest
2. quality_check.py
3. build_data_manifest.py
4. acceptance_check.py
5. smoke_downstream_read.py
6. build_failure_summary.py
7. commit data/quality metadata
```

注意：

```text
不要使用 continue-on-error: true
不要吞掉异常
不要把失败伪装成成功
```

### 4.3 必须产出的文件

运行成功或失败后，应尽量产出：

```text
data/quality/data_quality_latest.json
data/quality/acceptance_latest.json
data/quality/downstream_smoke_latest.json
data/quality/failure_summary_latest.json
data/quality/failure_summary_latest.md
metadata/data_manifest.json
metadata/downstream_ready.json
```

如果中途失败，也应该尽可能输出 failure summary。

---

## 5. 任务二：新增失败摘要脚本

### 5.1 新增文件

```text
scripts/build_failure_summary.py
```

### 5.2 目标

读取以下文件：

```text
data/quality/data_quality_latest.json
data/quality/acceptance_latest.json
data/quality/downstream_smoke_latest.json
```

生成：

```text
data/quality/failure_summary_latest.json
data/quality/failure_summary_latest.md
```

### 5.3 JSON 输出格式

```json
{
  "status": "FAIL",
  "generated_at": "2026-06-18 16:55:00",
  "blocking": true,
  "failed_count": 2,
  "warn_count": 1,
  "top_failures": [
    {
      "source": "acceptance",
      "name": "daily_close_vs_minute_last_close",
      "status": "FAIL",
      "detail": "daily close and minute last close mismatch",
      "suggested_action": "rerun fetch_minute and rebuild processed data"
    }
  ],
  "top_warnings": [
    {
      "source": "quality",
      "name": "moneyflow_latest_trade_date",
      "status": "WARN",
      "detail": "moneyflow is one trading day behind",
      "suggested_action": "wait for source update or rerun fetch_moneyflow"
    }
  ]
}
```

### 5.4 MD 输出格式

生成一个人能直接看懂的 Markdown：

```markdown
# CNSVdata Failure Summary

## Overall Status

FAIL

## Blocking

true

## Top Failures

### 1. daily_close_vs_minute_last_close

- Source: acceptance
- Status: FAIL
- Detail: daily close and minute last close mismatch
- Suggested action: rerun fetch_minute and rebuild processed data

## Top Warnings

...
```

### 5.5 状态规则

```text
任意 FAIL -> summary status = FAIL
无 FAIL 但有 WARN -> summary status = WARN
全 PASS -> summary status = PASS
```

---

## 6. 任务三：新增下游 READY 状态

### 6.1 新增文件

```text
metadata/downstream_ready.json
```

### 6.2 生成逻辑

可以在 `scripts/smoke_downstream_read.py` 中生成，也可以新增：

```text
scripts/build_downstream_ready.py
```

推荐新增独立脚本：

```text
scripts/build_downstream_ready.py
```

### 6.3 输出格式

```json
{
  "ready": true,
  "status": "PASS",
  "generated_at": "2026-06-18 16:58:00",
  "latest_trade_date": "2026-06-18",
  "quality_status": "PASS",
  "acceptance_status": "PASS",
  "smoke_status": "PASS",
  "contract_version": "1.1.0",
  "manifest_snapshot_id": "cnsvdata-2026-06-18-xxxx",
  "blocking_reason": null
}
```

如果失败：

```json
{
  "ready": false,
  "status": "FAIL",
  "generated_at": "2026-06-18 16:58:00",
  "latest_trade_date": "2026-06-18",
  "quality_status": "PASS",
  "acceptance_status": "FAIL",
  "smoke_status": "FAIL",
  "contract_version": "1.1.0",
  "manifest_snapshot_id": "cnsvdata-2026-06-18-xxxx",
  "blocking_reason": "acceptance_check failed"
}
```

### 6.4 CNSV 主系统未来读取规则

未来 CNSV 主系统应优先读取：

```text
metadata/downstream_ready.json
```

规则：

```text
ready = true  -> 可以读取数据
ready = false -> 不得生成正式交易辅助结果
status = WARN -> 可以观察，但必须降低置信度
status = FAIL -> 阻断
```

---

## 7. 任务四：新增历史快照机制

### 7.1 目标

每次验收后，把关键结果复制一份到按日期归档的目录。

### 7.2 新增脚本

```text
scripts/archive_quality_snapshot.py
```

### 7.3 归档目录建议

```text
data/quality/history/YYYY-MM-DD/
metadata/history/YYYY-MM-DD/
```

例如：

```text
data/quality/history/2026-06-18/data_quality_latest.json
data/quality/history/2026-06-18/acceptance_latest.json
data/quality/history/2026-06-18/downstream_smoke_latest.json
data/quality/history/2026-06-18/failure_summary_latest.json
data/quality/history/2026-06-18/failure_summary_latest.md

metadata/history/2026-06-18/data_manifest.json
metadata/history/2026-06-18/downstream_ready.json
```

### 7.4 文件名策略

可以保留原名，也可以加时间戳。

推荐：

```text
YYYY-MM-DD_HHMMSS_acceptance.json
YYYY-MM-DD_HHMMSS_manifest.json
```

但为了 GitHub 页面简洁，第一版可以按日期目录保存 latest 副本。

### 7.5 注意事项

不要无限膨胀。

可以只保留：

```text
最近 60 个交易日
```

后续再做清理脚本。

---

## 8. 任务五：新增缺口检测脚本

### 8.1 新增文件

```text
scripts/detect_data_gaps.py
```

### 8.2 目标

检测：

```text
日线缺失
分钟线缺失
资金流缺失
交易日历缺失
多周期聚合缺失
```

### 8.3 输入文件

```text
data/processed/trade_calendar.parquet
data/processed/cnsv_daily.parquet
data/processed/cnsv_1min.parquet
data/processed/cnsv_moneyflow.parquet
```

### 8.4 输出文件

```text
data/quality/data_gaps_latest.json
```

### 8.5 输出格式

```json
{
  "status": "PASS",
  "generated_at": "2026-06-18 16:45:00",
  "latest_trade_date": "2026-06-18",
  "checks": [
    {
      "name": "daily_missing_trade_dates",
      "status": "PASS",
      "missing_dates": []
    },
    {
      "name": "minute_missing_trade_dates",
      "status": "WARN",
      "missing_dates": ["2026-06-17"]
    },
    {
      "name": "moneyflow_missing_trade_dates",
      "status": "WARN",
      "missing_dates": ["2026-06-18"]
    }
  ]
}
```

### 8.6 检测逻辑

使用交易日历中：

```text
is_open = 1
```

的日期作为应有交易日。

对比：

```text
daily.trade_date
minute.trade_date
moneyflow.trade_date
```

缺失规则：

```text
daily 缺最新交易日：FAIL
minute 缺最新交易日：FAIL 或 WARN，按数据源延迟策略
moneyflow 缺最新交易日：WARN
moneyflow 连续缺 3 个交易日：FAIL
历史中间缺日：WARN 或 FAIL，取决于是否影响模型训练
```

---

## 9. 任务六：新增回补脚本

### 9.1 新增文件

```text
scripts/backfill_missing_data.py
```

### 9.2 目标

根据：

```text
data/quality/data_gaps_latest.json
```

自动或半自动补齐缺失数据。

### 9.3 第一版建议

第一版不要做过度自动化。

建议支持参数：

```bash
python scripts/backfill_missing_data.py --start-date 20260601 --end-date 20260618 --daily
python scripts/backfill_missing_data.py --start-date 20260601 --end-date 20260618 --minute
python scripts/backfill_missing_data.py --start-date 20260601 --end-date 20260618 --moneyflow
python scripts/backfill_missing_data.py --from-gap-report
```

### 9.4 回补完成后必须自动执行

```bash
python scripts/build_processed_daily.py
python scripts/build_minute_bars.py
python scripts/build_data_manifest.py
python scripts/quality_check.py
python scripts/acceptance_check.py
python scripts/smoke_downstream_read.py
python scripts/build_downstream_ready.py
```

### 9.5 输出文件

```text
data/quality/backfill_latest.json
```

示例：

```json
{
  "status": "PASS",
  "generated_at": "2026-06-18 17:10:00",
  "mode": "from_gap_report",
  "filled": [
    {
      "dataset": "daily",
      "trade_date": "2026-06-17",
      "status": "PASS"
    }
  ],
  "failed": []
}
```

---

## 10. 任务七：字段级 Contract 升级

### 10.1 当前问题

当前 `config/data_contract.yml` 多数是文件级 required_files。

V1.2 需要补字段级契约。

### 10.2 建议新增文件

```text
config/field_contract.yml
```

也可以扩展 `data_contract.yml`，但为了清晰，建议新增独立文件。

### 10.3 字段契约示例

```yaml
contract:
  version: "1.2.0"
  timezone: "Asia/Shanghai"
  datasets:
    cnsv_daily:
      path: "data/processed/cnsv_daily.parquet"
      primary_key: ["trade_date"]
      required: true
      freshness:
        max_lag_trading_days: 0
      fields:
        ts_code:
          type: "string"
          required: true
          nullable: false
          description: "证券代码"
        trade_date:
          type: "string"
          required: true
          nullable: false
          format: "YYYY-MM-DD"
          description: "交易日期"
        open:
          type: "float"
          required: true
          nullable: false
          unit: "CNY"
          description: "开盘价"
        high:
          type: "float"
          required: true
          nullable: false
          unit: "CNY"
          description: "最高价"
        low:
          type: "float"
          required: true
          nullable: false
          unit: "CNY"
          description: "最低价"
        close:
          type: "float"
          required: true
          nullable: false
          unit: "CNY"
          description: "收盘价"
        vol:
          type: "float"
          required: true
          nullable: false
          unit: "shares_or_lots_source_defined"
          description: "成交量，保留数据源原始口径"
        amount:
          type: "float"
          required: true
          nullable: false
          unit: "source_defined"
          description: "成交额，保留数据源原始口径，需在 manifest 中记录 source"
```

### 10.4 质量检查接入

`quality_check.py` 和 `acceptance_check.py` 应读取 `field_contract.yml`，检查：

```text
字段是否存在
字段类型是否符合
是否允许为空
是否核心字段
是否满足 freshness
```

第一版可以先做字段存在性和 nullable 检查，后续再做完整类型验证。

---

## 11. 任务八：事件数据做实

### 11.1 目标

不要让：

```text
corporate_actions.parquet
structural_breaks.parquet
```

长期只是空表或占位文件。

### 11.2 最小可用版本

先做最小可用版本，不追求一次性全覆盖。

#### corporate_actions 最小字段

```text
ts_code
event_date
available_at
event_type
event_name
description
raw_source
impact_level
created_at
```

#### event_type 建议

```text
dividend
ex_right
suspension
resume
announcement
restructure
industry_policy
large_order
other
```

### 11.3 structural_breaks 最小字段

```text
regime_id
start_date
end_date
description
reason
impact_fields
model_action
created_at
```

### 11.4 第一阶段允许人工维护

如果自动抓公告还没接入，第一阶段可以允许：

```text
config/manual_corporate_actions.yml
config/manual_structural_breaks.yml
```

再由脚本生成 parquet。

新增或强化：

```text
scripts/build_corporate_actions.py
scripts/build_structural_breaks.py
```

要求：

```text
允许空表，但空表必须明确 status = WARN 或 empty_allowed = true
不允许文件缺失
不允许 schema 缺字段
```

---

## 12. 任务九：Preview Manifest 强化

### 12.1 当前情况

`data/preview` 里已经有：

```text
cnsv_daily_latest.csv
cnsv_moneyflow_latest.csv
preview_manifest.csv
trade_calendar_latest.csv
```

这说明 preview 已经能输出部分人工预览文件。

### 12.2 需要补充

`preview_manifest.csv` 应记录：

```text
preview_file
source_file
rows
columns
min_date
max_date
generated_at
status
```

### 12.3 Preview 必须覆盖

```text
trade_calendar_latest.csv
cnsv_daily_latest.csv
cnsv_moneyflow_latest.csv
cnsv_1min_latest.csv
cnsv_5min_latest.csv
cnsv_15min_latest.csv
cnsv_30min_latest.csv
cnsv_60min_latest.csv
corporate_actions.csv
structural_breaks.csv
preview_manifest.csv
```

如果某些 source 文件不存在或为空，preview_manifest 中必须标注，不要沉默。

---

## 13. 任务十：README 增加运维指南

README 需要新增：

```text
## V1.2 运维与验收流程
```

内容包括：

### 13.1 每日正常链路

```text
fetch_daily
fetch_minute
build_processed
data_quality_check
acceptance
archive_quality_snapshot
```

### 13.2 手动验收命令

```bash
pip install -r requirements.txt
pytest
python scripts/quality_check.py
python scripts/build_data_manifest.py
python scripts/acceptance_check.py
python scripts/smoke_downstream_read.py
python scripts/build_downstream_ready.py
python scripts/build_failure_summary.py
```

### 13.3 失败定位

```text
优先看：
1. data/quality/failure_summary_latest.md
2. data/quality/acceptance_latest.json
3. data/quality/downstream_smoke_latest.json
4. data/quality/data_quality_latest.json
5. GitHub Actions logs
```

### 13.4 下游读取规则

```text
CNSV 主系统应优先读取 metadata/downstream_ready.json

ready = true:
  可以读取

ready = false:
  不得生成正式交易辅助结果

status = WARN:
  可观察，但必须降低置信度

status = FAIL:
  阻断
```

---

## 14. 测试要求

V1.2 必须补充或强化测试。

### 14.1 新增测试文件

```text
tests/test_failure_summary.py
tests/test_downstream_ready.py
tests/test_data_gaps.py
tests/test_backfill_missing_data.py
tests/test_field_contract.py
tests/test_archive_quality_snapshot.py
```

### 14.2 测试原则

```text
1. 不依赖真实 TUSHARE_TOKEN
2. 使用 tmp_path 构造临时 parquet/json
3. 测试 FAIL/WARN/PASS 聚合逻辑
4. 测试缺文件时必须 FAIL
5. 测试 ready=false 时下游阻断
6. 测试 field_contract 可读取
7. 测试 history 目录可生成
```

### 14.3 pytest 必须通过

```bash
pytest
```

必须在 GitHub Actions 中通过。

---

## 15. Acceptance Workflow 建议最终结构

建议 `.github/workflows/acceptance.yml` 升级为：

```yaml
name: Acceptance

on:
  workflow_dispatch:
  schedule:
    - cron: "50 8 * * 1-5"

permissions:
  contents: write

jobs:
  acceptance:
    runs-on: ubuntu-latest
    env:
      PYTHONPATH: ${{ github.workspace }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - run: pip install -r requirements.txt

      - run: pytest

      - run: python scripts/detect_data_gaps.py

      - run: python scripts/quality_check.py

      - run: python scripts/build_data_manifest.py

      - run: python scripts/acceptance_check.py

      - run: python scripts/smoke_downstream_read.py

      - run: python scripts/build_downstream_ready.py

      - run: python scripts/build_failure_summary.py
        if: always()

      - run: python scripts/archive_quality_snapshot.py
        if: always()

      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add data/quality metadata
          git diff --cached --quiet || git commit -m "data: update acceptance and quality snapshots"
          git push
        if: always()
```

注意：

```text
build_failure_summary.py 和 archive_quality_snapshot.py 可以 if: always()
但核心验收脚本不能 continue-on-error
```

---

## 16. V1.2 完成后的验收标准

Codex 完成后，必须满足：

### 16.1 文件存在

```text
scripts/build_failure_summary.py
scripts/build_downstream_ready.py
scripts/archive_quality_snapshot.py
scripts/detect_data_gaps.py
scripts/backfill_missing_data.py
config/field_contract.yml
metadata/downstream_ready.json
data/quality/failure_summary_latest.json
data/quality/failure_summary_latest.md
data/quality/data_gaps_latest.json
```

### 16.2 命令可运行

```bash
pytest
python scripts/detect_data_gaps.py
python scripts/quality_check.py
python scripts/build_data_manifest.py
python scripts/acceptance_check.py
python scripts/smoke_downstream_read.py
python scripts/build_downstream_ready.py
python scripts/build_failure_summary.py
python scripts/archive_quality_snapshot.py
```

### 16.3 GitHub Actions 可运行

```text
Actions -> Acceptance -> Run workflow
```

运行后必须能在仓库中看到：

```text
data/quality/failure_summary_latest.md
metadata/downstream_ready.json
data/quality/history/
metadata/history/
```

### 16.4 下游 READY 正确

```text
全部 PASS -> ready=true
任何核心 FAIL -> ready=false
WARN -> ready=true 但 status=WARN
```

### 16.5 缺口检测正确

如果手工构造缺失日期，`detect_data_gaps.py` 必须能输出缺失项。

### 16.6 回补脚本不误伤

`backfill_missing_data.py` 不得删除已有数据。

如果回补失败，必须输出失败原因。

---

## 17. 完成后 Codex 必须汇报

Codex 完成后，请按以下格式汇报：

```text
一、修改文件清单
二、新增文件清单
三、删除文件清单，如没有则写无
四、是否改变原有数据路径契约
五、是否触碰 TUSHARE_TOKEN
六、pytest 结果
七、acceptance workflow 是否可运行
八、downstream_ready.json 当前状态
九、failure_summary 当前状态
十、仍然存在的风险
十一、下一步建议
```

---

## 18. 严格禁止事项

```text
1. 不允许为了通过验收强行输出 PASS
2. 不允许把异常吞掉不报
3. 不允许 workflow 使用 continue-on-error 掩盖核心失败
4. 不允许删除已有 data/preview 功能
5. 不允许改动已约定的 processed 路径
6. 不允许写入真实 token
7. 不允许打印 token
8. 不允许生成买卖建议
9. 不允许开发交易信号
10. 不允许修改 CNSV 主系统
```

---

## 19. 本次 V1.2 完成后的预期完成度

如果 V1.2 完成，CNSVdata 完成度可从当前：

```text
75% - 80%
```

提升到：

```text
85% - 90%
```

但仍不是 100%。

后续还需要：

```text
1. 多数据源交叉校验
2. 公告自动抓取
3. 数据漂移监控
4. 外部告警通知
5. 下游 CNSV 主系统正式接入
6. 历史版本冻结
7. 数据血缘可视化
```

---

## 20. 给 Codex 的最终执行口令

请直接复制以下内容给 Codex：

```text
继续 CNSVdata 主线。

当前阶段：V1.2 升级后复检与下一阶段补强。

目标：
把 V1.1 已经搭好的验收框架，升级为真实可运行、失败可定位、历史可追溯、缺口可回补、字段契约可版本化、下游 CNSV 可安全读取的数据底座。

严格边界：
不开发交易信号，不输出买卖建议，不做模型预测，不修改 CNSV 主系统，不改变已有 processed 路径，不删除 preview 功能，不泄露 TUSHARE_TOKEN。

请一次性完成以下任务：

1. 确保 .github/workflows/acceptance.yml 可以真实手动运行和定时运行
2. 新增 scripts/build_failure_summary.py
   - 输出 data/quality/failure_summary_latest.json
   - 输出 data/quality/failure_summary_latest.md
3. 新增 scripts/build_downstream_ready.py
   - 输出 metadata/downstream_ready.json
   - ready=true/false 必须根据 quality、acceptance、smoke 真实状态判断
4. 新增 scripts/archive_quality_snapshot.py
   - 归档 data/quality 和 metadata 的关键结果到 history/YYYY-MM-DD/
5. 新增 scripts/detect_data_gaps.py
   - 检测 daily、minute、moneyflow 的交易日缺口
   - 输出 data/quality/data_gaps_latest.json
6. 新增 scripts/backfill_missing_data.py
   - 支持按 start-date/end-date 回补 daily、minute、moneyflow
   - 支持 --from-gap-report
   - 回补后必须重建 processed、manifest、quality、acceptance、smoke、ready
7. 新增 config/field_contract.yml
   - 把文件级契约升级为字段级契约
   - 至少覆盖 daily、1min、moneyflow、trade_calendar
8. 强化 scripts/build_data_manifest.py
   - manifest 中加入 contract_version、quality_status、ready_status
9. 强化 scripts/build_preview_csv.py
   - preview_manifest.csv 记录 preview_file、source_file、rows、columns、min_date、max_date、generated_at、status
10. 强化 corporate_actions / structural_breaks
   - 如暂时没有自动数据源，允许从 config/manual_corporate_actions.yml 和 config/manual_structural_breaks.yml 生成
   - 不允许文件缺失
   - 空表必须明确 empty_allowed 或 WARN
11. 更新 README.md
   - 增加 V1.2 运维指南
   - 增加失败定位顺序
   - 增加 downstream_ready 读取规则
12. 新增测试：
   - tests/test_failure_summary.py
   - tests/test_downstream_ready.py
   - tests/test_data_gaps.py
   - tests/test_backfill_missing_data.py
   - tests/test_field_contract.py
   - tests/test_archive_quality_snapshot.py

完成要求：
- pytest 必须通过
- acceptance workflow 必须可运行
- FAIL 必须阻断
- WARN 必须说明原因
- downstream_ready.json 必须真实反映能否被 CNSV 下游读取
- 不得用固定 PASS 假装完成
- 不得吞掉异常
- 不得泄露 token
- 不得生成交易建议或买卖信号

完成后请汇报：
1. 修改文件清单
2. 新增文件清单
3. 是否改变原路径契约
4. 是否触碰 TUSHARE_TOKEN
5. pytest 结果
6. acceptance workflow 运行方式
7. downstream_ready 当前状态
8. failure_summary 当前状态
9. 仍有风险
10. 下一步建议
```

---

## 21. 最后原则

CNSVdata 的价值不是“文件多”，而是：

```text
数据真实
质量可查
失败可见
历史可追
缺口可补
下游可控
```

这六件事做实，CNSV 主系统才有可靠地基。
