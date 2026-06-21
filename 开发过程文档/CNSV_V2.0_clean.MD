# CNSV V2.0.MD — 实盘人工决策系统开发文档

> 交付对象：Codex  
> 适用仓库：`https://github.com/njedu2023-prog/CNSV`  
> 当前正式阶段：`CNSV V2.0_live_manual_decision_system`  
> 核心任务：在 V1.0–V1.6 全链路完成后，开发“实盘人工决策系统”，把数据、特征、基准分布、路径分布、观察级回测、人工决策辅助、风控解释整合成一个每日可用的人工量化驾驶舱。  
> 最高边界：V2.0 坚持人工决策、人工下单、系统辅助；不连接券商自动下单，不自动交易，不绕过人工确认。

---

## 0. 版本规则与总路线

继续 CNSV 主程序仓库主线，不回退旧话题，不推倒重来。

仓库：

```text
https://github.com/njedu2023-prog/CNSV
```

正式版本路线只允许使用：

```text
V1.0 数据接线层
V1.1 特征层
V1.2 基准模型层
V1.3 路径分布层
V1.4 观察级回测层
V1.5 人工决策辅助层
V1.6 风控解释层
V2.0 实盘人工决策系统
```

本轮所有报告、registry、README、HTML、workflow 中的版本字段统一使用：

```json
"version": "2.0"
```

本轮 stage 统一使用：

```json
"stage": "V2.0_live_manual_decision_system"
```

不要写三段式子版本号，不要把阶段内修复拆成正式版本。

---

## 1. V2.0 启动前置条件

V2.0 不允许在上游链路失败时直接进入实盘人工使用。

启动前必须满足：

1. V1.0 数据接线层可运行；
2. V1.1 特征层可运行；
3. V1.2 基准模型层可运行；
4. V1.3 路径分布层可运行；
5. V1.4 观察级回测层可运行；
6. V1.5 人工决策辅助层可运行；
7. V1.6 风控解释层可运行；
8. `pytest` 不得失败；
9. GitHub Actions 不得为 failure；
10. `risk_explanation_quality.status` 不得为 `FAIL`；
11. `is_trade_signal = false`；
12. `can_generate_formal_signal = false`；
13. `forbidden_actions` 必须包含：
    - `formal_signal_generation`
    - `auto_order`
    - `broker_api`

如果最新 commit / workflow 仍为 failure：

```text
V2.0 可以开发准备文件，但不能验收为可用系统。
必须先修复 CI / Actions failure。
```

---

## 2. V2.0 核心定位

V2.0 是实盘人工决策系统，不是自动交易系统。

V2.0 的目标是：

```text
把 V1.0–V1.6 的所有证据整合到一个实盘人工驾驶舱。
让人工操作者在一个页面中看到数据状态、模型证据、路径概率、历史观察证据、风险解释、人工复核清单和人工确认区。
```

V2.0 可以输出：

```text
manual_decision_status
manual_review_required
risk_blocked
evidence_complete
evidence_conflict
operator_checklist
operator_notes
manual_action_log
decision_session_id
decision_snapshot_id
```

V2.0 不允许输出：

```text
系统自动买入
系统自动卖出
自动下单
券商接口下单
自动仓位调整
自动止盈
自动止损
无人值守交易
```

一句话：

```text
V2.0 是人工量化驾驶舱，不是自动炒股机器人。
```

---

## 3. V2.0 严禁事项

严禁：

1. 不连接券商接口；
2. 不自动下单；
3. 不自动买入；
4. 不自动卖出；
5. 不自动调整仓位；
6. 不自动设置止盈；
7. 不自动设置止损；
8. 不输出目标股数；
9. 不输出必须执行的交易命令；
10. 不配置或使用 `TUSHARE_TOKEN`；
11. 不绕过 CNSVdata；
12. 不直接从 Tushare 拉数据；
13. 不把系统结论命名成 formal signal；
14. 不把观察等级包装成自动操作；
15. 不把风险等级包装成卖出指令；
16. 不把低风险包装成买入指令；
17. 不把路径触达概率包装成目标价承诺；
18. 不把历史表现包装成未来承诺；
19. 不允许无人工确认的实盘动作；
20. 不允许生成或保存券商交易凭证。

V2.0 的人工状态只能使用非交易命令式状态：

```text
review_required
risk_blocked
evidence_incomplete
ready_for_manual_review
manual_review_completed
no_decision_due_to_risk
```

禁止状态：

```text
buy
sell
hold
increase_position
reduce_position
clear_position
take_profit
stop_loss
target_price
target_position
```

---

## 4. V2.0 与 V1.6 的关系

V1.6 负责解释风险。  
V2.0 负责把风险解释接入人工决策流程。

V1.6 输出：

```text
总体风险等级
主要风险来源
P2 辅助层风险
证据冲突风险
路径下穿风险
最大回撤风险
风险复核清单
```

V2.0 要做：

```text
把这些风险展示到人工驾驶舱；
把风险复核清单变成人工确认流程；
把证据冲突变成人工必须确认的项目；
把高风险状态变成 risk_blocked 或 review_required；
把人工确认结果保存成日志；
```

如果 V1.6 报告缺失或 FAIL：

```text
V2.0 必须阻断，manual_decision_status = evidence_incomplete 或 risk_blocked。
```

---

## 5. V2.0 输入证据

V2.0 必须读取已有产物，不重新发明证据。

必须读取或兼容读取：

```text
docs/data/latest_data_report.json
docs/data/latest_feature_report.json
docs/data/latest_baseline_model_report.json
docs/data/latest_baseline_validation_report.json
docs/data/latest_path_distribution_report.json
docs/data/latest_path_validation_report.json
docs/data/latest_observation_backtest_report.json
docs/data/latest_human_decision_support_report.json
docs/data/latest_risk_explanation_report.json
```

核心输入包括：

```text
cnsvdata_gate
data_quality
feature_quality
baseline_quality
validation_quality
path_quality
path_validation_quality
observation_backtest_quality
human_decision_support_quality
risk_explanation_quality
current_state
baseline_models
path_models
observation_backtest_metrics
human_decision_support
risk_explanation
risk_scenario_cards
risk_review_checklist
forbidden_actions
```

如果任一关键上游证据缺失：

1. 不允许伪造；
2. 不允许 fake 值；
3. 必须降级；
4. 必须写入 `live_decision_evidence_availability`；
5. 必须设置 `manual_review_required = true`；
6. 必须禁止高置信人工决策状态。

---

## 6. V2.0 核心输出模块

### 6.1 实盘状态总览

输出：

```text
latest_trade_date
latest_close
data_status
feature_status
path_status
backtest_status
support_status
risk_status
overall_system_status
manual_decision_status
manual_review_required
```

`overall_system_status` 建议取值：

```text
ready_for_manual_review
degraded
risk_blocked
evidence_incomplete
system_error
```

### 6.2 证据完整性面板

输出：

```text
evidence_availability
missing_evidence
stale_evidence
failed_quality_gates
warning_quality_gates
```

每条必须关联到上游报告路径。

### 6.3 当前状态卡

输出：

```text
current_price_context
trend_state_context
volatility_state_context
flow_strength_context
state_sample_context
```

只能是观察说明，不是交易动作。

### 6.4 路径观察卡

从 V1.3 / V1.4 读取：

```text
terminal_distribution_summary
touch_up_summary
touch_down_summary
drawdown_summary
path_validation_summary
observation_backtest_support
```

### 6.5 风险解释卡

从 V1.6 读取：

```text
overall_risk_level
primary_risk_sources
secondary_risk_sources
risk_scenario_cards
risk_review_checklist
```

### 6.6 证据冲突卡

输出：

```text
evidence_conflict
conflict_reasons
model_disagreement_points
risk_conflict_points
manual_confirmation_required
```

### 6.7 人工复核清单

至少包含：

```text
check_data_freshness
check_latest_trade_date
check_path_downside
check_drawdown_exposure
check_model_conflict
check_p2_fallback
check_evidence_conflict
check_risk_level
check_manual_notes
confirm_no_auto_order
```

### 6.8 人工确认区

允许字段：

```text
operator_name
decision_session_id
decision_snapshot_id
manual_review_timestamp
manual_review_status
operator_notes
manual_confirmation_items
manual_decision_status
```

`manual_review_status` 只能是：

```text
not_started
in_review
completed
blocked_by_risk
blocked_by_missing_evidence
```

### 6.9 人工日志

新增人工日志文件，记录系统证据快照和人工复核状态。

建议路径：

```text
reports/manual_logs/YYYY-MM-DD_manual_decision_log.json
reports/manual_logs/YYYY-MM-DD_manual_decision_log.md
```

日志只记录人工复核与证据状态，不记录自动交易动作。

---

## 7. V2.0 决策状态规则

### 7.1 evidence_incomplete

触发条件：

```text
任一关键上游报告缺失
任一关键 quality gate FAIL
latest_trade_date 不一致
数据 freshness 异常
```

### 7.2 risk_blocked

触发条件：

```text
overall_risk_level = severe
risk_explanation_quality = FAIL
evidence_conflict 严重且未复核
P2 被错误当作核心依赖
出现 forbidden trading field
```

### 7.3 review_required

触发条件：

```text
risk_level = high
human_review_required = true
evidence_conflict = true
P2 fallback_rate 偏高
purged 样本偏少
```

### 7.4 ready_for_manual_review

触发条件：

```text
上游证据完整
无 FAIL
风险等级不是 severe
禁止交易边界完整
```

注意：

```text
ready_for_manual_review 不是可以买，只是可以进入人工复核。
```

---

## 8. V2.0 质量门禁

新增：

```text
live_manual_decision_quality
```

建议结构：

```json
{
  "status": "PASS/WARN/FAIL",
  "failed_count": 0,
  "warn_count": 0,
  "blocking_error_count": 0,
  "checks": []
}
```

### 8.1 必须 FAIL 的情况

1. 出现自动交易字段；
2. 出现 broker order 字段；
3. 出现 buy/sell/position/stop_loss/take_profit/target_price 等字段；
4. 出现 NaN/inf；
5. `is_trade_signal` 不是 false；
6. `auto_order_enabled` 不是 false；
7. `broker_api_enabled` 不是 false；
8. 缺少 `forbidden_actions`；
9. `forbidden_actions` 缺少 `formal_signal_generation`、`auto_order`、`broker_api`；
10. 上游 V1.6 风控解释报告缺失；
11. 上游关键质量门禁 FAIL 但 V2.0 未阻断；
12. 把 P2 当作核心依赖；
13. 输出任何直接交易动作；
14. 报告命名成 signal；
15. 连接券商接口；
16. 自动下单相关代码或字段出现；
17. 伪造缺失证据；
18. 版本字段不是 `"2.0"`；
19. workflow failure 仍然验收为可用；
20. 人工日志中出现自动下单记录。

### 8.2 可以 WARN 的情况

1. risk_explanation_quality = WARN；
2. human_decision_support_quality = WARN；
3. human_review_required = true；
4. evidence_conflict = true；
5. overall_risk_level = high；
6. P2 fallback_rate 偏高；
7. purged 样本数偏少；
8. 数据 freshness 有提醒；
9. manual_decision_status = review_required；
10. manual_review_status = not_started。

---

## 9. 报告结构要求

新增 JSON：

```text
docs/data/latest_live_manual_decision_report.json
```

建议结构：

```json
{
  "meta": {
    "system": "CNSV",
    "version": "2.0",
    "stage": "V2.0_live_manual_decision_system",
    "report_type": "live_manual_decision_report",
    "ts_code": "600150.SH",
    "name": "中国船舶",
    "generated_at": "...",
    "latest_trade_date": "...",
    "is_trade_signal": false
  },
  "cnsvdata_gate": {},
  "live_decision_evidence_availability": {},
  "live_manual_decision_quality": {},
  "live_state_overview": {},
  "evidence_dashboard": {},
  "current_state_card": {},
  "path_observation_card": {},
  "risk_explanation_card": {},
  "evidence_conflict_card": {},
  "manual_review_checklist": [],
  "manual_confirmation_panel": {},
  "manual_decision_status": "review_required",
  "auto_order_enabled": false,
  "broker_api_enabled": false,
  "formal_signal_enabled": false,
  "forbidden_actions": [
    "formal_signal_generation",
    "auto_order",
    "broker_api"
  ],
  "next_stage": "V2.0 acceptance and daily manual operation"
}
```

新增 registry：

```text
docs/data/live_manual_decision_registry.json
```

新增 MD 报告：

```text
reports/latest_live_manual_decision_report.md
reports/archive/YYYY-MM-DD_live_manual_decision_report.md
```

新增 HTML 页面：

```text
docs/live.html
```

新增人工日志目录：

```text
reports/manual_logs/
```

并更新：

```text
docs/index.html
```

增加入口：

```text
Live Manual Decision Report
```

---

## 10. Markdown 报告要求

`reports/latest_live_manual_decision_report.md` 必须用中文说明：

1. 当前阶段是 V2.0；
2. 这是实盘人工决策系统，不是自动交易系统；
3. 使用了哪些上游证据；
4. 上游证据是否完整；
5. 当前系统状态；
6. 当前人工决策状态；
7. 路径观察摘要；
8. 风险解释摘要；
9. 证据冲突摘要；
10. 人工复核清单；
11. 人工确认区；
12. 禁止自动交易声明；
13. 是否可进入每日人工使用；
14. 如不可使用，原因是什么。

MD 报告不允许出现：

```text
建议买入
建议卖出
止盈
止损
目标仓位
目标股数
目标价
自动下单
```

---

## 11. HTML 页面要求

新增：

```text
docs/live.html
```

页面至少展示：

```text
V2.0 阶段说明
live_manual_decision_quality
live_state_overview
evidence_dashboard
current_state_card
path_observation_card
risk_explanation_card
evidence_conflict_card
manual_review_checklist
manual_confirmation_panel
manual_decision_status
auto_order_enabled = false
broker_api_enabled = false
formal_signal_enabled = false
禁止自动交易声明
```

更新：

```text
docs/index.html
```

新增入口：

```text
Live Manual Decision Report
```

不得出现：

```text
Buy
Sell
Position
Stop Loss
Take Profit
Target Price
Auto Order
Broker Order
```

---

## 12. 建议新增文件结构

```text
src/cnsv/live/__init__.py
src/cnsv/live/live_evidence_loader.py
src/cnsv/live/live_state.py
src/cnsv/live/live_decision_rules.py
src/cnsv/live/manual_checklist.py
src/cnsv/live/manual_confirmation.py
src/cnsv/live/manual_log.py
src/cnsv/live/live_evaluator.py
src/cnsv/live/live_report.py
src/cnsv/live/live_registry.py
```

新增 CLI：

```text
src/cnsv/cli/run_live_manual_decision.py
```

新增测试：

```text
tests/test_live_evidence_loader.py
tests/test_live_state.py
tests/test_live_decision_rules.py
tests/test_manual_checklist.py
tests/test_manual_confirmation.py
tests/test_manual_log.py
tests/test_live_evaluator.py
tests/test_live_report.py
tests/test_live_registry.py
tests/test_live_manual_decision_cli.py
```

新增 workflow：

```text
.github/workflows/run_live_manual_decision.yml
```

---

## 13. CLI 命令要求

新增命令：

```bash
python -m cnsv.cli.run_live_manual_decision
```

该命令必须：

1. 读取 CNSVdata gate；
2. 读取 V1.0–V1.6 已有报告；
3. 检查上游证据可用性；
4. 检查全链路 quality gates；
5. 构造 live_decision_evidence_availability；
6. 构造 live_state_overview；
7. 构造 evidence_dashboard；
8. 构造 current_state_card；
9. 构造 path_observation_card；
10. 构造 risk_explanation_card；
11. 构造 evidence_conflict_card；
12. 构造 manual_review_checklist；
13. 构造 manual_confirmation_panel；
14. 计算 manual_decision_status；
15. 执行 live_manual_decision_quality；
16. 生成 JSON；
17. 生成 registry；
18. 生成 MD；
19. 生成 HTML；
20. 更新 docs/index.html；
21. 写入 archive；
22. 写入 manual_logs。

---

## 14. GitHub Actions 要求

新增：

```text
.github/workflows/run_live_manual_decision.yml
```

要求执行：

```bash
pip install -r requirements.txt
pytest
python -m cnsv.cli.generate_data_report
python -m cnsv.cli.generate_feature_report
python -m cnsv.cli.run_baseline_models
python -m cnsv.cli.run_baseline_validation
python -m cnsv.cli.run_path_distribution
python -m cnsv.cli.run_path_validation
python -m cnsv.cli.run_observation_backtest
python -m cnsv.cli.run_human_decision_support
python -m cnsv.cli.run_risk_explanation
python -m cnsv.cli.run_live_manual_decision
```

提交产物：

```text
docs/data/latest_live_manual_decision_report.json
docs/data/live_manual_decision_registry.json
reports/latest_live_manual_decision_report.md
reports/archive/*_live_manual_decision_report.md
reports/manual_logs/*_manual_decision_log.json
reports/manual_logs/*_manual_decision_log.md
docs/live.html
docs/index.html
```

不要破坏现有 workflow。

---

## 15. 测试要求

必须新增并跑通测试。

### 15.1 上游证据读取测试

构造 mock V1.0–V1.6 报告。

断言：

```text
live_decision_evidence_availability 正确
缺失报告能被记录
缺失报告不会被伪造
```

### 15.2 人工决策状态测试

构造不同场景。

断言：

```text
evidence_incomplete 正确
risk_blocked 正确
review_required 正确
ready_for_manual_review 正确
```

### 15.3 禁止自动交易测试

断言：

```text
auto_order_enabled = false
broker_api_enabled = false
formal_signal_enabled = false
```

如果出现：

```text
buy_signal
sell_signal
target_position
stop_loss
take_profit
target_price
broker_order
auto_order
```

必须 FAIL。

### 15.4 人工复核清单测试

断言至少包含：

```text
check_data_freshness
check_latest_trade_date
check_path_downside
check_drawdown_exposure
check_model_conflict
check_p2_fallback
check_evidence_conflict
check_risk_level
confirm_no_auto_order
```

### 15.5 人工日志测试

断言：

```text
manual_log 能生成
manual_log 包含 decision_session_id
manual_log 包含 evidence snapshot
manual_log 不包含自动下单字段
```

### 15.6 CLI 测试

执行：

```bash
python -m cnsv.cli.run_live_manual_decision
```

断言生成：

```text
docs/data/latest_live_manual_decision_report.json
docs/data/live_manual_decision_registry.json
reports/latest_live_manual_decision_report.md
docs/live.html
docs/index.html
reports/manual_logs/
```

---

## 16. 自检命令

完成后必须执行：

```bash
pip install -r requirements.txt
pytest
python -m cnsv.cli.generate_data_report
python -m cnsv.cli.generate_feature_report
python -m cnsv.cli.run_baseline_models
python -m cnsv.cli.run_baseline_validation
python -m cnsv.cli.run_path_distribution
python -m cnsv.cli.run_path_validation
python -m cnsv.cli.run_observation_backtest
python -m cnsv.cli.run_human_decision_support
python -m cnsv.cli.run_risk_explanation
python -m cnsv.cli.run_live_manual_decision
```

不允许只改代码不跑测试。

---

## 17. 最终输出要求

完成后请给我简洁说明，必须包含：

1. 修改了哪些文件；
2. 是否新增 V2.0 实盘人工决策系统；
3. 是否仍然严格禁止自动交易；
4. 是否生成 live manual decision JSON；
5. 是否生成 live manual decision MD；
6. 是否生成 live.html；
7. 是否更新 index.html；
8. 是否生成 manual_logs；
9. 是否读取 V1.0–V1.6 上游证据；
10. live_decision_evidence_availability 结果；
11. live_manual_decision_quality 结果；
12. manual_decision_status 结果；
13. auto_order_enabled 是否为 false；
14. broker_api_enabled 是否为 false；
15. formal_signal_enabled 是否为 false；
16. 是否仍然把 P2 作为辅助；
17. pytest 结果；
18. run_live_manual_decision 结果；
19. GitHub Actions 是否 success；
20. 最新报告路径；
21. 是否可以进入每日人工使用。

---

## 18. V2.0 验收标准

V2.0 通过条件：

1. `pytest` 通过；
2. `run_live_manual_decision` 通过；
3. GitHub Actions success；
4. `latest_live_manual_decision_report.json` 正常生成；
5. `live_manual_decision_quality.status` 不得为 FAIL；
6. 上游证据读取完整或缺失时已降级；
7. live_decision_evidence_availability 存在；
8. live_state_overview 存在；
9. evidence_dashboard 存在；
10. current_state_card 存在；
11. path_observation_card 存在；
12. risk_explanation_card 存在；
13. evidence_conflict_card 存在；
14. manual_review_checklist 存在；
15. manual_confirmation_panel 存在；
16. manual_decision_status 合法；
17. manual_logs 存在；
18. 无 NaN/inf；
19. 无交易信号字段；
20. `is_trade_signal = false`；
21. `auto_order_enabled = false`；
22. `broker_api_enabled = false`；
23. `formal_signal_enabled = false`；
24. `forbidden_actions` 包含 `formal_signal_generation`、`auto_order`、`broker_api`；
25. `docs/live.html` 存在；
26. `docs/index.html` 有 live manual decision 入口；
27. README 或开发文档说明 V2.0；
28. 不出现券商自动交易接口；
29. 不出现自动下单逻辑；
30. 不出现系统直接操作建议。

---

## 19. V2.0 与未来扩展边界

V2.0 是实盘人工决策系统，不是自动交易系统。

未来如果要做自动交易，必须单独立项，不能在 V2.0 内偷偷加入。

自动交易需要另行验收：

```text
券商接口合规
账户权限
下单权限
撤单权限
风控阈值
人工授权
交易日志
异常熔断
法律合规
安全审计
```

当前 V2.0 不允许包含这些能力。

---

## 20. 核心原则

V1.6 解决的是：

```text
这些证据背后的风险来自哪里，为什么有风险，人工需要复核什么。
```

V2.0 要解决的是：

```text
如何把所有证据和风险解释放到一个可供人工每日使用的实盘驾驶舱。
```

V2.0 最重要的专业判断：

```text
实盘人工决策不是自动交易。
人工驾驶舱不是券商接口。
人工复核状态不是买卖指令。
风险阻断不是自动卖出。
低风险不是自动买入。
系统负责证据、风险、日志和复核流程；最终操作由人工独立完成。
```

只有 V2.0 通过验收后，才允许进入每日人工使用。
