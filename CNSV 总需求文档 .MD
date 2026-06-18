# CNSV 中国船舶人工波段量化系统需求框架

## 0. 文档定位

本文档是 `CNSV` 主程序仓库的总需求框架。

`CNSV` 是中国船舶 `600150.SH` 专用人工波段量化决策系统。  
系统定位不是自动交易机器人，而是：

> 量化计算 + 人工执行 + 报告看板 + 回测复盘 + 自学习修正系统

系统只负责输出信号、价格区间、仓位建议、风险提示和人工操作计划。  
最终买卖由人工手动完成。

---

## 1. 项目基本信息

### 1.1 仓库名称

```text
CNSV
```

### 1.2 项目对象

```text
股票代码：600150.SH
股票名称：中国船舶
市场：A 股 / 上交所
系统类型：单票专用波段量化系统
执行方式：人工手动买卖
```

### 1.3 上游数据仓库

```text
CNSVdata
```

`CNSVdata` 负责拉取、清洗、保存上游数据。  
`CNSV` 原则上不直接调用 Tushare。

### 1.4 TOKEN 原则

`CNSV` 默认不配置 `TUSHARE_TOKEN`。

Tushare TOKEN 只配置在：

```text
CNSVdata
```

原因：

```text
CNSVdata = 数据层
CNSV = 模型层、策略层、报告层
```

如未来 `CNSV` 需要临时补数据，才允许增加 `TUSHARE_TOKEN`，但第一版不建议这样做。

---

## 2. 系统总目标

`CNSV` 的目标不是简单预测“明天涨不涨”，而是每天回答以下问题：

1. 当前中国船舶处于什么波段状态？
2. 今天/明天是否适合买入、持有、加仓、减仓、清仓？
3. 如果买，合理买入区间是多少？
4. 如果卖，合理减仓区间是多少？
5. 如果判断错误，硬止损价是多少？
6. 当前建议仓位是多少？
7. 盘中不同走势下，人工应该怎么操作？
8. 哪些动作今天禁止做？
9. 历史信号是否有效？
10. 模型错误和人工执行偏差如何区分？

---

## 3. 系统核心原则

### 3.1 不自动下单

系统不连接券商交易接口。  
系统不执行自动买入、自动卖出。

所有交易动作由人工完成。

### 3.2 数据和模型分离

`CNSVdata` 负责数据。  
`CNSV` 负责模型和报告。

`CNSV` 不污染上游数据。

### 3.3 JSON 为标准中间层

系统输出必须同时生成：

```text
reports/latest_signal.json
reports/latest_signal.md
docs/data/latest_signal.json
docs/index.html
docs/decision.html
```

其中：

```text
JSON = 标准数据源
MD = 归档复盘报告
HTML = 网页看板
```

MD 和 HTML 都应从 JSON 派生，避免字段错位。

### 3.4 人工可执行优先

策略不是越复杂越好。  
必须保证人工能看懂、能执行、能复盘。

不允许输出模糊结论，例如：

```text
支撑附近买入
压力附近减仓
情况不好就卖
```

必须输出明确价格和明确条件。

---

## 4. 仓库目录结构要求

第一版建议目录结构如下：

```text
CNSV/
├── .github/
│   └── workflows/
│       ├── run_daily_signal.yml
│       ├── run_backtest.yml
│       └── publish_pages.yml
├── config/
│   ├── strategy.yml
│   ├── risk.yml
│   ├── model.yml
│   └── data_source.yml
├── src/
│   └── cnsv/
│       ├── data/
│       │   ├── loader.py
│       │   └── validator.py
│       ├── features/
│       │   ├── trend_features.py
│       │   ├── minute_structure_features.py
│       │   ├── moneyflow_features.py
│       │   ├── support_resistance.py
│       │   └── regime_features.py
│       ├── models/
│       │   ├── band_engine.py
│       │   ├── probability_engine.py
│       │   ├── expected_return_engine.py
│       │   └── self_learning.py
│       ├── strategy/
│       │   ├── entry_rules.py
│       │   ├── exit_rules.py
│       │   ├── position_sizing.py
│       │   ├── stop_loss.py
│       │   └── manual_execution_plan.py
│       ├── backtest/
│       │   ├── backtest_engine.py
│       │   ├── metrics.py
│       │   └── walk_forward.py
│       ├── report/
│       │   ├── report_json.py
│       │   ├── report_md.py
│       │   ├── report_html_data.py
│       │   └── publish_report.py
│       └── utils/
│           ├── trading_calendar.py
│           └── logger.py
├── reports/
│   ├── latest_signal.md
│   ├── latest_signal.json
│   ├── archive/
│   └── backtest/
├── docs/
│   ├── index.html
│   ├── decision.html
│   ├── backtest.html
│   ├── assets/
│   │   ├── style.css
│   │   └── app.js
│   └── data/
│       ├── latest_signal.json
│       ├── latest_backtest.json
│       └── history_signals.json
├── models/
│   ├── model_meta.json
│   ├── thresholds.json
│   └── learning_log.jsonl
├── tests/
│   ├── test_loader.py
│   ├── test_features.py
│   ├── test_strategy.py
│   ├── test_report_json.py
│   ├── test_report_md.py
│   ├── test_html_schema.py
│   └── test_no_future_leakage.py
├── requirements.txt
└── README.md
```

---

## 5. 数据输入需求

### 5.1 数据来源

`CNSV` 从 `CNSVdata` 读取数据。

推荐读取路径：

```text
../CNSVdata/data/processed/
```

或通过配置指定远程路径。

### 5.2 必须读取的数据

```text
cnsv_daily.parquet
cnsv_5min.parquet
cnsv_15min.parquet
cnsv_30min.parquet
cnsv_60min.parquet
cnsv_moneyflow.parquet
latest_trade_date.json
data_quality_latest.json
```

### 5.3 可选数据

```text
index_daily.parquet
industry_daily.parquet
limitup_emotion.parquet
news_event_tags.json
northbound_flow.parquet
```

### 5.4 数据质量要求

运行模型前必须检查：

1. 最新交易日是否一致；
2. 日线数据是否存在；
3. 分钟数据是否存在；
4. 是否有重复时间戳；
5. 是否有异常空值；
6. 是否有未来函数；
7. 是否有成交量异常为 0；
8. 是否有价格字段异常；
9. 是否和交易日历匹配；
10. 数据质量报告是否通过。

如果数据质量不通过，系统不得输出正式买卖信号，只能输出“数据异常报告”。

---

## 6. 配置文件需求

### 6.1 `config/strategy.yml`

```yaml
target:
  ts_code: "600150.SH"
  name: "中国船舶"

mode:
  execution: "manual"
  auto_order: false

timeframes:
  daily: true
  min_5: true
  min_15: true
  min_30: true
  min_60: true

signal:
  min_buy_score: 70
  min_add_score: 80
  reduce_risk_score: 65
  clear_risk_score: 80
```

### 6.2 `config/risk.yml`

```yaml
position:
  max_position: 0.80
  base_position: 0.20
  add_position: 0.20
  reduce_position: 0.30

risk:
  hard_stop_loss_pct: 0.04
  max_single_trade_loss_pct: 0.05
  min_reward_risk_ratio: 1.50
  max_intraday_chase_pct: 0.03
```

### 6.3 `config/model.yml`

```yaml
model:
  probability_window:
    - 3
    - 5
    - 10

features:
  trend: true
  minute_structure: true
  moneyflow: true
  support_resistance: true
  risk: true

learning:
  enabled: true
  log_path: "models/learning_log.jsonl"
```

### 6.4 `config/data_source.yml`

```yaml
data_source:
  repo: "CNSVdata"
  local_path: "../CNSVdata/data/processed"
  remote_enabled: false

required_files:
  - "cnsv_daily.parquet"
  - "cnsv_5min.parquet"
  - "cnsv_15min.parquet"
  - "cnsv_30min.parquet"
  - "cnsv_60min.parquet"
  - "cnsv_moneyflow.parquet"
```

---

## 7. 核心模块需求

## 7.1 数据读取模块

路径：

```text
src/cnsv/data/loader.py
```

职责：

1. 读取 `CNSVdata` 的 processed 数据；
2. 统一字段名；
3. 统一日期格式；
4. 返回标准 DataFrame；
5. 不直接调用 Tushare。

核心函数建议：

```python
load_daily_data()
load_minute_data(freq: str)
load_moneyflow_data()
load_latest_trade_date()
load_data_quality_report()
```

---

## 7.2 数据校验模块

路径：

```text
src/cnsv/data/validator.py
```

职责：

1. 检查数据是否存在；
2. 检查最新交易日是否一致；
3. 检查 OHLC 是否合理；
4. 检查分钟数据是否断档；
5. 检查是否有未来数据；
6. 生成校验结果。

核心函数建议：

```python
validate_all_inputs()
validate_trade_date_consistency()
validate_ohlcv()
validate_no_future_leakage()
validate_minute_coverage()
```

---

## 7.3 趋势特征模块

路径：

```text
src/cnsv/features/trend_features.py
```

需要计算：

```text
ma5
ma10
ma20
ma30
ma60
ma120
close_above_ma20
close_above_ma60
ma20_slope
ma60_slope
trend_score
trend_state
```

趋势状态建议：

```text
强趋势
弱趋势
震荡
破位
反弹
```

---

## 7.4 分钟结构模块

路径：

```text
src/cnsv/features/minute_structure_features.py
```

需要计算：

```text
vwap
close_vs_vwap
morning_strength
afternoon_strength
tail_strength
intraday_drawdown
intraday_rebound_ratio
minute_trend_score
minute_support_score
```

周期要求：

```text
5min
15min
30min
60min
```

用途：

1. 判断盘中承接；
2. 判断是否适合低吸；
3. 判断是否冲高回落；
4. 判断尾盘是否强；
5. 判断盘中是否转弱。

---

## 7.5 资金流模块

路径：

```text
src/cnsv/features/moneyflow_features.py
```

需要计算：

```text
net_mf_amount
main_net_inflow
large_order_inflow
retail_outflow
moneyflow_score
moneyflow_state
```

资金状态建议：

```text
主力流入
温和流入
资金中性
主力流出
异常流出
```

---

## 7.6 支撑压力模块

路径：

```text
src/cnsv/features/support_resistance.py
```

需要计算：

```text
support_20d
support_60d
resistance_20d
resistance_60d
distance_to_support
distance_to_resistance
breakout_price
breakdown_price
```

价格区间必须明确输出，不允许只输出文字描述。

---

## 7.7 波段状态引擎

路径：

```text
src/cnsv/models/band_engine.py
```

波段状态定义：

```text
S0 空仓观察
S1 回踩观察
S2 低吸买点
S3 趋势持有
S4 冲高减仓
S5 破位退出
```

输出字段：

```text
band_state
band_state_name
band_score
state_reason
```

---

## 7.8 概率引擎

路径：

```text
src/cnsv/models/probability_engine.py
```

输出：

```text
up_prob_3d
up_prob_5d
up_prob_10d
down_prob_3d
down_prob_5d
down_prob_10d
confidence
```

概率必须满足：

```text
0 <= probability <= 1
```

或统一转为百分比展示。

---

## 7.9 预期收益引擎

路径：

```text
src/cnsv/models/expected_return_engine.py
```

输出：

```text
expected_return_3d
expected_return_5d
expected_return_10d
expected_high_price
expected_low_price
reward_risk_ratio
```

必须判断：

```text
预期上涨空间 / 预期下跌风险 >= 1.5
```

否则不能输出强买入。

---

## 7.10 买入规则模块

路径：

```text
src/cnsv/strategy/entry_rules.py
```

买入不是只看上涨概率。

买入必须满足三重确认：

```text
日线位置合格
分钟结构确认
风险收益比合格
```

买入信号分级：

```text
A+ 强买入
A 买入
B 试探买入
C 持有观察
F 禁止买入
```

---

## 7.11 卖出规则模块

路径：

```text
src/cnsv/strategy/exit_rules.py
```

卖出分三类：

```text
止损卖出
止盈减仓
趋势破坏卖出
```

必须输出：

```text
reduce_zone_1
reduce_zone_2
hard_stop_price
trend_invalid_price
clear_condition
```

---

## 7.12 仓位模块

路径：

```text
src/cnsv/strategy/position_sizing.py
```

仓位档位：

```text
0%
20%
40%
60%
80%
```

默认不建议 100% 满仓。

输出字段：

```text
suggest_position
position_reason
max_position_allowed
```

---

## 7.13 人工执行计划模块

路径：

```text
src/cnsv/strategy/manual_execution_plan.py
```

这是系统核心模块之一。

必须输出盘中场景化操作计划。

场景至少包括：

```text
高开
低开
平开震荡
放量突破
缩量回踩
冲高回落
跌破支撑
尾盘转强
尾盘转弱
```

每个场景输出：

```text
scenario
condition
action
target_position
forbidden
```

---

## 8. 报告系统需求

## 8.1 JSON 报告

路径：

```text
reports/latest_signal.json
docs/data/latest_signal.json
```

JSON 是标准数据源。  
MD 和 HTML 都必须从 JSON 派生。

标准结构：

```json
{
  "meta": {
    "trade_date": "",
    "generated_at": "",
    "ts_code": "600150.SH",
    "name": "中国船舶",
    "mode": "manual_execution"
  },
  "summary": {
    "close": 0,
    "state": "",
    "signal_level": "",
    "conclusion": "",
    "suggest_position": 0,
    "risk_level": ""
  },
  "scores": {
    "trend_score": 0,
    "minute_support_score": 0,
    "moneyflow_score": 0,
    "risk_score": 0,
    "confidence": 0
  },
  "probability": {
    "up_prob_3d": 0,
    "up_prob_5d": 0,
    "up_prob_10d": 0,
    "down_prob_3d": 0,
    "down_prob_5d": 0,
    "down_prob_10d": 0
  },
  "price_plan": {
    "buy_zone_1": [0, 0],
    "buy_zone_2": [0, 0],
    "add_confirm_price": 0,
    "reduce_zone_1": [0, 0],
    "reduce_zone_2": [0, 0],
    "hard_stop_price": 0,
    "trend_invalid_price": 0
  },
  "manual_plan": [],
  "watch_fields": {},
  "forbidden_actions": [],
  "review": {}
}
```

---

## 8.2 Markdown 报告

路径：

```text
reports/latest_signal.md
reports/archive/YYYY-MM-DD_signal.md
```

MD 报告必须包含：

```text
报告摘要
波段状态总表
人工操作计划表
价格执行区间表
盘中观察字段表
禁止动作
风险提示
明日计划
复盘记录区
```

---

## 8.3 HTML 报告页面

路径：

```text
docs/index.html
docs/decision.html
docs/backtest.html
```

HTML 页面读取：

```text
docs/data/latest_signal.json
```

页面展示模块：

```text
顶部总览卡片
核心信号表
人工操作计划表
价格执行区间
禁止动作
最近历史信号
回测摘要
```

HTML 禁止写死旧字段。  
所有字段必须从 JSON 读取。

---

## 9. 回测系统需求

路径：

```text
src/cnsv/backtest/
```

回测系统必须支持：

```text
历史买入信号回测
历史卖出信号回测
止损触发统计
止盈触发统计
最大回撤统计
盈亏比统计
平均持仓天数
信号触发次数
人工延迟容错测试
```

### 9.1 核心指标

```text
胜率
盈亏比
最大回撤
最大连续亏损
平均持仓天数
信号次数
买入区间命中率
止损触发率
止盈触发率
```

### 9.2 人工延迟容错

必须测试：

```text
晚买 5 分钟
晚买 15 分钟
晚买 30 分钟
晚卖 5 分钟
晚卖 15 分钟
晚卖 30 分钟
```

如果策略必须极短时间执行才有效，则不适合人工系统。

---

## 10. 自学习系统需求

路径：

```text
src/cnsv/models/self_learning.py
models/learning_log.jsonl
models/model_meta.json
models/thresholds.json
```

每天记录：

```text
系统预测
实际走势
预测误差
系统建议动作
人工实际动作
是否按系统执行
偏离原因
最终结果
```

必须区分：

```text
模型判断错误
人工执行偏差
市场突发事件
数据异常
```

自学习第一版不要求复杂机器学习。  
第一版重点是把日志结构做稳。

---

## 11. GitHub Actions 需求

## 11.1 每日信号任务

路径：

```text
.github/workflows/run_daily_signal.yml
```

职责：

```text
读取 CNSVdata 数据
运行数据校验
生成特征
运行波段引擎
生成 JSON 报告
生成 MD 报告
同步 docs/data/latest_signal.json
提交 reports 和 docs/data
```

建议运行时间：

```text
北京时间 16:30 以后
```

因为 A 股 15:00 收盘，数据可能有延迟。

---

## 11.2 回测任务

路径：

```text
.github/workflows/run_backtest.yml
```

职责：

```text
手动触发或每周运行
生成 backtest_report.md
生成 latest_backtest.json
同步 docs/data/latest_backtest.json
```

---

## 11.3 Pages 发布任务

路径：

```text
.github/workflows/publish_pages.yml
```

如果 GitHub Pages 设置为 `/docs`，可以简化。  
页面直接从 `docs/` 展示。

---

## 12. 测试需求

必须有测试，不允许裸跑。

测试文件：

```text
tests/test_loader.py
tests/test_features.py
tests/test_strategy.py
tests/test_report_json.py
tests/test_report_md.py
tests/test_html_schema.py
tests/test_no_future_leakage.py
```

重点检查：

```text
latest_signal.json 是否存在
JSON 字段是否完整
概率字段是否合法
价格字段是否为空
MD 表头是否缺失
HTML 读取字段是否存在
reports/latest_signal.json 是否和 docs/data/latest_signal.json 一致
是否存在未来函数
仓位是否超过 80%
```

---

## 13. 第一阶段 MVP 目标

第一阶段不要追求复杂 AI。  
先做一个稳定、能每天跑、能看报告、能人工执行的版本。

MVP 必须完成：

```text
读取 CNSVdata 数据
完成数据校验
生成趋势特征
生成分钟结构特征
计算支撑压力
输出波段状态
输出买卖价格区间
输出建议仓位
输出人工操作计划
输出 latest_signal.json
输出 latest_signal.md
输出 docs/data/latest_signal.json
HTML 页面能读取 JSON 展示
```

MVP 不强制完成：

```text
复杂机器学习
新闻 NLP
行业联动
高级资金模型
自动交易
```

---

## 14. 第二阶段升级目标

第二阶段完成：

```text
完整回测系统
人工延迟容错测试
资金流评分
风险收益比模型
历史信号归档
HTML 历史信号表
```

---

## 15. 第三阶段升级目标

第三阶段完成：

```text
自学习日志
模型误差统计
阈值自动修正
行业共振模型
事件标签模型
更完整 HTML 看板
```

---

## 16. 输出结论规范

系统每日必须输出明确结论。

允许结论：

```text
观望
试探买入
买入
加仓
持有
减仓
清仓
禁止买入
```

不允许结论：

```text
看情况
可能可以
支撑附近
压力附近
注意风险
```

所有操作建议必须配套：

```text
价格
条件
仓位
止损
禁止动作
```

---

## 17. 风险控制硬规则

1. 默认最大仓位不超过 80%；
2. 第一买点默认不超过 20%；
3. 没有确认信号不允许加仓；
4. 跌破硬止损不得补仓；
5. 高开大幅冲高不得追涨；
6. 放量滞涨必须提示减仓风险；
7. 跌破趋势失效价必须提示清仓或降仓；
8. 数据异常时不得输出买入信号；
9. 回测未通过时不得升级为强买入；
10. 所有信号必须可复盘。

---

## 18. 项目最终闭环

系统最终形成以下闭环：

```text
CNSVdata 拉取数据
↓
CNSV 读取数据
↓
数据质量校验
↓
特征工程
↓
波段状态判断
↓
概率与收益计算
↓
人工操作计划生成
↓
JSON / MD / HTML 报告输出
↓
人工手动买卖
↓
盘后复盘记录
↓
模型自学习修正
```

---

## 19. 项目核心结论

`CNSV` 的核心不是预测某一天涨跌。  
它的核心是帮助人工交易者做三件事：

```text
什么时候可以买
什么时候不能买
什么时候必须卖
```

系统必须始终坚持：

```text
数据清楚
逻辑清楚
价格清楚
仓位清楚
风险清楚
复盘清楚
```

这就是 `CNSV` 中国船舶人工波段量化系统的总需求框架。
