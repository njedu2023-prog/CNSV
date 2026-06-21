# CNSV V3.0 交易决策系统开发文档  
## BUY / HOLD / SELL + EV + 风控 + 仓位  
版本：V3.0  
项目：CNSV 主程序仓库  
标的：600150.SH 中国船舶  
定位：人工执行量化交易决策系统  

---

# 0. V3.0 一句话定义

CNSV V3.0 不是单纯预测系统，而是面向真实人工买卖操作的交易决策系统。

它的目标不是告诉用户“模型怎么看”，而是清楚回答：

- 明天涨的概率有多大？
- 明天可能涨多少、跌多少？
- 当前应该买、持有、卖出，还是继续观察？
- 如果买，建议买多少仓位？
- 如果错了，最大风险在哪里？
- 什么情况下必须降级、禁止买入或强制提示卖出？

V3.0 必须从“观察级系统”正式升级为“人工交易决策系统”。

---

# 1. V3.0 的系统边界

## 1.1 V3.0 必须做

V3.0 必须输出以下结果：

1. 次日上涨概率  
2. 次日下跌概率  
3. 次日涨跌幅分布  
4. 预期收益 EV  
5. 风险收益比  
6. BUY / HOLD / SELL / WATCH 信号  
7. 建议仓位  
8. 止盈参考  
9. 止损参考  
10. 风控拦截原因  
11. 人工决策解释  
12. 中文 HTML 看板  

---

## 1.2 V3.0 仍然不做

为了保证安全，V3.0 仍然不允许：

- 不自动下单
- 不连接券商接口
- 不替用户直接执行交易
- 不绕过 CNSVdata
- 不直接拉取 Tushare
- 不输出“保证盈利”
- 不使用无法解释的黑箱信号
- 不在风控失败时输出 BUY
- 不在数据质量失败时输出正式交易信号

---

# 2. 数据链路承前关系

V3.0 必须承接前面版本成果，不允许推倒重来。

## 2.1 上游数据来源

默认继续从 CNSVdata 读取数据：

```text
https://raw.githubusercontent.com/njedu2023-prog/CNSVdata/refs/heads/main
```

第一读取入口必须仍然是：

```text
metadata/downstream_ready.json
```

Gate 规则继续有效：

| 条件 | V3.0 行为 |
|---|---|
| ready=false | 阻断，不生成交易信号 |
| status=FAIL | 阻断，不生成交易信号 |
| status=WARN | 只允许观察级输出，不允许 BUY / SELL |
| status=PASS | 允许进入 V3.0 决策流程 |
| can_generate_formal_signal=false | 只允许人工辅助，不允许自动交易 |

---

## 2.2 承接 V1.0 数据层

V1.0 已完成：

- 数据读取
- 数据状态检查
- 基础 OHLCV
- 分钟结构摘要
- 资金流摘要
- latest_data_report

V3.0 必须复用：

```text
docs/data/latest_data_report.json
reports/latest_data_report.md
```

---

## 2.3 承接 V1.1 特征层

V1.1 已完成：

- 量价特征
- 分钟结构特征
- 资金流特征
- 趋势特征
- 波动率特征
- Feature Quality
- Feature Registry

V3.0 必须复用：

```text
docs/data/latest_feature_report.json
docs/data/feature_registry.json
reports/latest_feature_report.md
```

---

## 2.4 承接 V1.2 基准模型层

V1.2 已完成：

- B0 random walk
- B1 historical distribution
- B2 state grouped distribution
- B3 volatility adjusted
- baseline validation
- walk-forward 验证

V3.0 必须复用：

```text
docs/data/latest_baseline_model_report.json
docs/data/latest_baseline_validation_report.json
docs/data/baseline_registry.json
```

V3.0 不允许直接抛弃 B0-B3，而是要把它们作为概率分布和风险判断的基础来源。

---

## 2.5 承接 V1.3 路径分布层

V1.3 已完成：

- 5D / 10D / 20D 路径分布
- 历史路径回放
- 波动率调整路径
- 状态条件路径
- 路径验证
- purged walk-forward

V3.0 必须复用：

```text
docs/data/latest_path_distribution_report.json
docs/data/latest_path_validation_report.json
docs/data/path_distribution_registry.json
reports/latest_path_distribution_report.md
reports/latest_path_validation_report.md
```

V3.0 的止盈、止损、仓位、风险收益比，必须优先参考路径分布结果。

---

## 2.6 承接 V2.0 人工决策辅助层

V2.0 已经进入人工决策解释系统。

V3.0 在 V2.0 基础上新增：

- 正式信号定义
- EV 计算
- 买卖建议
- 仓位建议
- 风控约束
- 中文决策看板
- 人工执行说明

---

# 3. V3.0 核心模块

V3.0 新增 6 个核心模块：

```text
D0_data_gate
D1_next_day_probability_engine
D2_return_distribution_engine
D3_ev_engine
D4_signal_engine
D5_risk_control_engine
D6_position_engine
D7_exit_engine
D8_human_decision_report
```

---

# 4. D1 次日涨跌概率引擎

## 4.1 目标

输出次日上涨概率、下跌概率、平盘概率和方向置信度。

示例：

| 指标 | 输出 |
|---|---|
| 次日上涨概率 | 64.2% |
| 次日下跌概率 | 31.5% |
| 次日平盘概率 | 4.3% |
| 方向置信度 | 0.71 |

---

## 4.2 输入数据

输入包括：

- 最新日线数据
- 最新分钟结构
- 最新资金流
- 趋势状态
- 波动状态
- B1 历史分布
- B2 状态分组分布
- B3 波动率调整分布
- V1.3 路径分布
- V1.4 / V1.5 / V2.0 已有验证结果

---

## 4.3 概率输出字段

必须输出：

```json
{
  "prob_up_1d": 0.642,
  "prob_down_1d": 0.315,
  "prob_flat_1d": 0.043,
  "direction_confidence": 0.71,
  "primary_model": "B3_volatility_adjusted",
  "fallback_used": false,
  "fallback_reason": null
}
```

---

# 5. D2 次日涨跌幅分布引擎

## 5.1 目标

不只判断涨跌，还要输出涨跌幅区间概率。

示例：

| 次日收益区间 | 概率 |
|---|---|
| 大涨 > +5% | 12% |
| 中涨 +2% ~ +5% | 24% |
| 小涨 0% ~ +2% | 28% |
| 小跌 0% ~ -2% | 20% |
| 中跌 -2% ~ -5% | 11% |
| 大跌 < -5% | 5% |

---

## 5.2 必须输出字段

```json
{
  "return_bins_1d": {
    "gt_5pct": 0.12,
    "plus_2_to_5pct": 0.24,
    "zero_to_plus_2pct": 0.28,
    "zero_to_minus_2pct": 0.20,
    "minus_2_to_5pct": 0.11,
    "lt_minus_5pct": 0.05
  },
  "expected_return_1d": 0.018,
  "median_return_1d": 0.011,
  "p10_return_1d": -0.031,
  "p90_return_1d": 0.056
}
```

---

# 6. D3 EV 期望收益引擎

## 6.1 EV 定义

EV 是 V3.0 的核心。

EV 不是单次收益预测，而是长期重复执行同类交易时的期望收益。

计算逻辑：

```text
EV = Σ(收益区间中值 × 对应概率) - 交易成本 - 风险惩罚
```

---

## 6.2 EV 输出

示例：

| 项目 | 数值 |
|---|---|
| 原始 EV | +2.14% |
| 成本调整 EV | +1.92% |
| 风险调整 EV | +1.36% |
| EV 评级 | 正期望 |

---

## 6.3 EV 分级

| EV 区间 | 评级 | 含义 |
|---|---|---|
| EV ≥ +2.0% | 强正期望 | 可进入 BUY 判断 |
| +1.0% ≤ EV < +2.0% | 正期望 | 可谨慎 BUY |
| -0.5% ≤ EV < +1.0% | 中性 | HOLD / WATCH |
| EV < -0.5% | 负期望 | 禁止买入 |
| EV < -1.5% | 明显负期望 | SELL 倾向 |

---

# 7. D4 信号引擎

## 7.1 信号类型

V3.0 只允许输出以下信号：

```text
STRONG_BUY
BUY
HOLD
WATCH
REDUCE
SELL
STRONG_SELL
BLOCKED
```

---

## 7.2 STRONG_BUY 定义

必须同时满足：

- 次日上涨概率 ≥ 70%
- 风险调整 EV ≥ +2.0%
- 方向置信度 ≥ 0.75
- 大跌概率 < 8%
- 数据状态 PASS
- 风控未拦截
- 路径分布支持上行
- 近端资金流不恶化

输出：

```text
STRONG_BUY
```

---

## 7.3 BUY 定义

必须同时满足：

- 次日上涨概率 ≥ 60%
- 风险调整 EV ≥ +1.0%
- 方向置信度 ≥ 0.65
- 大跌概率 < 12%
- 数据状态 PASS
- 风控未拦截

输出：

```text
BUY
```

---

## 7.4 HOLD 定义

适用于已经持仓时：

满足以下任一情况：

- 上涨概率 45% ~ 60%
- EV 接近 0
- 未触发卖出
- 趋势未明显破坏
- 路径仍未失效

输出：

```text
HOLD
```

---

## 7.5 WATCH 定义

适用于未持仓时：

- 信号不够强
- EV 不够高
- 模型置信度不足
- 数据质量存在 WARN
- 资金流分歧明显

输出：

```text
WATCH
```

WATCH 的含义是：

```text
可以观察，但不建议主动买入。
```

---

## 7.6 REDUCE 定义

适用于已经持仓时：

- 下跌概率上升
- EV 转弱
- 上行空间不足
- 风险收益比恶化
- 但尚未达到强制卖出

输出：

```text
REDUCE
```

含义：

```text
建议降低仓位，不建议继续满仓持有。
```

---

## 7.7 SELL 定义

满足以下任一条件：

- 次日下跌概率 ≥ 60%
- 风险调整 EV < -0.5%
- 大跌概率 ≥ 15%
- 路径验证失效
- 趋势状态恶化
- 资金流明显转弱
- 已触发止损规则

输出：

```text
SELL
```

---

## 7.8 STRONG_SELL 定义

满足以下任一条件：

- 次日下跌概率 ≥ 75%
- 大跌概率 ≥ 25%
- 风险调整 EV < -1.5%
- 趋势破坏
- 波动风险极高
- 风控强制退出

输出：

```text
STRONG_SELL
```

---

## 7.9 BLOCKED 定义

只要出现以下情况，必须输出：

```text
BLOCKED
```

触发条件：

- 数据状态 FAIL
- ready=false
- 关键字段缺失
- 样本不足且无法 fallback
- 模型验证未通过
- 风控硬约束失败
- can_generate_formal_signal=false 且系统配置禁止正式信号

BLOCKED 的中文解释：

```text
当前数据或模型条件不满足交易决策要求，不允许输出买卖建议。
```

---

# 8. D5 风控约束引擎

## 8.1 风控原则

V3.0 的核心不是多赚钱，而是避免一次大亏吃掉多次小赚。

风控优先级高于信号。

任何时候：

```text
风控 > EV > 概率 > 信号
```

---

## 8.2 硬风控规则

以下情况必须禁止 BUY：

| 风控项 | 阈值 | 行为 |
|---|---|---|
| 大跌概率 | ≥ 18% | 禁止 BUY |
| 预期 P10 跌幅 | ≤ -5% | 禁止 BUY |
| 数据状态 | WARN / FAIL | 禁止正式 BUY |
| 方向置信度 | < 0.55 | 禁止 BUY |
| EV | < 0 | 禁止 BUY |
| 流动性异常 | true | 禁止 BUY |
| 波动率异常 | true | 降级或禁止 BUY |
| 模型验证失败 | true | BLOCKED |

---

## 8.3 风险等级

V3.0 输出 5 档风险等级：

```text
LOW
MEDIUM_LOW
MEDIUM
MEDIUM_HIGH
HIGH
```

中文展示：

| 英文 | 中文 |
|---|---|
| LOW | 低风险 |
| MEDIUM_LOW | 中低风险 |
| MEDIUM | 中风险 |
| MEDIUM_HIGH | 中高风险 |
| HIGH | 高风险 |

---

## 8.4 风险解释必须人话化

错误示例：

```text
volatility_state=high, downside_tail=0.21
```

正确示例：

```text
近期波动明显放大，模型认为次日出现较大下跌的概率偏高，因此不建议主动买入。
```

---

# 9. D6 仓位建议引擎

## 9.1 仓位输出原则

V3.0 的仓位是人工参考仓位，不是自动下单仓位。

必须明确展示：

```text
建议仓位仅用于人工决策参考，不代表自动交易指令。
```

---

## 9.2 仓位分档

| 信号 | 建议仓位 |
|---|---|
| STRONG_BUY | 25% ~ 35% |
| BUY | 10% ~ 20% |
| HOLD | 维持原仓 |
| WATCH | 0% |
| REDUCE | 降至 10% ~ 20% |
| SELL | 降至 0% ~ 10% |
| STRONG_SELL | 0% |
| BLOCKED | 0% |

---

## 9.3 仓位计算因子

仓位必须由以下因素共同决定：

- EV
- 上涨概率
- 下跌概率
- 大跌概率
- 方向置信度
- 波动率
- 最大回撤
- 当前持仓状态
- 数据质量
- 风控状态

---

## 9.4 仓位输出字段

```json
{
  "position_action": "ADD",
  "suggested_position_pct": 0.15,
  "position_range": "10%~20%",
  "position_reason": "上涨概率和EV均为正，但大跌概率仍需控制，因此建议轻仓参与。"
}
```

---

# 10. D7 卖出与退出引擎

## 10.1 退出系统目标

V3.0 不只解决怎么买，还必须解决怎么卖。

退出引擎必须输出：

- 止盈参考
- 止损参考
- 时间退出
- 信号退出
- 风险退出

---

## 10.2 止盈参考

止盈不使用固定死规则，必须参考路径分布。

示例：

| 指标 | 数值 |
|---|---|
| 5D 上行 P80 | +6.8% |
| 10D 上行 P80 | +9.5% |
| 建议止盈区 | +6% ~ +9% |

---

## 10.3 止损参考

止损必须参考：

- 1D P10
- 5D P10
- 波动率
- 当前风险等级

示例：

| 风险等级 | 止损参考 |
|---|---|
| 低风险 | -4% |
| 中风险 | -3% |
| 高风险 | -2% 或禁止买入 |

---

## 10.4 时间退出

如果持仓超过设定周期，但 EV 不再为正，应提示退出。

示例：

```text
持仓已超过 10 个交易日，当前 EV 已转为负值，继续持有的性价比下降，建议降低仓位或退出。
```

---

# 11. V3.0 HTML 看板要求

## 11.1 看板定位

V3.0 HTML 不是工程报告，而是给人看的交易决策面板。

用户打开页面后，必须 3 秒内看懂：

```text
今天该不该买？
持仓该不该卖？
风险大不大？
仓位给多少？
```

---

## 11.2 中文优先

HTML 页面必须大量使用中文。

禁止主要界面全英文。

允许保留少量模型字段，但必须有中文解释。

---

## 11.3 风格参考

视觉风格参考 Apple 官网：

https://www.apple.com.cn/

要求：

- 简洁
- 留白多
- 卡片清晰
- 层级明确
- 中文标题大
- 关键结论突出
- 不堆满技术字段
- 不像后台日志
- 不像量化研究论文
- 像一个高级决策仪表盘

---

## 11.4 首页第一屏

第一屏必须包含：

```text
CNSV V3.0 交易决策系统
中国船舶 600150.SH
今日决策：BUY / HOLD / SELL
建议仓位：15%
次日上涨概率：64.2%
风险调整 EV：+1.36%
风险等级：中风险
```

---

## 11.5 核心决策卡片

必须有一张最大卡片：

```text
今日建议
BUY
轻仓参与
建议仓位：10%~20%
```

并配中文解释：

```text
模型认为次日上涨概率占优，风险调整后的期望收益为正，但下方尾部风险仍存在，因此建议轻仓参与，不建议重仓。
```

---

## 11.6 概率卡片

展示：

- 次日上涨概率
- 次日下跌概率
- 大涨概率
- 大跌概率

中文展示示例：

```text
明天上涨概率：64.2%
明天下跌概率：31.5%
大涨概率：12.0%
大跌概率：5.0%
```

---

## 11.7 EV 卡片

展示：

```text
风险调整 EV：+1.36%
交易性价比：正期望
```

解释：

```text
EV 为正，说明在当前类似条件下，长期重复执行具备正收益倾向。但单次交易仍可能亏损。
```

---

## 11.8 风控卡片

展示：

```text
当前风险：中风险
主要风险：波动放大、下方尾部风险未完全消除
风控状态：通过
```

如果风控拦截：

```text
风控状态：已拦截
原因：大跌概率过高，不允许输出 BUY。
```

---

## 11.9 仓位卡片

展示：

```text
建议仓位：10%~20%
不建议满仓
不建议加杠杆
```

解释：

```text
仓位建议根据上涨概率、EV、波动率和最大亏损风险共同生成。
```

---

## 11.10 卖出卡片

展示：

```text
止盈参考：+6% ~ +9%
止损参考：-3%
时间退出：10 个交易日后重新评估
```

---

# 12. HTML 文件输出路径

V3.0 必须生成：

```text
docs/trading.html
docs/data/latest_trading_decision_report.json
reports/latest_trading_decision_report.md
reports/archive/YYYY-MM-DD_trading_decision_report.md
```

可选新增：

```text
docs/data/trading_decision_registry.json
```

---

# 13. JSON 报告结构

必须输出：

```json
{
  "version": "CNSV_V3.0",
  "symbol": "600150.SH",
  "name": "中国船舶",
  "trade_date": "YYYY-MM-DD",
  "data_status": "PASS",
  "decision": {
    "signal": "BUY",
    "signal_cn": "建议买入",
    "suggested_action": "轻仓参与",
    "suggested_position_pct": 0.15,
    "position_range": "10%~20%"
  },
  "probability": {
    "prob_up_1d": 0.642,
    "prob_down_1d": 0.315,
    "prob_flat_1d": 0.043,
    "direction_confidence": 0.71
  },
  "return_distribution": {
    "expected_return_1d": 0.018,
    "median_return_1d": 0.011,
    "p10_return_1d": -0.031,
    "p90_return_1d": 0.056
  },
  "ev": {
    "raw_ev": 0.0214,
    "cost_adjusted_ev": 0.0192,
    "risk_adjusted_ev": 0.0136,
    "ev_rating": "positive"
  },
  "risk": {
    "risk_level": "MEDIUM",
    "risk_level_cn": "中风险",
    "risk_passed": true,
    "blocked": false,
    "block_reasons": []
  },
  "exit": {
    "take_profit_range": "+6%~+9%",
    "stop_loss_reference": "-3%",
    "time_exit_days": 10
  },
  "human_explanation": {
    "summary": "模型认为次日上涨概率占优，EV 为正，但尾部风险仍需控制，因此建议轻仓参与。",
    "risk_note": "单次交易仍可能亏损，禁止满仓和加杠杆。"
  }
}
```

---

# 14. Markdown 报告结构

`reports/latest_trading_decision_report.md` 必须包含：

1. 今日总决策  
2. 次日涨跌概率  
3. 次日涨跌幅分布  
4. EV 期望收益  
5. 风险等级  
6. 仓位建议  
7. 止盈止损参考  
8. 风控是否通过  
9. 模型来源  
10. 人工执行说明  

---

# 15. CLI 命令

新增命令：

```bash
python -m cnsv.cli.run_trading_decision
```

该命令必须执行：

```text
1. 检查 CNSVdata gate
2. 读取 V1.0 数据报告
3. 读取 V1.1 特征报告
4. 读取 V1.2 基准模型报告
5. 读取 V1.3 路径分布报告
6. 读取 V2.0 人工决策辅助报告
7. 生成 V3.0 交易决策 JSON
8. 生成 V3.0 Markdown 报告
9. 生成 docs/trading.html
```

---

# 16. GitHub Actions

新增：

```text
.github/workflows/run_trading_decision.yml
```

执行内容：

```bash
pip install -r requirements.txt
pytest
python -m cnsv.cli.run_baseline_models
python -m cnsv.cli.run_baseline_validation
python -m cnsv.cli.run_path_distribution
python -m cnsv.cli.run_path_validation
python -m cnsv.cli.run_trading_decision
```

然后自动提交：

```text
docs/trading.html
docs/data/latest_trading_decision_report.json
reports/latest_trading_decision_report.md
reports/archive/YYYY-MM-DD_trading_decision_report.md
```

---

# 17. 测试要求

必须新增测试：

```text
tests/test_trading_probability.py
tests/test_return_distribution.py
tests/test_ev_engine.py
tests/test_signal_engine.py
tests/test_risk_control_engine.py
tests/test_position_engine.py
tests/test_exit_engine.py
tests/test_trading_report.py
tests/test_trading_html.py
```

---

# 18. 验收标准

V3.0 完成后，必须满足：

## 18.1 工程验收

```bash
pytest
python -m cnsv.cli.run_trading_decision
```

必须通过。

---

## 18.2 数据验收

必须生成：

```text
docs/data/latest_trading_decision_report.json
reports/latest_trading_decision_report.md
docs/trading.html
```

---

## 18.3 决策验收

必须能清楚回答：

- 今天是否可以买？
- 如果可以买，买多少？
- 如果不能买，为什么？
- 如果已经持仓，是持有、减仓还是卖出？
- 明天涨跌概率是多少？
- 预期涨跌幅是多少？
- EV 是正还是负？
- 最大风险是什么？

---

## 18.4 风控验收

必须证明：

- 风控可以拦截 BUY
- 数据失败可以 BLOCKED
- EV 为负不能 BUY
- 大跌概率过高不能 BUY
- 置信度不足不能 BUY
- WARN 状态不能正式 BUY

---

## 18.5 HTML 验收

HTML 必须满足：

- 中文为主
- 第一屏能看懂结论
- BUY / HOLD / SELL 明显
- EV 明显
- 仓位明显
- 风险明显
- 风格简洁高级
- 不堆满技术字段
- 适合人做决策

---

# 19. 用户体验要求

V3.0 是给人用的，不是给程序员自嗨的。

页面必须避免：

- 大量英文缩写
- 大量模型字段
- 大量 JSON
- 无解释的概率
- 无结论的报告
- 看完不知道该不该买卖

页面必须做到：

- 一眼看到决策
- 一眼看到仓位
- 一眼看到风险
- 一眼看到 EV
- 一眼看到止盈止损
- 下面再展开模型解释

---

# 20. 最终定位

CNSV V3.0 是 CNSV 从研究系统进入真实人工交易使用的关键版本。

它的最终价值不是预测得多复杂，而是：

```text
让用户在真实买卖前，清楚知道：
能不能买；
买多少；
错了怎么办；
什么时候卖；
风险值不值得承担。
```

V3.0 必须服务于人工交易决策，而不是服务于模型展示。

---

# 21. 给 Codex 的开发要求

请严格按本文档开发 CNSV V3.0。

要求：

1. 不推倒重来  
2. 承接 V1.0 到 V2.0 的全部成果  
3. 新增 V3.0 交易决策层  
4. 输出 BUY / HOLD / SELL / WATCH / REDUCE / BLOCKED  
5. 输出次日涨跌概率  
6. 输出次日涨跌幅分布  
7. 输出 EV  
8. 输出风控状态  
9. 输出仓位建议  
10. 输出止盈止损参考  
11. 生成中文 HTML 看板  
12. HTML 风格简洁、高级、适合人工决策  
13. 所有测试必须通过  
14. 所有报告必须自动生成  
15. 不允许自动下单  
16. 不允许连接券商  
17. 不允许绕过 CNSVdata  

V3.0 的核心目标：

```text
把 CNSV 从“看懂市场”升级为“辅助真实买卖决策”。
```
