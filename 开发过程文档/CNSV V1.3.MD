# CNSV V1.3.MD — 路径分布层开发文档

> 交付对象：Codex  
> 适用仓库：`https://github.com/njedu2023-prog/CNSV`  
> 当前阶段：`CNSV V1.3_path_distribution`  
> 核心任务：在 V1.2 基准终点分布和 V1.2.2 验证层之后，开发 5D / 10D / 20D 路径分布与路径验证层。  
> 最高边界：V1.3 仍然不是交易信号层，不输出买卖建议，不输出仓位，不输出止盈止损，不连接券商，不自动下单。

---

## 0. 给 Codex 的总口令

继续 CNSV 主程序仓库主线，不回退旧话题，不推倒重来。

当前仓库：

```text
https://github.com/njedu2023-prog/CNSV
```

当前任务：

```text
CNSV V1.3 —— Path Distribution Layer / 路径分布层
```

本轮目标不是开发交易系统，而是开发观察级路径分布系统。

请严格基于现有 V1.0 / V1.1 / V1.2 / V1.2.1 / V1.2.2 已完成链路继续开发：

- V1.0：数据接线层；
- V1.1：特征层；
- V1.2：B0/B1/B2/B3 基准终点分布；
- V1.2.1：B2 状态分组样本修复；
- V1.2.2：baseline validation / walk-forward 验证层；
- V1.3：路径分布层，也就是本轮任务。

注意：

V1.2.2 验证显示，B2 当前没有稳定证明优于 B1。因此 V1.3 的主地基不应依赖 B2。V1.3 的默认主地基应是 B1 / B3，B2 只能作为辅助状态条件层。

---

## 1. V1.3 的核心目标

V1.2 解决的是：

```text
未来 5D / 10D / 20D 的终点收益分布大概在哪里。
```

V1.3 要解决的是：

```text
未来 5D / 10D / 20D 的过程中，价格路径可能怎么走。
```

V1.3 必须输出路径级分布，而不是只输出终点收益。

至少包括：

1. 终点收益分布；
2. 终点价格分布；
3. 路径最高点分布；
4. 路径最低点分布；
5. 最大上行幅度分布；
6. 最大下行幅度分布；
7. 最大回撤分布；
8. 路径波动分布；
9. 向上触达概率；
10. 向下触达概率；
11. 路径验证报告；
12. 防未来函数检查；
13. purged walk-forward 降重叠验证；
14. 明确声明不是交易信号。

---

## 2. V1.3 绝对禁止事项

本轮仍然不是交易系统。

严禁：

1. 不生成买入信号；
2. 不生成卖出信号；
3. 不输出目标仓位；
4. 不输出目标股数；
5. 不输出止盈；
6. 不输出止损；
7. 不输出交易建议；
8. 不输出“建议买入”“建议卖出”“加仓”“减仓”“清仓”；
9. 不连接券商接口；
10. 不自动下单；
11. 不配置或使用 `TUSHARE_TOKEN`；
12. 不绕过 CNSVdata；
13. 不直接从 Tushare 拉数据；
14. 不开发正式交易回测；
15. 不把 path report 命名成 signal；
16. 不把触达概率包装成目标价；
17. 不把下穿概率包装成止损建议；
18. 不把路径分布包装成正式操作建议；
19. 不把 B2/P2 强行作为核心模型；
20. 不因为路径触达概率高就输出任何操作动作。

允许输出：

```text
路径分布
触达概率
下穿概率
回撤概率
上行路径概率
下行路径概率
路径验证指标
风险提示
质量门禁结果
是否允许进入下一阶段
```

---

## 3. V1.3 模型框架

V1.3 建议采用三层路径模型：

```text
P0_historical_path_replay
P1_volatility_adjusted_path
P2_state_conditional_path
```

### 3.1 P0_historical_path_replay：历史路径回放

P0 是最基础的路径模型。

逻辑：

```text
从历史日线中抽取连续 5D / 10D / 20D 的真实路径片段。
把历史路径归一化到当前 latest_close。
生成未来路径样本池。
```

P0 的价值：

1. 保留真实 A 股单票路径形态；
2. 保留跳空、急涨、急跌、回撤、震荡；
3. 避免正态随机模拟过度平滑；
4. 作为所有路径模型的基础地基。

### 3.2 P1_volatility_adjusted_path：波动率调整路径

P1 在 P0 基础上加入当前波动率缩放。

逻辑：

```text
historical_path_return -> adjusted_path_return
adjusted_path_return = historical_path_return * volatility_scale
```

`volatility_scale` 可参考 B3 逻辑：

```text
volatility_scale = current_realized_vol_20d / historical_realized_vol_20d
```

要求：

1. `volatility_scale` 必须有限；
2. 不能为 NaN；
3. 不能为 inf；
4. 必须设置合理上下限；
5. 建议默认 clipping 区间为 `[0.5, 1.8]`；
6. 如果发生 clipping，必须写 warning；
7. 不允许 silent clipping。

### 3.3 P2_state_conditional_path：状态条件路径

P2 是辅助模型，不是核心模型。

状态字段来自 V1.1 / V1.2.1：

```text
trend_state
volatility_state
flow_strength_basic
```

逻辑：

```text
用当前状态键筛选历史同状态路径。
如果同状态样本充足，则生成状态条件路径分布。
如果样本不足，则透明 fallback 到 P1。
```

P2 要求：

1. 同状态路径样本数 >= 30 才允许独立输出；
2. 样本不足必须 fallback 到 P1；
3. fallback 必须写明 `fallback_used = true`；
4. fallback 必须写明 `fallback_reason`；
5. fallback 必须写明 `source_model = P1_volatility_adjusted_path`；
6. 不允许 P2 样本不足却伪装成功；
7. 报告必须说明 P2 是辅助层，不是核心依赖。

---

## 4. 建议新增文件结构

请根据仓库现有结构实现。实际路径可微调，但职责不能混乱。

```text
src/cnsv/path/__init__.py
src/cnsv/path/path_replay.py
src/cnsv/path/path_distribution.py
src/cnsv/path/path_metrics.py
src/cnsv/path/path_evaluator.py
src/cnsv/path/path_registry.py
src/cnsv/path/path_report.py
src/cnsv/path/path_validation.py
```

新增 CLI：

```text
src/cnsv/cli/run_path_distribution.py
src/cnsv/cli/run_path_validation.py
```

新增测试：

```text
tests/test_path_replay.py
tests/test_path_distribution.py
tests/test_path_metrics.py
tests/test_path_evaluator.py
tests/test_path_registry.py
tests/test_path_report.py
tests/test_path_validation.py
tests/test_path_cli.py
```

新增数据产物：

```text
docs/data/latest_path_distribution_report.json
docs/data/latest_path_validation_report.json
docs/data/path_distribution_registry.json
```

新增 Markdown 报告：

```text
reports/latest_path_distribution_report.md
reports/latest_path_validation_report.md
reports/archive/YYYY-MM-DD_path_distribution_report.md
reports/archive/YYYY-MM-DD_path_validation_report.md
```

新增前端页面：

```text
docs/path.html
```

更新入口：

```text
docs/index.html
```

新增 workflow：

```text
.github/workflows/run_path_distribution.yml
```

不要破坏现有文件：

```text
src/cnsv/cli/run_baseline_models.py
src/cnsv/cli/run_baseline_validation.py
docs/data/latest_baseline_model_report.json
docs/data/latest_baseline_validation_report.json
reports/latest_baseline_model_report.md
reports/latest_baseline_validation_report.md
docs/baseline.html
docs/validation.html
```

---

## 5. 输入数据要求

V1.3 必须继续遵守 CNSVdata 下游读取边界。

允许使用：

```text
daily.open
daily.high
daily.low
daily.close
daily.vol
daily.amount
trend_state
volatility_state
flow_strength_basic
realized_vol_20d
feature_history
baseline_validation_report
```

禁止：

```text
TUSHARE_TOKEN
券商接口
实时交易接口
外部直接拉取 Tushare
绕过 CNSVdata 的数据源
```

如果某些字段缺失：

1. 可以降级；
2. 必须在报告里记录；
3. 不能静默假装正常；
4. 不能用 fake 值伪造路径；
5. 不能用未来数据补当前字段。

---

## 6. 路径样本构造逻辑

对每个历史窗口，假设起点为 `t`，horizon 为 `h`。

### 6.1 路径窗口

```text
base_close = close[t]
future_close_path = close[t+1 : t+h]
future_high_path = high[t+1 : t+h]
future_low_path = low[t+1 : t+h]
```

### 6.2 收益路径

```text
close_return_path[i] = close[t+i] / close[t] - 1
high_return_path[i] = high[t+i] / close[t] - 1
low_return_path[i] = low[t+i] / close[t] - 1
```

### 6.3 当前价格映射

用最新价格 `latest_close` 映射为未来观察价格：

```text
future_close_price_path[i] = latest_close * (1 + close_return_path[i])
future_high_price_path[i] = latest_close * (1 + high_return_path[i])
future_low_price_path[i] = latest_close * (1 + low_return_path[i])
```

### 6.4 路径样本要求

1. 路径必须从 T+1 开始；
2. 不能包含 T 日之前的未来泄露；
3. 历史窗口必须完整覆盖 horizon；
4. close/high/low 缺失则剔除；
5. 剔除数量必须记录；
6. 每个 horizon 都要输出 path_count；
7. path_count = 0 必须 FAIL。

---

## 7. 必须输出的路径指标

每个模型、每个 horizon 至少输出：

```text
sample_size
path_count
latest_close

terminal_return_p10
terminal_return_p50
terminal_return_p90
terminal_price_p10
terminal_price_p50
terminal_price_p90

max_up_return_p10
max_up_return_p50
max_up_return_p90
max_up_price_p10
max_up_price_p50
max_up_price_p90

max_down_return_p10
max_down_return_p50
max_down_return_p90
max_down_price_p10
max_down_price_p50
max_down_price_p90

max_drawdown_p10
max_drawdown_p50
max_drawdown_p90

path_volatility_p50
path_volatility_p90

positive_terminal_prob
touch_up_3pct_prob
touch_up_5pct_prob
touch_up_8pct_prob
touch_down_3pct_prob
touch_down_5pct_prob
touch_down_8pct_prob

end_above_start_prob
intraperiod_any_up_prob
intraperiod_any_down_prob

fallback_used
fallback_reason
source_model
```

解释：

`touch_up_5pct_prob` 是路径中任意一天最高价触达 +5% 的概率。  
`touch_down_5pct_prob` 是路径中任意一天最低价下穿 -5% 的概率。  
`max_down_return` 是路径中相对起点的最低收益。  
`max_drawdown` 是路径内从阶段高点到后续低点的最大回撤。  
`positive_terminal_prob` 是终点收益为正的概率。

---

## 8. 触达概率的表达边界

允许表达：

```text
未来 20D 历史路径样本中，最高价触达 +5% 的比例为 X%。
未来 20D 历史路径样本中，最低价下穿 -5% 的比例为 Y%。
```

禁止表达：

```text
目标价是 XX
建议在 XX 买入
建议在 XX 卖出
建议在 XX 止盈
建议在 XX 止损
触达 XX 后应该卖出
下穿 XX 后应该割肉
```

所有触达和下穿概率都只是路径观察，不是交易动作。

---

## 9. 路径质量门禁 path_quality

新增：

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
2. 出现 buy/sell/position/stop_loss/take_profit 等字段；
3. 出现 NaN/inf；
4. 缺少 P0/P1/P2 核心产物；
5. P0/P1 缺少 5D/10D/20D 任一 horizon；
6. 分位数顺序错误；
7. 价格分位数 <= 0；
8. touch probability 不在 `[0, 1]`；
9. fallback_used=true 但 fallback_reason 为空；
10. P2 样本不足却没有 fallback；
11. 路径样本使用未来数据；
12. 报告命名或字段中出现正式 signal 字段；
13. path_count = 0；
14. latest_close 缺失或非正数。

### 9.2 可以 WARN 的情况

1. P2 fallback_rate 偏高；
2. P2 状态样本不足；
3. volatility_scale 被 clipping；
4. 部分路径因缺失数据被剔除；
5. 20D 样本较少；
6. 路径验证样本偏少；
7. P2 未优于 P1；
8. 触达概率区间过宽或过窄；
9. 当前 volatility_state 为 unknown。

---

## 10. 路径验证层 path_validation

V1.3 必须同时开发路径验证，不允许只生成路径报告。

新增命令：

```bash
python -m cnsv.cli.run_path_validation
```

验证逻辑：

对每个历史 `as_of_date = T`：

1. 只使用 T 日及 T 日之前的数据；
2. 生成 5D / 10D / 20D 路径分布；
3. 用真实 T+1 到 T+h 的 high / low / close 验证；
4. 验证终点收益；
5. 验证最高触达；
6. 验证最低下穿；
7. 验证最大回撤；
8. 验证路径区间覆盖；
9. 输出 standard walk-forward 指标；
10. 输出 purged walk-forward 指标。

必须输出：

```text
terminal_p10_p90_coverage
max_up_p10_p90_coverage
max_down_p10_p90_coverage
drawdown_p10_p90_coverage
touch_up_3pct_brier
touch_up_5pct_brier
touch_down_3pct_brier
touch_down_5pct_brier
positive_terminal_brier
path_interval_coverage
path_mae_terminal
path_rmse_terminal
fallback_rate
purged_sample_size
standard_sample_size
```

---

## 11. 防未来函数检查

V1.3 必须新增或复用 leakage checks。

至少检查：

1. 每个 as_of_date T 的训练数据最大日期 <= T；
2. T 日状态只由 T 及以前数据构造；
3. 真实验证结果只来自 T+1 到 T+h；
4. 不能用完整历史全样本来模拟历史 T 日；
5. 不能用未来 volatility_scale；
6. 不能用未来 high/low 构造 T 日路径预测；
7. purged 模式必须按 horizon 间隔抽样，降低重叠污染。

输出中必须包含：

```text
path_leakage_checks.status
path_leakage_checks.checks
purged_sample_mode
```

---

## 12. JSON 报告要求

新增：

```text
docs/data/latest_path_distribution_report.json
```

建议结构：

```json
{
  "meta": {
    "system": "CNSV",
    "version": "1.3.0",
    "stage": "V1.3_path_distribution",
    "report_type": "path_distribution_report",
    "ts_code": "600150.SH",
    "name": "中国船舶",
    "generated_at": "...",
    "latest_trade_date": "...",
    "is_trade_signal": false
  },
  "cnsvdata_gate": {},
  "path_quality": {},
  "current_state": {},
  "path_models": {
    "P0_historical_path_replay": {},
    "P1_volatility_adjusted_path": {},
    "P2_state_conditional_path": {}
  },
  "path_registry": [],
  "forbidden_actions": [
    "formal_signal_generation",
    "auto_order",
    "broker_api"
  ],
  "next_stage": "V1.4 observation backtest after path validation acceptance"
}
```

新增：

```text
docs/data/latest_path_validation_report.json
```

建议结构：

```json
{
  "meta": {
    "system": "CNSV",
    "version": "1.3.0",
    "stage": "V1.3_path_validation",
    "report_type": "path_validation_report",
    "ts_code": "600150.SH",
    "name": "中国船舶",
    "generated_at": "...",
    "is_trade_signal": false
  },
  "path_validation_quality": {},
  "validation_scope": {
    "horizons": [5, 10, 20],
    "models": [
      "P0_historical_path_replay",
      "P1_volatility_adjusted_path",
      "P2_state_conditional_path"
    ],
    "walk_forward": true,
    "purged_walk_forward": true
  },
  "standard_walk_forward_metrics": {},
  "purged_walk_forward_metrics": {},
  "p2_vs_p1": {},
  "path_leakage_checks": {},
  "forbidden_actions": [
    "formal_signal_generation",
    "auto_order",
    "broker_api"
  ],
  "next_stage": "V1.4 observation backtest after path validation acceptance"
}
```

---

## 13. Markdown 报告要求

新增：

```text
reports/latest_path_distribution_report.md
reports/latest_path_validation_report.md
```

MD 报告必须用中文说明：

1. 当前阶段；
2. 使用数据；
3. P0/P1/P2 路径模型；
4. 5D/10D/20D 终点分布；
5. 5D/10D/20D 路径最高点分布；
6. 5D/10D/20D 路径最低点分布；
7. 最大回撤分布；
8. 触达概率；
9. 下穿概率；
10. P2 是否 fallback；
11. path_quality 状态；
12. path_validation_quality 状态；
13. 是否允许进入 V1.4；
14. 明确声明：这不是交易信号。

---

## 14. HTML 页面要求

新增：

```text
docs/path.html
```

并在：

```text
docs/index.html
```

增加入口：

```text
Path Distribution Report
Path Validation Report
```

页面只展示路径观察与验证信息，不展示交易建议。

---

## 15. Registry 要求

新增：

```text
docs/data/path_distribution_registry.json
```

至少包含：

```json
[
  {
    "model_id": "P0_historical_path_replay",
    "model_name": "历史路径回放",
    "stage": "V1.3_path_distribution",
    "is_trade_signal": false,
    "horizons": [5, 10, 20],
    "input_data": ["daily.close", "daily.high", "daily.low"],
    "output_fields": [
      "terminal_return_p10",
      "terminal_return_p50",
      "terminal_return_p90",
      "max_up_return_p90",
      "max_down_return_p10",
      "touch_up_5pct_prob",
      "touch_down_5pct_prob"
    ]
  },
  {
    "model_id": "P1_volatility_adjusted_path",
    "model_name": "波动率调整路径回放",
    "stage": "V1.3_path_distribution",
    "is_trade_signal": false,
    "horizons": [5, 10, 20]
  },
  {
    "model_id": "P2_state_conditional_path",
    "model_name": "状态条件路径回放",
    "stage": "V1.3_path_distribution",
    "is_trade_signal": false,
    "horizons": [5, 10, 20]
  }
]
```

---

## 16. 测试要求

必须新增测试并跑通。

### 16.1 路径构造测试

构造简单 close/high/low 数据。

断言：

```text
路径数量正确
路径长度正确
terminal_return 正确
max_up_return 正确
max_down_return 正确
max_drawdown 正确
```

### 16.2 分位数测试

断言：

```text
p10 <= p50 <= p90
价格分位数 > 0
```

### 16.3 触达概率测试

构造固定路径。

断言：

```text
touch_up_3pct_prob 计算正确
touch_down_5pct_prob 计算正确
概率在 [0, 1]
```

### 16.4 波动率调整测试

断言：

```text
volatility_scale 计算正确
clipping 有 warning
clipping 不 silent
```

### 16.5 P2 fallback 测试

构造状态样本不足场景。

断言：

```text
fallback_used = true
fallback_reason 非空
source_model = P1_volatility_adjusted_path
path_quality 不 FAIL
```

构造伪装成功场景。

断言：

```text
P2 样本不足但 fallback_used = false 时，path_quality = FAIL
```

### 16.6 禁止交易字段测试

如果报告出现：

```text
buy_signal
sell_signal
target_position
stop_loss
take_profit
formal_signal
```

必须 FAIL。

### 16.7 防未来函数测试

断言：

```text
max_training_date <= as_of_date
state_date <= as_of_date
truth_start_date > as_of_date
truth_end_date = as_of_date + horizon
```

### 16.8 CLI 测试

执行：

```bash
python -m cnsv.cli.run_path_distribution
python -m cnsv.cli.run_path_validation
```

断言生成：

```text
docs/data/latest_path_distribution_report.json
docs/data/latest_path_validation_report.json
docs/data/path_distribution_registry.json
reports/latest_path_distribution_report.md
reports/latest_path_validation_report.md
docs/path.html
docs/index.html
```

---

## 17. GitHub Actions

新增：

```text
.github/workflows/run_path_distribution.yml
```

要求：

1. 安装依赖；
2. 运行 pytest；
3. 运行 baseline models；
4. 运行 baseline validation；
5. 运行 path distribution；
6. 运行 path validation；
7. 提交以下产物：

```text
docs/data/latest_path_distribution_report.json
docs/data/latest_path_validation_report.json
docs/data/path_distribution_registry.json
reports/latest_path_distribution_report.md
reports/latest_path_validation_report.md
reports/archive/*_path_distribution_report.md
reports/archive/*_path_validation_report.md
docs/path.html
docs/index.html
```

不要破坏现有 workflow：

```text
.github/workflows/check_data.yml
.github/workflows/run_features.yml
.github/workflows/run_baseline_models.yml
.github/workflows/run_baseline_validation.yml
```

---

## 18. 自检命令

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
```

不允许只改代码不跑测试。

---

## 19. 最终输出要求

完成后请给我一个简洁说明，必须包含：

1. 修改了哪些文件；
2. 是否新增 V1.3 路径分布层；
3. 是否新增路径验证层；
4. P0/P1/P2 是否完整；
5. 5D/10D/20D 是否全部覆盖；
6. P2 是否 fallback；
7. P2 是否仅作为辅助，不作为核心依赖；
8. 是否复用 walk-forward / purged 思路；
9. 是否通过 leakage checks；
10. 是否仍然禁止交易信号；
11. pytest 结果；
12. run_path_distribution 结果；
13. run_path_validation 结果；
14. 最新报告路径；
15. 是否可以进入 V1.4。

---

## 20. V1.3 验收标准

V1.3 通过条件：

1. `pytest` 通过；
2. `run_path_distribution` 通过；
3. `run_path_validation` 通过；
4. `latest_path_distribution_report.json` 正常生成；
5. `latest_path_validation_report.json` 正常生成；
6. `path_quality.status` 不得为 FAIL；
7. `path_validation_quality.status` 不得为 FAIL；
8. P0/P1/P2 均有产物；
9. P0/P1 必须完整覆盖 5D/10D/20D；
10. P2 可以 fallback，但必须透明；
11. 触达概率全部在 `[0, 1]`；
12. 分位数顺序正确；
13. 价格分位数全部 > 0；
14. 无 NaN/inf；
15. 无未来函数；
16. 无交易信号字段；
17. `is_trade_signal = false`；
18. `forbidden_actions` 包含 `formal_signal_generation`、`auto_order`、`broker_api`；
19. `docs/index.html` 有 Path Report 入口；
20. README 或开发文档说明 V1.3；
21. next_stage 写为：

```text
V1.4 observation backtest after path validation acceptance
```

---

## 21. V1.3 与 V1.4 的边界

V1.3 只做路径分布与路径验证。

V1.3 不做正式回测。

V1.4 才允许做：

```text
observation backtest
人工观察级策略回测
不同观察条件下的历史表现
```

但 V1.4 仍然不能自动交易，不能连接券商。

---

## 22. 核心原则

V1.3 要解决的是：

```text
未来 5D / 10D / 20D 不只是终点在哪里，而是中间路径可能怎么走。
```

V1.3 最重要的专业判断：

```text
B1/B3 是路径层主地基。
B2/P2 只能做辅助状态层。
路径报告必须带验证。
触达概率不是目标价。
下穿概率不是止损建议。
路径分布不是交易信号。
```

只有 V1.3 通过后，才允许进入 V1.4 observation backtest。
