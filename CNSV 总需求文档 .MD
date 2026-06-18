# CNSV 中国船舶专业量化波段系统总需求文档 V2.0

## 0. 文档定位

本文档是 `CNSV` 主程序仓库的 V2.0 专业量化版总需求文档。

`CNSV` 是中国船舶 `600150.SH` 专用的专业量化研究与人工波段操作系统。

系统不是自动交易机器人。  
系统不连接券商接口。  
系统不自动下单。  
系统只负责数据读取、量化计算、价格分布预测、风险评估、人工执行计划、报告输出、回测复盘和模型自学习。

最终买卖由人工完成。

系统核心定位：

```text
量化数据底座
多周期价格分布预测
人工波段操作计划
风险控制系统
同类生态分析系统
回测验证系统
执行复盘系统
模型自学习系统
```

---

## 1. 项目基本信息

### 1.1 仓库名称

```text
CNSV
```

### 1.2 上游数据仓库

```text
CNSVdata
```

`CNSVdata` 负责拉取、清洗、标准化和保存上游数据。  
`CNSV` 原则上不直接调用 Tushare。

### 1.3 标的对象

```text
股票代码：600150.SH
股票名称：中国船舶
市场：A 股 / 上交所
系统类型：单标的专业量化波段系统
执行方式：人工手动买卖
```

### 1.4 TOKEN 原则

`TUSHARE_TOKEN` 默认只配置在 `CNSVdata`。

`CNSV` 默认不配置 `TUSHARE_TOKEN`。

原因：

```text
CNSVdata = 数据层
CNSV = 模型层 / 策略层 / 报告层
```

只有在未来需要 `CNSV` 临时补数据时，才允许增加 `TUSHARE_TOKEN`。  
第一版和 V2.0 主线都不建议这样做。

---

## 2. V2.0 总体目标

V2.0 不再只是输出“买入、卖出、持有”。

V2.0 每天必须回答：

```text
当前中国船舶处于什么波段状态？
下一个 A 股交易日价格分布如何？
未来 20 个交易日价格分布如何？
未来 60 个交易日价格分布如何？
未来 120 个交易日价格分布如何？
现在是低吸区、持有区、减仓区，还是风险区？
当前建议仓位是多少？
什么价格可以买？
什么价格不能买？
什么价格应该减仓？
什么价格必须止损？
同类标的是否共振？
行业生态是否支持？
大盘环境是否支持？
模型置信度是多少？
数据置信度是多少？
当前人工执行难度高不高？
模型是否出现漂移？
历史信号是否有效？
如果亏损，是模型错还是人工偏离？
```

---

## 3. 系统核心原则

### 3.1 人工执行，不自动交易

系统不连接券商。  
系统不自动买卖。  
系统不生成自动下单指令。

系统输出的是：

```text
信号
价格区间
仓位建议
止损价
减仓价
情景计划
禁止动作
风险提示
```

人工根据报告执行。

---

### 3.2 严格使用 A 股交易日历

系统所有时间窗口必须基于 A 股交易日历。

不允许用自然日粗算。

定义如下：

```text
T = 最新完整 A 股交易日
T+1 = 下一个 A 股开市交易日
20D = 未来约 20 个 A 股交易日
60D = 未来约 60 个 A 股交易日
120D = 未来约 120 个 A 股交易日
```

如果遇到周末、节假日、临时休市，系统必须自动跳过。

报告中不允许只写“明天”。  
必须写：

```text
下一个交易日：YYYY-MM-DD
未来 20 个交易日截止日：YYYY-MM-DD
未来 60 个交易日截止日：YYYY-MM-DD
未来 120 个交易日截止日：YYYY-MM-DD
```

---

### 3.3 输出价格分布，不输出单点幻想

系统不允许只输出一个目标价。

必须输出价格分布。

标准分布字段：

```text
P10：悲观价
P25：偏弱价
P50：中位价
P75：偏强价
P90：乐观价
```

所有预测周期都必须表达不确定性。

---

### 3.4 JSON 是唯一标准中间层

系统必须同时输出：

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

MD 和 HTML 必须从 JSON 派生。

禁止 HTML 页面写死字段。  
禁止 MD 和 HTML 各写一套逻辑。  
禁止报告字段错位。

---

### 3.5 数据异常时不得输出强信号

如果数据质量不通过，只能输出：

```text
数据异常报告
```

不得输出：

```text
强买入
买入
加仓
```

---

### 3.6 人工可执行优先

所有建议必须包含：

```text
价格
条件
仓位
止损
禁止动作
失效条件
```

禁止输出模糊建议，例如：

```text
支撑附近买入
压力附近卖出
情况不好就走
注意风险
```

---

## 4. 仓库目录结构 V2.0

```text
CNSV/
├── .github/
│   └── workflows/
│       ├── run_daily_signal.yml
│       ├── run_backtest.yml
│       ├── run_model_validation.yml
│       └── publish_pages.yml
├── config/
│   ├── strategy.yml
│   ├── risk.yml
│   ├── model.yml
│   ├── data_source.yml
│   ├── ecosystem.yml
│   └── report.yml
├── src/
│   └── cnsv/
│       ├── data/
│       │   ├── loader.py
│       │   ├── validator.py
│       │   ├── schema.py
│       │   └── trade_calendar.py
│       ├── features/
│       │   ├── trend_features.py
│       │   ├── minute_structure_features.py
│       │   ├── moneyflow_features.py
│       │   ├── support_resistance.py
│       │   ├── volatility_features.py
│       │   ├── ecosystem_features.py
│       │   ├── relative_strength_features.py
│       │   └── regime_features.py
│       ├── models/
│       │   ├── band_engine.py
│       │   ├── t1_distribution_engine.py
│       │   ├── medium_distribution_engine.py
│       │   ├── probability_engine.py
│       │   ├── expected_return_engine.py
│       │   ├── scenario_engine.py
│       │   ├── attribution_engine.py
│       │   ├── confidence_engine.py
│       │   ├── drift_monitor.py
│       │   └── self_learning.py
│       ├── strategy/
│       │   ├── entry_rules.py
│       │   ├── exit_rules.py
│       │   ├── position_sizing.py
│       │   ├── stop_loss.py
│       │   └── manual_execution_plan.py
│       ├── backtest/
│       │   ├── backtest_engine.py
│       │   ├── distribution_backtest.py
│       │   ├── metrics.py
│       │   ├── walk_forward.py
│       │   └── execution_delay_test.py
│       ├── report/
│       │   ├── report_json.py
│       │   ├── report_md.py
│       │   ├── report_html_data.py
│       │   ├── report_schema.py
│       │   └── publish_report.py
│       └── utils/
│           ├── logger.py
│           ├── math_utils.py
│           └── date_utils.py
├── reports/
│   ├── latest_signal.md
│   ├── latest_signal.json
│   ├── archive/
│   └── backtest/
├── docs/
│   ├── index.html
│   ├── decision.html
│   ├── distribution.html
│   ├── ecosystem.html
│   ├── backtest.html
│   ├── assets/
│   │   ├── style.css
│   │   └── app.js
│   └── data/
│       ├── latest_signal.json
│       ├── latest_backtest.json
│       ├── history_signals.json
│       └── ecosystem_latest.json
├── models/
│   ├── model_meta.json
│   ├── thresholds.json
│   ├── learning_log.jsonl
│   ├── drift_log.jsonl
│   └── validation_report.json
├── tests/
│   ├── test_loader.py
│   ├── test_validator.py
│   ├── test_trade_calendar.py
│   ├── test_features.py
│   ├── test_distribution.py
│   ├── test_strategy.py
│   ├── test_report_json.py
│   ├── test_report_md.py
│   ├── test_html_schema.py
│   └── test_no_future_leakage.py
├── requirements.txt
└── README.md
```

---

## 5. 数据输入需求 V2.0

### 5.1 必须读取的数据

从 `CNSVdata` 读取：

```text
cnsv_daily.parquet
cnsv_1min.parquet
cnsv_5min.parquet
cnsv_15min.parquet
cnsv_30min.parquet
cnsv_60min.parquet
cnsv_moneyflow.parquet
trade_calendar.parquet
latest_trade_date.json
data_quality_latest.json
```

### 5.2 指数数据

必须支持：

```text
上证指数
沪深300
中证500
中证1000
创业板指
中证军工
国防军工指数
船舶制造相关指数
```

### 5.3 同类标的池

第一版建议纳入：

```text
中国重工
中船防务
中国动力
中船科技
亚星锚链
江龙船艇
国瑞科技
军工 ETF
中证军工
沪深300
上证指数
中证500
```

同类标的不用于推荐买卖。  
只用于判断中国船舶的生态位置和相对强弱。

### 5.4 生态数据层

系统必须支持以下生态数据：

```text
标的自身数据
同类公司数据
船舶制造行业数据
军工板块数据
央企改革相关数据
大盘指数数据
资金风格数据
宏观环境数据
事件标签数据
```

### 5.5 数据质量要求

运行模型前必须检查：

```text
最新交易日是否一致
交易日历是否有效
日线数据是否存在
分钟数据是否存在
分钟数据是否断档
是否有重复时间戳
是否有异常空值
是否有未来数据
成交量是否异常为 0
价格字段是否异常
同类标的池是否可用
指数数据是否可用
数据质量报告是否通过
```

如果数据不完整，系统必须降低数据置信度。  
如果核心数据缺失，系统不得输出正式买入信号。

---

## 6. 配置文件需求 V2.0

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
  min_1: true
  min_5: true
  min_15: true
  min_30: true
  min_60: true

signal:
  min_buy_score: 70
  min_add_score: 80
  reduce_risk_score: 65
  clear_risk_score: 80

horizons:
  t1: true
  d20: true
  d60: true
  d120: true
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
  max_model_drift_level: "medium"
```

### 6.3 `config/model.yml`

```yaml
distribution:
  quantiles:
    - 0.10
    - 0.25
    - 0.50
    - 0.75
    - 0.90

horizons:
  t1: 1
  d20: 20
  d60: 60
  d120: 120

features:
  trend: true
  minute_structure: true
  moneyflow: true
  support_resistance: true
  volatility: true
  ecosystem: true
  relative_strength: true
  regime: true

learning:
  enabled: true
  log_path: "models/learning_log.jsonl"

drift:
  enabled: true
  log_path: "models/drift_log.jsonl"
```

### 6.4 `config/ecosystem.yml`

```yaml
peers:
  - ts_code: "601989.SH"
    name: "中国重工"
  - ts_code: "600685.SH"
    name: "中船防务"
  - ts_code: "600482.SH"
    name: "中国动力"
  - ts_code: "600072.SH"
    name: "中船科技"
  - ts_code: "601890.SH"
    name: "亚星锚链"

indices:
  - code: "000001.SH"
    name: "上证指数"
  - code: "000300.SH"
    name: "沪深300"
  - code: "000905.SH"
    name: "中证500"
  - code: "399967.SZ"
    name: "中证军工"
```

### 6.5 `config/report.yml`

```yaml
report:
  output_json: true
  output_md: true
  output_html_data: true
  archive: true

pages:
  enabled: true
  data_path: "docs/data/latest_signal.json"

sections:
  summary: true
  trade_calendar: true
  t1_distribution: true
  medium_distribution: true
  ecosystem: true
  scenario: true
  attribution: true
  confidence: true
  drift: true
  manual_plan: true
  review: true
```

---

## 7. 核心模块需求 V2.0

## 7.1 数据读取模块

路径：

```text
src/cnsv/data/loader.py
```

职责：

```text
读取 CNSVdata 标准数据
读取日线和分钟线
读取资金流
读取交易日历
读取同类标的
读取指数数据
统一字段
统一日期格式
返回标准 DataFrame
```

禁止直接调用 Tushare。

---

## 7.2 交易日历模块

路径：

```text
src/cnsv/data/trade_calendar.py
```

职责：

```text
识别最新完整交易日
识别下一个 A 股交易日
计算未来 20 个交易日截止日
计算未来 60 个交易日截止日
计算未来 120 个交易日截止日
跳过周末和节假日
防止自然日误判
```

核心输出：

```text
trade_date
next_trade_date
horizon_20d_end
horizon_60d_end
horizon_120d_end
```

---

## 7.3 数据校验模块

路径：

```text
src/cnsv/data/validator.py
```

职责：

```text
检查文件是否存在
检查交易日是否一致
检查 OHLCV 是否合理
检查分钟数据覆盖率
检查同类标的数据完整性
检查指数数据完整性
检查未来函数
生成数据置信度
```

输出：

```text
data_valid
data_confidence
missing_files
warnings
fatal_errors
```

---

## 7.4 趋势特征模块

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

趋势状态：

```text
强趋势
弱趋势
震荡
反弹
破位
```

---

## 7.5 分钟结构模块

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
冲高回落概率
低开修复概率
尾盘转强概率
```

---

## 7.6 波动率模块

路径：

```text
src/cnsv/features/volatility_features.py
```

需要计算：

```text
atr_14
volatility_20d
volatility_60d
realized_volatility
intraday_volatility
gap_risk
extreme_move_risk
```

用途：

```text
价格分布预测
止损距离计算
仓位控制
风险等级判断
```

---

## 7.7 资金流模块

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
moneyflow_persistence
```

资金状态：

```text
主力流入
温和流入
资金中性
主力流出
异常流出
```

---

## 7.8 支撑压力模块

路径：

```text
src/cnsv/features/support_resistance.py
```

需要计算：

```text
support_20d
support_60d
support_120d
resistance_20d
resistance_60d
resistance_120d
distance_to_support
distance_to_resistance
breakout_price
breakdown_price
hard_stop_price
trend_invalid_price
```

所有价格必须明确输出。

---

## 7.9 生态特征模块

路径：

```text
src/cnsv/features/ecosystem_features.py
```

职责：

```text
读取同类标的
计算行业共振
计算军工板块强弱
计算同类标的涨跌分布
判断中国船舶生态位置
```

输出：

```text
peer_strength_score
industry_strength_score
index_environment_score
ecosystem_state
leader_or_lagger
```

生态状态：

```text
个股独强
板块共振
行业领涨
行业补涨
指数带动
资金抱团
风险拖累
```

---

## 7.10 相对强弱模块

路径：

```text
src/cnsv/features/relative_strength_features.py
```

需要比较：

```text
中国船舶 vs 同类标的
中国船舶 vs 船舶行业
中国船舶 vs 军工板块
中国船舶 vs 上证指数
中国船舶 vs 沪深300
```

输出：

```text
relative_strength_5d
relative_strength_20d
relative_strength_60d
relative_rank_peer
relative_rank_industry
```

---

## 8. 价格分布预测系统

## 8.1 T+1 价格分布引擎

路径：

```text
src/cnsv/models/t1_distribution_engine.py
```

T+1 必须严格代表下一个 A 股交易日。

输出字段：

```text
next_trade_date
open_p10
open_p25
open_p50
open_p75
open_p90
high_p10
high_p25
high_p50
high_p75
high_p90
low_p10
low_p25
low_p50
low_p75
low_p90
close_p10
close_p25
close_p50
close_p75
close_p90
red_prob
green_prob
gap_up_prob
gap_down_prob
intraday_reversal_prob
low_open_repair_prob
extreme_up_prob
extreme_down_prob
```

T+1 报告必须服务人工操作。

必须回答：

```text
高开能不能追
低开能不能吸
冲高要不要减
跌破哪里必须走
尾盘是否适合留仓
```

---

## 8.2 中周期价格分布引擎

路径：

```text
src/cnsv/models/medium_distribution_engine.py
```

预测周期：

```text
20 个交易日
60 个交易日
120 个交易日
```

每个周期输出：

```text
p10
p25
p50
p75
p90
up_prob
down_prob
expected_return
expected_drawdown
trend_continue_prob
trend_reverse_prob
```

禁止只输出单一目标价。

---

## 8.3 多周期模型分层原则

不同周期不得混用同一套简单规则。

### T+1 模型重点

```text
分钟结构
VWAP
盘中承接
成交量变化
尾盘强度
短线资金流
当日市场情绪
```

### 20D 模型重点

```text
日线趋势
20 日均线
60 分钟结构
阶段成交量
资金连续性
板块共振
短波段支撑压力
```

### 60D 模型重点

```text
60 日趋势
120 日趋势
行业景气度
同类标的强弱
指数环境
估值位置
资金风格
```

### 120D 模型重点

```text
大周期趋势
行业周期
订单周期
估值周期
宏观流动性
军工船舶产业周期
市场风险偏好
```

---

## 9. 波段状态引擎

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

输出：

```text
band_state
band_state_name
band_score
state_reason
state_invalid_condition
```

---

## 10. 情景预测模块

路径：

```text
src/cnsv/models/scenario_engine.py
```

每份报告必须输出三种情景：

```text
基准情景
强势情景
弱势情景
```

每种情景必须包含：

```text
触发条件
价格区间
概率
人工动作
目标仓位
失效条件
```

示例：

```text
基准情景：震荡上行
强势情景：放量突破
弱势情景：跌破支撑
```

系统不得只输出单一方向判断。

---

## 11. 归因解释模块

路径：

```text
src/cnsv/models/attribution_engine.py
```

每个信号必须给出归因解释。

归因至少包括：

```text
价格结构归因
成交量归因
资金流归因
行业生态归因
指数环境归因
风险归因
```

报告必须说明：

```text
为什么给这个信号
主要支持因素是什么
主要反对因素是什么
最大风险是什么
关键观察位在哪里
判断失效条件是什么
```

---

## 12. 置信度系统

路径：

```text
src/cnsv/models/confidence_engine.py
```

系统必须区分：

```text
数据置信度
模型置信度
市场稳定度
执行难度
综合置信度
```

含义：

```text
数据置信度 = 数据是否完整可靠
模型置信度 = 模型信号是否稳定
市场稳定度 = 当前环境是否适合预测
执行难度 = 人工是否容易执行
综合置信度 = 最终报告可靠程度
```

硬规则：

```text
数据置信度不足，不得输出强买入
市场稳定度不足，降低仓位建议
执行难度过高，提示人工谨慎
模型置信度不足，降低信号等级
```

---

## 13. 买入规则模块

路径：

```text
src/cnsv/strategy/entry_rules.py
```

买入必须满足：

```text
日线位置合格
分钟结构确认
风险收益比合格
生态环境不拖累
数据置信度合格
模型置信度合格
```

买入信号分级：

```text
A+ 强买入
A 买入
B 试探买入
C 持有观察
F 禁止买入
```

强买入必须满足：

```text
多周期共振
风险收益比合格
T+1 分布不极端偏弱
20D 分布中位收益为正
生态数据不拖累
模型未漂移
```

---

## 14. 卖出规则模块

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

强制风险规则：

```text
跌破硬止损价，不得补仓
跌破趋势失效价，必须降仓
放量滞涨，必须提示减仓风险
冲高回落概率过高，降低追涨建议
```

---

## 15. 仓位模块

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

仓位由以下因素共同决定：

```text
波段状态
T+1 分布
20D 分布
风险收益比
模型置信度
数据置信度
市场稳定度
执行难度
模型漂移状态
```

输出：

```text
suggest_position
max_position_allowed
position_reason
position_risk_warning
```

---

## 16. 人工执行计划模块

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

每个场景必须输出：

```text
scenario
condition
action
target_position
forbidden
invalid_condition
```

报告必须明确告诉人工：

```text
什么情况可以买
什么情况不能买
什么情况要减仓
什么情况必须止损
什么情况只能观察
```

---

## 17. 报告系统 V2.0

## 17.1 JSON 报告

路径：

```text
reports/latest_signal.json
docs/data/latest_signal.json
```

JSON 是标准数据源。

V2.0 标准结构：

```json
{
  "meta": {
    "version": "2.0",
    "trade_date": "",
    "generated_at": "",
    "ts_code": "600150.SH",
    "name": "中国船舶",
    "mode": "manual_execution"
  },
  "trade_calendar": {
    "trade_date": "",
    "next_trade_date": "",
    "horizon_20d_end": "",
    "horizon_60d_end": "",
    "horizon_120d_end": ""
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
    "ecosystem_score": 0,
    "risk_score": 0,
    "confidence": 0
  },
  "price_distribution": {
    "t1": {},
    "d20": {},
    "d60": {},
    "d120": {}
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
  "scenario_forecast": {
    "base": {},
    "bull": {},
    "bear": {}
  },
  "ecosystem": {
    "peer_strength": {},
    "industry_strength": {},
    "index_strength": {},
    "relative_position": ""
  },
  "attribution": {
    "price": "",
    "volume": "",
    "moneyflow": "",
    "industry": "",
    "index": "",
    "risk": ""
  },
  "confidence_breakdown": {
    "data_confidence": 0,
    "model_confidence": 0,
    "market_stability": 0,
    "execution_difficulty": 0,
    "overall_confidence": 0
  },
  "model_drift": {
    "drift_detected": false,
    "drift_level": "",
    "reason": "",
    "action": ""
  },
  "manual_plan": [],
  "forbidden_actions": [],
  "execution_review": {
    "system_action": "",
    "actual_action": "",
    "execution_match": null,
    "deviation_reason": "",
    "execution_score": null
  }
}
```

---

## 17.2 Markdown 报告

路径：

```text
reports/latest_signal.md
reports/archive/YYYY-MM-DD_signal.md
```

MD 报告必须包含：

```text
报告摘要
严格交易日历
T+1 价格分布
未来 20D 价格分布
未来 60D 价格分布
未来 120D 价格分布
波段状态总表
人工操作计划表
价格执行区间表
生态数据总览
同类标的强弱表
三情景预测
归因解释
置信度拆解
模型漂移监控
禁止动作
风险提示
明日计划
复盘记录区
```

---

## 17.3 HTML 页面

路径：

```text
docs/index.html
docs/decision.html
docs/distribution.html
docs/ecosystem.html
docs/backtest.html
```

HTML 页面读取：

```text
docs/data/latest_signal.json
```

页面展示模块：

```text
顶部总览卡片
严格交易日历
T+1 价格分布
20D / 60D / 120D 价格分布
核心信号表
人工操作计划表
价格执行区间
生态数据总览
同类标的强弱
三情景预测
归因解释
置信度拆解
模型漂移监控
禁止动作
最近历史信号
回测摘要
```

禁止 HTML 写死字段。  
所有字段必须从 JSON 读取。

---

## 18. 回测系统 V2.0

路径：

```text
src/cnsv/backtest/
```

必须支持：

```text
历史买入信号回测
历史卖出信号回测
价格分布命中率回测
T+1 分布命中率
20D 分布命中率
60D 分布命中率
120D 分布命中率
止损触发统计
止盈触发统计
最大回撤统计
盈亏比统计
平均持仓天数
信号触发次数
人工延迟容错测试
```

核心指标：

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
P10/P50/P90 分布命中率
预测偏差
人工延迟损耗
```

---

## 19. 人工延迟容错

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

## 20. 模型漂移监控

路径：

```text
src/cnsv/models/drift_monitor.py
models/drift_log.jsonl
```

系统必须监控模型是否失效。

漂移信号包括：

```text
预测误差扩大
胜率连续下降
盈亏比下降
最大回撤扩大
信号过度频繁
信号长期不触发
价格分布偏离实际
阈值失效
```

出现模型漂移时，系统必须：

```text
降低信号等级
降低建议仓位
暂停强买入信号
输出模型漂移提示
进入重新校准流程
```

---

## 21. 自学习系统

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
T+1 实际走势
20D 实际走势
60D 实际走势
120D 实际走势
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

第一版自学习不要求复杂机器学习。  
第一版重点是把日志结构做稳。

---

## 22. 人工执行质量评分

因为系统是人工买卖，所以必须记录人工执行质量。

复盘字段：

```text
系统建议动作
人工实际动作
是否按价格区间执行
是否追高
是否止损
是否提前卖出
是否该减仓未减
是否该空仓却买入
实际盈亏
偏离原因
执行纪律评分
```

系统必须区分：

```text
模型错误
人工偏离
市场突发
数据异常
```

不能把所有亏损都归因于模型。

---

## 23. GitHub Actions 需求 V2.0

## 23.1 每日信号任务

路径：

```text
.github/workflows/run_daily_signal.yml
```

职责：

```text
读取 CNSVdata 数据
运行数据校验
计算交易日历
生成特征
运行波段引擎
运行价格分布引擎
运行生态分析
运行情景预测
运行归因解释
运行置信度系统
运行模型漂移检测
生成 JSON 报告
生成 MD 报告
同步 docs/data/latest_signal.json
提交 reports 和 docs/data
```

建议运行时间：

```text
北京时间 16:30 以后
```

---

## 23.2 回测任务

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

## 23.3 模型验证任务

路径：

```text
.github/workflows/run_model_validation.yml
```

职责：

```text
检查价格分布命中率
检查模型漂移
检查信号胜率
检查回撤变化
检查阈值是否失效
输出 validation_report.json
```

---

## 23.4 Pages 发布任务

路径：

```text
.github/workflows/publish_pages.yml
```

如果 GitHub Pages 设置为 `/docs`，可以简化。  
页面直接从 `docs/` 展示。

---

## 24. 测试需求 V2.0

必须有测试，不允许裸跑。

测试文件：

```text
tests/test_loader.py
tests/test_validator.py
tests/test_trade_calendar.py
tests/test_features.py
tests/test_distribution.py
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
交易日历是否正确
T+1 是否为下一个 A 股交易日
概率字段是否合法
价格分布字段是否合法
价格字段是否为空
MD 表头是否缺失
HTML 读取字段是否存在
reports/latest_signal.json 是否和 docs/data/latest_signal.json 一致
是否存在未来函数
仓位是否超过 80%
数据异常时是否禁止强买入
模型漂移时是否降级信号
```

---

## 25. 第一阶段 MVP 目标

V2.0 的 MVP 必须完成：

```text
读取 CNSVdata 数据
完成数据校验
完成严格 A 股交易日历
生成趋势特征
生成分钟结构特征
生成波动率特征
计算支撑压力
输出波段状态
输出 T+1 价格分布
输出 20D 价格分布
输出买卖价格区间
输出建议仓位
输出人工操作计划
输出 latest_signal.json
输出 latest_signal.md
输出 docs/data/latest_signal.json
HTML 页面能读取 JSON 展示
```

MVP 暂不强制完成：

```text
复杂机器学习
新闻 NLP
完整行业 NLP
高级宏观模型
自动交易
```

---

## 26. 第二阶段目标

第二阶段完成：

```text
完整回测系统
价格分布命中率回测
人工延迟容错测试
资金流评分
生态强弱评分
风险收益比模型
历史信号归档
HTML 历史信号表
```

---

## 27. 第三阶段目标

第三阶段完成：

```text
自学习日志
模型误差统计
阈值自动修正
行业共振模型
事件标签模型
模型漂移监控
更完整 HTML 看板
```

---

## 28. 输出结论规范

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
失效条件
```

---

## 29. 风险控制硬规则

系统必须遵守：

```text
默认最大仓位不超过 80%
第一买点默认不超过 20%
没有确认信号不允许加仓
跌破硬止损不得补仓
高开大幅冲高不得追涨
放量滞涨必须提示减仓风险
跌破趋势失效价必须提示清仓或降仓
数据异常时不得输出买入信号
模型漂移时不得输出强买入
回测未通过时不得升级为强买入
所有信号必须可复盘
```

---

## 30. 专业约束

系统必须遵守以下专业约束：

```text
不能用自然日代替交易日
不能只输出单点价格
不能只看个股自身数据
不能忽略同类标的生态
不能忽略指数环境
不能忽略模型漂移
不能把人工执行偏差算成模型错误
不能在数据异常时输出强信号
不能在回测不足时输出高置信强买入
不能输出没有价格、仓位、条件的模糊建议
```

---

## 31. 项目最终闭环

系统最终形成以下闭环：

```text
CNSVdata 拉取数据
↓
CNSV 读取数据
↓
数据质量校验
↓
严格交易日历计算
↓
特征工程
↓
生态数据分析
↓
价格分布预测
↓
波段状态判断
↓
三情景预测
↓
风险和置信度评估
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
↓
模型漂移监控
```

---

## 32. 项目核心结论

`CNSV` 的核心不是预测某一天涨跌。

它的核心是帮助人工交易者做五件事：

```text
什么时候可以买
什么时候不能买
什么时候必须卖
未来价格分布在哪里
当前判断是否可靠
```

系统必须始终坚持：

```text
数据清楚
交易日清楚
逻辑清楚
价格清楚
仓位清楚
风险清楚
生态清楚
置信度清楚
复盘清楚
```

这就是 `CNSV` 中国船舶专业量化波段系统 V2.0 的总需求框架。
