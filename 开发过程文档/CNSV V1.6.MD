# CNSV V1.6.MD — 风控解释层开发文档

> 交付对象：Codex  
> 适用仓库：`https://github.com/njedu2023-prog/CNSV`  
> 当前正式阶段：`CNSV V1.6_risk_explanation`  
> 核心任务：在 V1.5 人工决策辅助层之后，开发风控解释层，把数据风险、特征风险、模型风险、路径风险、回撤风险、证据冲突风险、P2 状态不稳定风险解释清楚，形成可复核的风险画像。  
> 最高边界：V1.6 仍然不是实盘交易系统，不输出买卖指令，不输出仓位，不输出止盈止损，不连接券商，不自动下单。

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
"version": "1.6"
```

本轮 stage 统一使用：

```json
"stage": "V1.6_risk_explanation"
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
6. V1.5 人工决策辅助层；
7. V1.5 已生成：
   - `latest_human_decision_support_report.json`
   - `human_decision_support_registry.json`
   - `latest_human_decision_support_report.md`
   - `docs/decision_support.html`

V1.5 的重要状态：

```text
V1.5 功能可以验收，但 human_decision_support_quality 可能是 WARN。
WARN 可接受的原因通常是 human_review_required = true 或 evidence_conflict = true。
这些 WARN 不是阻断错误，而是 V1.6 风控解释层必须重点解释的输入。
```

本轮任务：

```text
CNSV V1.6 —— Risk Explanation Layer / 风控解释层
```

V1.6 要回答的问题：

```text
当前 CNSV 系统看到的主要风险是什么？
这些风险来自数据、特征、模型、路径、回测证据、状态样本，还是证据冲突？
风险为什么出现？
风险是否可复核？
人工下一步需要重点确认哪些风险？
```

V1.6 不是交易指令层。  
V1.6 的产出是风险解释和风险复核清单，不是买卖建议。

---

## 2. V1.6 核心定位

V1.6 是风控解释层，不是正式交易信号层。

V1.6 可以输出：

```text
风险来源
风险等级
风险证据
风险解释
风险触发条件
风险冲突点
风险复核清单
下行路径风险
最大回撤风险
模型分歧风险
数据质量风险
状态样本不稳定风险
证据不足风险
是否允许进入 V2.0
```

V1.6 不可以输出：

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
V1.6 只解释风险，不发出交易命令。
```

---

## 3. V1.6 严禁事项

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
20. 不把 risk explanation report 命名成 signal；
21. 不把风险等级包装成交易动作；
22. 不把回撤解释包装成止损指令；
23. 不把路径上行解释包装成买入理由；
24. 不把历史风险表现包装成未来承诺；
25. 不因为风险低就输出操作动作；
26. 不因为风险高就输出操作动作。

允许输出：

```text
风险观察
风险解释
风险等级
风险证据
风险来源
风险复核项
风险冲突点
风险注意事项
人工需要确认什么
是否存在证据不足
是否允许进入 V2.0 前置准备
```

---

## 4. V1.6 与 V1.5 的关系

V1.5 负责回答：

```text
如何把数据、模型、路径、回测证据整理成人工能看懂、能复核、能谨慎使用的辅助信息？
```

V1.6 负责回答：

```text
这些辅助信息背后有哪些风险？
哪些风险最主要？
哪些风险来自模型分歧？
哪些风险来自路径下穿或回撤？
哪些风险来自数据质量或样本不足？
哪些风险需要人工重点复核？
```

V1.6 必须复用 V1.5 的人工决策辅助报告，不允许跳过 V1.5 直接生成风险解释。

如果 V1.5 报告不存在、质量 FAIL、或关键证据缺失，V1.6 必须降级，并在报告中写明：

```text
human_decision_support_evidence_unavailable
human_decision_support_quality_failed
insufficient_support_evidence
```

---

## 5. V1.6 输入证据

V1.6 必须从已有产物读取，不重新发明证据。

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
```

核心输入证据包括：

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
current_state
baseline_models
path_models
model_backtest_metrics
observation_condition_quality
model_comparison
support_levels
evidence_availability
evidence_conflict_summary
human_attention_items
human_review_checklist
forbidden_actions
```

如果某个上游报告缺失：

1. 不允许伪造；
2. 不允许用 fake 值填充；
3. 必须降级；
4. 必须在 `risk_evidence_availability` 中写明缺失项；
5. 不得输出高置信风险解释结论。

---

## 6. V1.6 核心输出模块

### 6.1 风险总览

输出：

```text
overall_risk_level
risk_confidence
primary_risk_sources
secondary_risk_sources
human_review_required
```

建议取值：

```text
overall_risk_level: low / medium / high / severe
risk_confidence: low / medium / high / insufficient
human_review_required: true / false
```

`overall_risk_level` 只是风险观察等级，不是交易动作。

### 6.2 数据风险解释

解释：

```text
data_freshness_risk
data_gate_risk
missing_data_risk
quality_check_risk
manifest_consistency_risk
```

输入来源：

```text
latest_data_report.json
latest_feature_report.json
cnsvdata_gate
data_manifest
```

### 6.3 特征风险解释

解释：

```text
trend_state_risk
volatility_state_risk
flow_strength_basic_risk
moneyflow_reliability_risk
feature_unknown_risk
feature_conflict_risk
```

输入来源：

```text
feature_quality
current_state
trend_state
volatility_state
flow_strength_basic
```

### 6.4 基准模型风险解释

解释：

```text
baseline_distribution_risk
B1_B3_conflict_risk
B2_state_sample_risk
positive_prob_calibration_risk
quantile_coverage_risk
```

输入来源：

```text
latest_baseline_model_report.json
latest_baseline_validation_report.json
```

### 6.5 路径风险解释

解释：

```text
downside_path_risk
touch_down_risk
max_drawdown_risk
path_volatility_risk
terminal_distribution_risk
```

输入来源：

```text
latest_path_distribution_report.json
latest_path_validation_report.json
```

### 6.6 观察级回测风险解释

解释：

```text
observation_backtest_evidence_risk
bucket_stability_risk
purged_sample_risk
condition_effectiveness_risk
P1_vs_P0_risk
P2_vs_P1_risk
```

输入来源：

```text
latest_observation_backtest_report.json
```

### 6.7 人工辅助证据风险解释

解释：

```text
evidence_strength_risk
model_consistency_risk
evidence_conflict_risk
human_review_required_risk
attention_item_risk
```

输入来源：

```text
latest_human_decision_support_report.json
```

### 6.8 P2 辅助层风险解释

P2 风险必须单独解释，因为历史阶段已经多次显示：

```text
P2 fallback_rate 偏高
P2 状态样本空间容易碎片化
P2 不能作为核心依赖
```

输出：

```text
p2_auxiliary_risk_level
p2_fallback_risk
p2_state_sample_risk
p2_state_space_fragmentation_risk
p2_core_dependency_forbidden = true
```

### 6.9 风险复核清单

输出：

```text
risk_review_checklist
```

至少包含：

```text
check_data_freshness
check_feature_unknown
check_model_conflict
check_path_downside
check_drawdown_exposure
check_touch_down_risk
check_p2_fallback
check_purged_sample_size
check_evidence_conflict
check_human_review_required
```

每一项都必须是人工复核事项，不是交易指令。

---

## 7. 风险等级规则

V1.6 可以输出风险等级，但不能输出交易动作。

允许等级：

```text
risk_level
risk_confidence
risk_attention_level
risk_source_weight
risk_evidence_strength
```

建议取值：

```text
risk_level: low / medium / high / severe
risk_confidence: low / medium / high / insufficient
risk_attention_level: low / medium / high / urgent_review
risk_evidence_strength: weak / moderate / strong / insufficient
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

## 8. 风险来源分类

V1.6 必须把风险拆成来源，不允许只输出一个总风险。

至少包含：

```text
data_risk
feature_risk
baseline_model_risk
path_distribution_risk
path_validation_risk
observation_backtest_risk
decision_support_risk
p2_auxiliary_risk
evidence_conflict_risk
system_boundary_risk
```

每类风险至少包含：

```text
risk_level
risk_reason
risk_evidence
source_reports
human_review_required
```

示例结构：

```json
{
  "risk_type": "path_distribution_risk",
  "risk_level": "high",
  "risk_reason": "touch_down_5pct_prob and max_drawdown_p90 are elevated",
  "risk_evidence": ["latest_path_distribution_report.json", "latest_path_validation_report.json"],
  "human_review_required": true
}
```

---

## 9. 风险解释规则

风险解释必须满足：

1. 只基于系统已有证据；
2. 不编造外部消息；
3. 不调用 Tushare；
4. 不调用券商；
5. 不输出未来承诺；
6. 不把概率说成确定结果；
7. 不把风险等级变成交易动作；
8. 不把历史表现当成未来保证；
9. 证据不足时必须明确写 `insufficient_evidence`；
10. 模型冲突时必须明确写 `evidence_conflict = true`。

---

## 10. 风险情景卡片

V1.6 建议新增 risk scenario cards。

每张卡片包含：

```text
scenario_id
scenario_name
risk_level
trigger_evidence
risk_explanation
historical_support
human_review_items
not_trade_signal_statement
```

建议至少生成以下卡片：

```text
downside_touch_risk_card
max_drawdown_risk_card
model_conflict_risk_card
p2_instability_risk_card
data_quality_risk_card
evidence_insufficiency_risk_card
```

禁止生成：

```text
buy_card
sell_card
stop_loss_card
take_profit_card
position_card
```

---

## 11. V1.6 质量门禁

新增：

```text
risk_explanation_quality
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

### 11.1 必须 FAIL 的情况

1. 出现交易信号字段；
2. 出现 buy/sell/position/stop_loss/take_profit/target_price 等字段；
3. 出现 NaN/inf；
4. `is_trade_signal` 不是 false；
5. 缺少 `forbidden_actions`；
6. `forbidden_actions` 缺少 `formal_signal_generation`、`auto_order`、`broker_api`；
7. 上游 V1.5 human decision support 报告缺失；
8. 上游关键质量门禁 FAIL 但 V1.6 未降级；
9. 把 P2 当作核心依赖；
10. 输出任何直接交易动作；
11. 报告命名成 signal；
12. 连接券商接口；
13. 自动下单相关代码或字段出现；
14. 伪造缺失证据；
15. 版本字段不是 `"1.6"`；
16. 风险等级字段被命名为 buy/sell/position/stop_loss/take_profit；
17. 风险解释中出现操作建议。

### 11.2 可以 WARN 的情况

1. 某个上游报告缺失但已降级；
2. P2 fallback_rate 偏高；
3. evidence_conflict = true；
4. human_review_required = true；
5. risk_confidence = insufficient；
6. purged 样本数偏少；
7. 状态字段存在 unknown；
8. 数据 freshness 不足；
9. 风险等级为 high 或 severe；
10. 风险证据来自多个互相冲突的模型。

---

## 12. 报告结构要求

新增 JSON：

```text
docs/data/latest_risk_explanation_report.json
```

建议结构：

```json
{
  "meta": {
    "system": "CNSV",
    "version": "1.6",
    "stage": "V1.6_risk_explanation",
    "report_type": "risk_explanation_report",
    "ts_code": "600150.SH",
    "name": "中国船舶",
    "generated_at": "...",
    "latest_trade_date": "...",
    "is_trade_signal": false
  },
  "cnsvdata_gate": {},
  "risk_evidence_availability": {},
  "risk_explanation_quality": {},
  "overall_risk_summary": {},
  "risk_source_breakdown": {},
  "data_risk_explanation": {},
  "feature_risk_explanation": {},
  "baseline_model_risk_explanation": {},
  "path_distribution_risk_explanation": {},
  "observation_backtest_risk_explanation": {},
  "decision_support_risk_explanation": {},
  "p2_auxiliary_risk_explanation": {},
  "evidence_conflict_risk_explanation": {},
  "risk_scenario_cards": [],
  "risk_review_checklist": [],
  "forbidden_actions": [
    "formal_signal_generation",
    "auto_order",
    "broker_api"
  ],
  "next_stage": "V2.0 live manual decision system"
}
```

新增 registry：

```text
docs/data/risk_explanation_registry.json
```

新增 MD 报告：

```text
reports/latest_risk_explanation_report.md
reports/archive/YYYY-MM-DD_risk_explanation_report.md
```

新增 HTML 页面：

```text
docs/risk.html
```

并更新：

```text
docs/index.html
```

增加入口：

```text
Risk Explanation Report
```

---

## 13. Markdown 报告要求

`reports/latest_risk_explanation_report.md` 必须用中文说明：

1. 当前阶段是 V1.6；
2. 这是风控解释，不是交易信号；
3. 使用了哪些上游证据；
4. 哪些上游证据可用；
5. 哪些上游证据缺失或降级；
6. 总体风险等级；
7. 主要风险来源；
8. 次要风险来源；
9. 数据风险解释；
10. 特征风险解释；
11. 基准模型风险解释；
12. 路径风险解释；
13. 观察级回测风险解释；
14. 人工辅助证据风险解释；
15. P2 辅助层风险解释；
16. 证据冲突风险解释；
17. 风险情景卡片；
18. 风险复核清单；
19. 是否允许进入 V2.0；
20. 明确声明：这不是买卖建议，不构成交易指令。

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

## 14. HTML 页面要求

新增：

```text
docs/risk.html
```

页面至少展示：

```text
V1.6 阶段说明
risk_explanation_quality
risk_evidence_availability
overall_risk_summary
risk_source_breakdown
data_risk_explanation
feature_risk_explanation
baseline_model_risk_explanation
path_distribution_risk_explanation
observation_backtest_risk_explanation
decision_support_risk_explanation
p2_auxiliary_risk_explanation
evidence_conflict_risk_explanation
risk_scenario_cards
risk_review_checklist
禁止交易信号声明
```

更新：

```text
docs/index.html
```

新增入口：

```text
Risk Explanation Report
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

## 15. 建议新增文件结构

请根据仓库实际结构实现，可微调路径，但职责要清晰。

```text
src/cnsv/risk/__init__.py
src/cnsv/risk/risk_evidence_loader.py
src/cnsv/risk/risk_scoring.py
src/cnsv/risk/risk_source_breakdown.py
src/cnsv/risk/risk_scenarios.py
src/cnsv/risk/risk_checklist.py
src/cnsv/risk/risk_evaluator.py
src/cnsv/risk/risk_report.py
src/cnsv/risk/risk_registry.py
```

新增 CLI：

```text
src/cnsv/cli/run_risk_explanation.py
```

新增测试：

```text
tests/test_risk_evidence_loader.py
tests/test_risk_scoring.py
tests/test_risk_source_breakdown.py
tests/test_risk_scenarios.py
tests/test_risk_checklist.py
tests/test_risk_evaluator.py
tests/test_risk_report.py
tests/test_risk_registry.py
tests/test_risk_explanation_cli.py
```

新增 workflow：

```text
.github/workflows/run_risk_explanation.yml
```

---

## 16. CLI 命令要求

新增命令：

```bash
python -m cnsv.cli.run_risk_explanation
```

该命令必须：

1. 读取 CNSVdata gate；
2. 读取 V1.0–V1.5 已有报告；
3. 检查上游证据可用性；
4. 构造 risk_evidence_availability；
5. 构造 overall_risk_summary；
6. 构造 risk_source_breakdown；
7. 构造各类 risk_explanation；
8. 构造 risk_scenario_cards；
9. 构造 risk_review_checklist；
10. 执行 risk_explanation_quality；
11. 生成 JSON；
12. 生成 registry；
13. 生成 MD；
14. 生成 HTML；
15. 更新 docs/index.html；
16. 写入 archive。

---

## 17. GitHub Actions 要求

新增：

```text
.github/workflows/run_risk_explanation.yml
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
```

提交产物：

```text
docs/data/latest_risk_explanation_report.json
docs/data/risk_explanation_registry.json
reports/latest_risk_explanation_report.md
reports/archive/*_risk_explanation_report.md
docs/risk.html
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
run_human_decision_support.yml
```

---

## 18. 测试要求

必须新增并跑通测试。

### 18.1 风险证据读取测试

构造 mock V1.0–V1.5 报告。

断言：

```text
risk_evidence_availability 正确
缺失报告能被记录
缺失报告不会被伪造
```

### 18.2 风险评分测试

构造低、中、高、严重风险场景。

断言：

```text
overall_risk_level 正确
risk_confidence 正确
human_review_required 正确
```

### 18.3 风险来源拆解测试

构造数据风险、路径风险、模型冲突风险、P2 fallback 风险。

断言：

```text
risk_source_breakdown 包含对应风险
risk_reason 非空
source_reports 非空
```

### 18.4 P2 辅助层风险测试

构造 P2 fallback_rate 偏高场景。

断言：

```text
p2_auxiliary_risk_level 不为空
p2_core_dependency_forbidden = true
P2 不被作为核心依赖
```

### 18.5 风险情景卡片测试

断言至少包含：

```text
downside_touch_risk_card
max_drawdown_risk_card
model_conflict_risk_card
p2_instability_risk_card
```

且不包含：

```text
buy_card
sell_card
stop_loss_card
take_profit_card
position_card
```

### 18.6 禁止交易字段测试

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

### 18.7 CLI 测试

执行：

```bash
python -m cnsv.cli.run_risk_explanation
```

断言生成：

```text
docs/data/latest_risk_explanation_report.json
docs/data/risk_explanation_registry.json
reports/latest_risk_explanation_report.md
docs/risk.html
docs/index.html
```

---

## 19. 自检命令

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
```

不允许只改代码不跑测试。

---

## 20. 最终输出要求

完成后请给我简洁说明，必须包含：

1. 修改了哪些文件；
2. 是否新增 V1.6 风控解释层；
3. 是否仍然严格禁止交易信号；
4. 是否生成 risk explanation JSON；
5. 是否生成 risk explanation MD；
6. 是否生成 risk.html；
7. 是否更新 index.html；
8. 是否读取 V1.0–V1.5 上游证据；
9. risk_evidence_availability 结果；
10. overall_risk_level 结果；
11. primary_risk_sources 结果；
12. p2_auxiliary_risk_level 结果；
13. evidence_conflict_risk 结果；
14. risk_scenario_cards 是否生成；
15. risk_review_checklist 是否生成；
16. 是否仍然把 P2 作为辅助；
17. pytest 结果；
18. run_risk_explanation 结果；
19. 最新报告路径；
20. 是否可以进入 V2.0。

---

## 21. V1.6 验收标准

V1.6 通过条件：

1. `pytest` 通过；
2. `run_risk_explanation` 通过；
3. `latest_risk_explanation_report.json` 正常生成；
4. `risk_explanation_quality.status` 不得为 FAIL；
5. 上游证据读取完整或缺失时已降级；
6. risk_evidence_availability 存在；
7. overall_risk_summary 存在；
8. risk_source_breakdown 存在；
9. data_risk_explanation 存在；
10. feature_risk_explanation 存在；
11. baseline_model_risk_explanation 存在；
12. path_distribution_risk_explanation 存在；
13. observation_backtest_risk_explanation 存在；
14. decision_support_risk_explanation 存在；
15. p2_auxiliary_risk_explanation 存在；
16. evidence_conflict_risk_explanation 存在；
17. risk_scenario_cards 存在；
18. risk_review_checklist 存在；
19. 无 NaN/inf；
20. 无交易信号字段；
21. `is_trade_signal = false`；
22. `forbidden_actions` 包含 `formal_signal_generation`、`auto_order`、`broker_api`；
23. `docs/risk.html` 存在；
24. `docs/index.html` 有 risk report 入口；
25. README 或开发文档说明 V1.6；
26. `next_stage = V2.0 live manual decision system`。

---

## 22. V1.6 与 V2.0 的边界

V1.6 只负责风控解释。

V2.0 才允许进入：

```text
实盘人工决策系统
人工驾驶舱
人工操作前证据整合
人工确认流程
人工日志
人工复盘
```

但 V2.0 仍然建议保持：

```text
人工决策
人工下单
系统辅助
系统不自动交易
系统不连接券商下单
```

除非未来单独立项并重新验收交易合规、券商接口、安全权限和风控边界。

---

## 23. 核心原则

V1.5 解决的是：

```text
如何把证据整理成人工能看懂、能复核、能谨慎使用的辅助信息。
```

V1.6 要解决的是：

```text
这些证据背后的风险来自哪里，为什么有风险，人工需要复核什么。
```

V1.6 最重要的专业判断：

```text
风控解释不是交易信号。
风险等级不是卖出建议。
低风险不是买入建议。
回撤解释不是止损指令。
模型冲突不是交易动作。
P2 仍然只是辅助观察层。
V1.6 的任务是解释风险，不是替人工交易。
```

只有 V1.6 通过后，才允许进入 V2.0 live manual decision system。
