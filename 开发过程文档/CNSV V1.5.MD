# CNSV V1.5.MD — 人工决策辅助层开发文档

> 交付对象：Codex
> 适用仓库：`https://github.com/njedu2023-prog/CNSV`
> 当前正式阶段：`CNSV V1.5_human_decision_support`
> 核心任务：在 V1.4 观察级回测层之后，开发人工决策辅助层，把 V1.0–V1.4 的数据、特征、基准分布、路径分布、观察级回测证据，整合成可供人工阅读、复核和判断的辅助报告。
> 最高边界：V1.5 仍然不是实盘交易系统，不输出买卖指令，不输出仓位，不输出止盈止损，不连接券商，不自动下单。

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
"version": "1.5"
```

本轮 stage 统一使用：

```json
"stage": "V1.5_human_decision_support"
```

不要写三段式子版本号或类似碎片化版本。

---

## 1. 当前阶段锚点

当前已完成：

1. V1.0 数据接线层；
2. V1.1 特征层；
3. V1.2 基准模型层；
4. V1.3 路径分布层；
5. V1.4 观察级回测层；
6. V1.4 已生成观察级回测证据：
   - `latest_observation_backtest_report.json`
   - `observation_backtest_registry.json`
   - `latest_observation_backtest_report.md`
   - `docs/backtest.html`
7. V1.4 已明确：
   - `is_trade_signal = false`
   - `backtest_type = observation_only`
   - 禁止正式交易信号；
   - 禁止券商接口；
   - 禁止自动下单。

本轮任务：

```text
CNSV V1.5 —— Human Decision Support Layer / 人工决策辅助层
```

V1.5 要回答的问题：

```text
基于 V1.0–V1.4 的证据，系统应该怎样帮助人工操作者理解当前状态、路径机会、路径风险、模型一致性和需要人工确认的关键点？
```

V1.5 不是自动决策层。V1.5 只把证据整理成“人工可读、人工可判断、人工可复核”的辅助报告。

---

## 2. V1.5 核心定位

V1.5 是人工决策辅助层，不是正式交易信号层。

V1.5 可以输出：

```text
当前状态摘要
模型证据摘要
路径分布摘要
观察级回测证据摘要
风险等级摘要
模型一致性摘要
人工关注点
人工复核清单
证据强弱等级
观察优先级
是否允许进入 V1.6
```

V1.5 不可以输出：

```text
应该买
应该卖
买入价
卖出价
目标仓位
目标股数
止盈价
止损价
清仓
加仓
减仓
自动下单
券商接口
```

一句话：

```text
V1.5 只能辅助人工理解，不替人工做交易决定。
```

---

## 3. V1.5 严禁事项

本轮仍然不是交易系统。

严禁：

1. 不生成买入信号；
2. 不生成卖出信号；
3. 不输出目标仓位；
4. 不输出目标股数；
5. 不输出止盈；
6. 不输出止损；
7. 不输出目标价；
8. 不输出交易建议；
9. 不输出“建议买入”；
10. 不输出“建议卖出”；
11. 不输出“加仓”；
12. 不输出“减仓”；
13. 不输出“清仓”；
14. 不输出“持有”这类直接操作结论；
15. 不连接券商接口；
16. 不自动下单；
17. 不配置或使用 `TUSHARE_TOKEN`；
18. 不绕过 CNSVdata；
19. 不直接从 Tushare 拉数据；
20. 不把 report 命名成 signal；
21. 不把观察优先级包装成交易指令；
22. 不把历史表现包装成未来承诺；
23. 不因为某个指标强就输出操作动作。

允许输出：

```text
观察结论
证据结论
风险结论
人工关注等级
人工复核事项
路径偏强 / 偏弱
风险偏高 / 偏低
模型一致 / 分歧
证据充分 / 证据不足
下一步人工需要看什么
```

---

## 4. V1.5 与 V1.4 的关系

V1.4 负责回答：

```text
这些路径判断在历史上有没有参考价值？
```

V1.5 负责回答：

```text
在当前交易日，哪些证据可以给人工参考？
哪些证据强？
哪些证据弱？
哪些证据冲突？
哪些风险需要人工优先关注？
```

V1.5 必须复用 V1.4 的观察级回测证据，不允许跳过 V1.4 直接做人工辅助结论。

如果 V1.4 报告不存在、质量 FAIL、或样本不足，V1.5 必须降级，并在报告中写明：

```text
observation_backtest_evidence_unavailable
observation_backtest_quality_failed
insufficient_observation_evidence
```

---

## 5. V1.5 输入证据

V1.5 必须从已有产物读取，不重新发明证据。

必须读取或兼容读取：

```text
docs/data/latest_data_report.json
docs/data/latest_feature_report.json
docs/data/latest_baseline_model_report.json
docs/data/latest_baseline_validation_report.json
docs/data/latest_path_distribution_report.json
docs/data/latest_path_validation_report.json
docs/data/latest_observation_backtest_report.json
```

核心输入证据包括：

```text
data_quality
feature_quality
baseline_quality
validation_quality
path_quality
path_validation_quality
observation_backtest_quality
current_state
baseline_models
path_models
model_backtest_metrics
observation_bucket_metrics
model_comparison
observation_condition_quality
leakage_checks
forbidden_actions
```

如果某个上游报告缺失：

1. 不允许伪造；
2. 不允许用 fake 值填充；
3. 必须降级；
4. 必须在 `evidence_availability` 中写明缺失项；
5. 不得输出高置信度辅助结论。

---

## 6. V1.5 核心输出模块

### 6.1 当前状态摘要

输出：

```text
latest_trade_date
latest_close
trend_state
volatility_state
flow_strength_basic
data_quality_status
feature_quality_status
cnsvdata_gate_status
```

解释当前状态时只能使用观察语言。

### 6.2 模型证据摘要

整合：

```text
B0/B1/B2/B3 baseline distribution
P0/P1/P2 path distribution
V1.4 observation backtest evidence
```

输出：

```text
terminal_distribution_summary
path_distribution_summary
observation_backtest_summary
model_support_summary
```

### 6.3 路径机会观察

基于路径分布和观察级回测输出：

```text
upside_path_observation
touch_up_observation
positive_terminal_observation
historical_support_level
evidence_strength
```

禁止把该模块写成买入理由。

### 6.4 路径风险观察

基于下穿概率、最大回撤、回测风险分组输出：

```text
downside_path_observation
drawdown_observation
touch_down_observation
risk_evidence_level
risk_attention_level
```

禁止把该模块写成止损指令。

### 6.5 模型一致性摘要

比较：

```text
B1 vs B3
P0 vs P1
P2 vs P1
baseline vs path
path vs backtest evidence
```

输出：

```text
model_consistency_status
model_disagreement_points
evidence_conflict_summary
```

一致性状态只能使用：

```text
consistent
mostly_consistent
mixed
divergent
insufficient_evidence
```

### 6.6 人工关注点

输出人工需要重点看的内容：

```text
attention_items
risk_items
data_items
model_items
evidence_items
```

每条必须是“需要人工确认/关注”的观察事项，不是操作建议。

### 6.7 人工复核清单

输出：

```text
check_data_freshness
check_market_context
check_industry_context
check_intraday_behavior
check_path_risk
check_model_conflict
check_evidence_quality
```

V1.5 不需要自动抓取外部新闻或行业数据；只生成内部系统复核清单。

---

## 7. 人工辅助等级设计

V1.5 可以输出人工辅助等级，但不能输出交易动作。

允许等级：

```text
observation_priority
risk_attention_level
evidence_strength
model_consistency_level
human_review_required
```

建议取值：

```text
observation_priority: low / medium / high
risk_attention_level: low / medium / high
evidence_strength: weak / moderate / strong / insufficient
model_consistency_level: consistent / mostly_consistent / mixed / divergent / insufficient
human_review_required: true / false
```

禁止等级：

```text
buy_level
sell_level
position_level
entry_level
exit_level
stop_loss_level
take_profit_level
```

输出中不得出现这些字段。

---

## 8. 证据融合规则

V1.5 必须以证据融合为主，不允许单指标决定结论。

建议证据分层：

```text
data_layer
feature_layer
baseline_layer
path_layer
backtest_layer
risk_layer
consistency_layer
```

### 8.1 证据强度

证据强度根据以下因素评估：

```text
上游质量是否 PASS
样本数是否充足
purged 样本是否可用
观察分组是否有区分度
Brier / coverage 是否合理
模型之间是否一致
P2 fallback_rate 是否偏高
是否存在数据缺失或 unknown 状态
```

输出：

```text
evidence_strength = strong / moderate / weak / insufficient
```

### 8.2 证据冲突

如果出现以下情况，必须标记 evidence_conflict：

```text
路径上行概率高，但回测证据弱
触达概率高，但下穿风险也高
P1 与 P0 方向明显不一致
P2 与 P1 方向明显不一致
P2 fallback_rate 偏高
数据或特征质量不是 PASS
```

输出：

```text
evidence_conflict = true / false
evidence_conflict_reasons = []
```

### 8.3 降级规则

以下情况必须降级：

```text
任一关键上游报告缺失
observation_backtest_quality 为 FAIL
path_quality 为 FAIL
path_validation_quality 为 FAIL
leakage_checks 未 PASS
样本数不足
P2 fallback_rate 过高且被错误当作核心证据
出现 forbidden trading fields
```

降级结果：

```text
support_quality.status = WARN 或 FAIL
evidence_strength = insufficient 或 weak
human_review_required = true
```

---

## 9. V1.5 质量门禁

新增：

```text
human_decision_support_quality
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

### 9.1 必须 FAIL 的情况

1. 出现交易信号字段；
2. 出现 buy/sell/position/stop_loss/take_profit/target_price 等字段；
3. 出现 NaN/inf；
4. `is_trade_signal` 不是 false；
5. 缺少 `forbidden_actions`；
6. `forbidden_actions` 缺少 `formal_signal_generation`、`auto_order`、`broker_api`；
7. 上游 V1.4 observation backtest 报告缺失；
8. 上游关键质量门禁 FAIL 但 V1.5 仍输出高置信辅助结论；
9. 把 P2 当作核心依赖；
10. 输出任何直接交易动作；
11. 报告命名成 signal；
12. 连接券商接口；
13. 自动下单相关代码或字段出现；
14. 伪造缺失证据；
15. 版本字段不是 `"1.5"`。

### 9.2 可以 WARN 的情况

1. 某个上游报告缺失但已降级；
2. P2 fallback_rate 偏高；
3. 模型证据冲突；
4. 观察条件证据弱；
5. purged 样本数偏少；
6. 状态字段存在 unknown；
7. 数据 freshness 不足；
8. 风险证据强于机会证据；
9. evidence_strength 为 weak 或 insufficient；
10. human_review_required 为 true。

---

## 10. 报告结构要求

新增 JSON：

```text
docs/data/latest_human_decision_support_report.json
```

建议结构：

```json
{
  "meta": {
    "system": "CNSV",
    "version": "1.5",
    "stage": "V1.5_human_decision_support",
    "report_type": "human_decision_support_report",
    "ts_code": "600150.SH",
    "name": "中国船舶",
    "generated_at": "...",
    "latest_trade_date": "...",
    "is_trade_signal": false
  },
  "cnsvdata_gate": {},
  "evidence_availability": {},
  "human_decision_support_quality": {},
  "current_state_summary": {},
  "model_evidence_summary": {},
  "path_opportunity_observation": {},
  "path_risk_observation": {},
  "model_consistency_summary": {},
  "evidence_conflict_summary": {},
  "human_attention_items": [],
  "human_review_checklist": [],
  "support_levels": {
    "observation_priority": "low/medium/high",
    "risk_attention_level": "low/medium/high",
    "evidence_strength": "weak/moderate/strong/insufficient",
    "model_consistency_level": "consistent/mostly_consistent/mixed/divergent/insufficient",
    "human_review_required": true
  },
  "forbidden_actions": [
    "formal_signal_generation",
    "auto_order",
    "broker_api"
  ],
  "next_stage": "V1.6 risk explanation"
}
```

新增 registry：

```text
docs/data/human_decision_support_registry.json
```

新增 MD 报告：

```text
reports/latest_human_decision_support_report.md
reports/archive/YYYY-MM-DD_human_decision_support_report.md
```

新增 HTML 页面：

```text
docs/decision_support.html
```

并更新：

```text
docs/index.html
```

增加入口：

```text
Human Decision Support Report
```

---

## 11. Markdown 报告要求

`reports/latest_human_decision_support_report.md` 必须用中文说明：

1. 当前阶段是 V1.5；
2. 这是人工决策辅助，不是交易信号；
3. 使用了哪些上游证据；
4. 哪些上游证据可用；
5. 哪些上游证据缺失或降级；
6. 当前状态摘要；
7. 路径机会观察；
8. 路径风险观察；
9. V1.4 观察级回测支持情况；
10. 模型一致性与分歧；
11. 证据强度；
12. 风险关注等级；
13. 人工关注点；
14. 人工复核清单；
15. 是否允许进入 V1.6；
16. 明确声明：这不是买卖建议，不构成交易指令。

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

## 12. HTML 页面要求

新增：

```text
docs/decision_support.html
```

页面至少展示：

```text
V1.5 阶段说明
human_decision_support_quality
evidence_availability
current_state_summary
model_evidence_summary
path_opportunity_observation
path_risk_observation
model_consistency_summary
evidence_conflict_summary
human_attention_items
human_review_checklist
support_levels
禁止交易信号声明
```

更新：

```text
docs/index.html
```

新增入口：

```text
Human Decision Support Report
```

不得出现：

```text
Buy
Sell
Position
Stop Loss
Take Profit
Target Price
```

---

## 13. 建议新增文件结构

请根据仓库实际结构实现，可微调路径，但职责要清晰。

```text
src/cnsv/support/__init__.py
src/cnsv/support/evidence_loader.py
src/cnsv/support/evidence_fusion.py
src/cnsv/support/support_levels.py
src/cnsv/support/consistency.py
src/cnsv/support/attention_items.py
src/cnsv/support/review_checklist.py
src/cnsv/support/support_evaluator.py
src/cnsv/support/support_report.py
src/cnsv/support/support_registry.py
```

新增 CLI：

```text
src/cnsv/cli/run_human_decision_support.py
```

新增测试：

```text
tests/test_evidence_loader.py
tests/test_evidence_fusion.py
tests/test_support_levels.py
tests/test_consistency.py
tests/test_attention_items.py
tests/test_review_checklist.py
tests/test_support_evaluator.py
tests/test_support_report.py
tests/test_support_registry.py
tests/test_human_decision_support_cli.py
```

新增 workflow：

```text
.github/workflows/run_human_decision_support.yml
```

---

## 14. CLI 命令要求

新增命令：

```bash
python -m cnsv.cli.run_human_decision_support
```

该命令必须：

1. 读取 CNSVdata gate；
2. 读取 V1.0–V1.4 已有报告；
3. 检查上游证据可用性；
4. 构造 evidence_availability；
5. 构造 current_state_summary；
6. 构造 model_evidence_summary；
7. 构造 path_opportunity_observation；
8. 构造 path_risk_observation；
9. 构造 model_consistency_summary；
10. 构造 evidence_conflict_summary；
11. 构造 human_attention_items；
12. 构造 human_review_checklist；
13. 执行 human_decision_support_quality；
14. 生成 JSON；
15. 生成 registry；
16. 生成 MD；
17. 生成 HTML；
18. 更新 docs/index.html；
19. 写入 archive。

---

## 15. GitHub Actions 要求

新增：

```text
.github/workflows/run_human_decision_support.yml
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
```

提交产物：

```text
docs/data/latest_human_decision_support_report.json
docs/data/human_decision_support_registry.json
reports/latest_human_decision_support_report.md
reports/archive/*_human_decision_support_report.md
docs/decision_support.html
docs/index.html
```

不要破坏现有 workflow：

```text
check_data.yml
run_features.yml
run_baseline_models.yml
run_baseline_validation.yml
run_path_distribution.yml
run_observation_backtest.yml
```

---

## 16. 测试要求

必须新增并跑通测试。

### 16.1 证据读取测试

构造 mock V1.0–V1.4 报告。

断言：

```text
evidence_availability 正确
缺失报告能被记录
缺失报告不会被伪造
```

### 16.2 证据融合测试

构造路径机会、路径风险、回测证据。

断言：

```text
evidence_strength 正确
evidence_conflict 正确
human_review_required 正确
```

### 16.3 模型一致性测试

构造一致、分歧、证据不足三种场景。

断言：

```text
model_consistency_level 正确
model_disagreement_points 正确
```

### 16.4 人工关注点测试

构造风险偏高、数据缺失、P2 fallback 高等场景。

断言：

```text
human_attention_items 非空
每条都是观察事项
不包含交易动作
```

### 16.5 人工复核清单测试

断言至少包含：

```text
data_freshness
path_risk
model_conflict
evidence_quality
```

### 16.6 禁止交易字段测试

如果报告出现：

```text
buy_signal
sell_signal
target_position
stop_loss
take_profit
target_price
formal_signal
```

必须 FAIL。

### 16.7 CLI 测试

执行：

```bash
python -m cnsv.cli.run_human_decision_support
```

断言生成：

```text
docs/data/latest_human_decision_support_report.json
docs/data/human_decision_support_registry.json
reports/latest_human_decision_support_report.md
docs/decision_support.html
docs/index.html
```

---

## 17. 自检命令

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
```

不允许只改代码不跑测试。

---

## 18. 最终输出要求

完成后请给我简洁说明，必须包含：

1. 修改了哪些文件；
2. 是否新增 V1.5 人工决策辅助层；
3. 是否仍然严格禁止交易信号；
4. 是否生成 human decision support JSON；
5. 是否生成 human decision support MD；
6. 是否生成 decision_support.html；
7. 是否更新 index.html；
8. 是否读取 V1.0–V1.4 上游证据；
9. evidence_availability 结果；
10. evidence_strength 结果；
11. model_consistency_level 结果；
12. risk_attention_level 结果；
13. human_attention_items 是否生成；
14. human_review_checklist 是否生成；
15. 是否存在 evidence_conflict；
16. 是否仍然把 P2 作为辅助；
17. pytest 结果；
18. run_human_decision_support 结果；
19. 最新报告路径；
20. 是否可以进入 V1.6。

---

## 19. V1.5 验收标准

V1.5 通过条件：

1. `pytest` 通过；
2. `run_human_decision_support` 通过；
3. `latest_human_decision_support_report.json` 正常生成；
4. `human_decision_support_quality.status` 不得为 FAIL；
5. 上游证据读取完整或缺失时已降级；
6. evidence_availability 存在；
7. current_state_summary 存在；
8. model_evidence_summary 存在；
9. path_opportunity_observation 存在；
10. path_risk_observation 存在；
11. model_consistency_summary 存在；
12. evidence_conflict_summary 存在；
13. human_attention_items 存在；
14. human_review_checklist 存在；
15. support_levels 存在；
16. 无 NaN/inf；
17. 无交易信号字段；
18. `is_trade_signal = false`；
19. `forbidden_actions` 包含 `formal_signal_generation`、`auto_order`、`broker_api`；
20. `docs/decision_support.html` 存在；
21. `docs/index.html` 有 decision support 入口；
22. README 或开发文档说明 V1.5；
23. `next_stage = V1.6 risk explanation`。

---

## 20. V1.5 与 V1.6 的边界

V1.5 只负责人工决策辅助。

V1.6 才允许开发：

```text
风控解释层
亏损路径解释
回撤风险解释
模型分歧风险解释
数据质量风险解释
市场环境风险解释
风险来源拆解
```

V1.6 仍然不能自动交易，不能连接券商，不能输出正式下单动作。

---

## 21. 核心原则

V1.4 解决的是：

```text
这些路径判断在历史上有没有参考价值。
```

V1.5 要解决的是：

```text
如何把数据、模型、路径、回测证据整理成人工能看懂、能复核、能谨慎使用的辅助信息。
```

V1.5 最重要的专业判断：

```text
人工决策辅助不是交易信号。
观察优先级不是买入建议。
风险关注等级不是止损指令。
证据强弱不是仓位建议。
模型一致性不是自动决策。
V1.5 的任务是帮助人工理解，不是替人工交易。
```

只有 V1.5 通过后，才允许进入 V1.6 risk explanation。
