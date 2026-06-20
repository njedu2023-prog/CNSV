
# CNSV V1.4.MD — 观察级回测层开发文档

> 交付对象：Codex  
> 适用仓库：`https://github.com/njedu2023-prog/CNSV`  
> 当前正式阶段：`CNSV V1.4_observation_backtest`  
> 核心任务：在 V1.3 路径分布层之后，开发观察级回测层，验证路径分布、触达概率、下穿概率、回撤风险在历史上的参考价值。  
> 最高边界：V1.4 仍然不是交易系统，不输出买卖建议，不输出仓位，不输出止盈止损，不连接券商，不自动下单。

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
"version": "1.4"
```

本轮 stage 统一使用：

```json
"stage": "V1.4_observation_backtest"
```

严禁把阶段内修复项写成正式版本号。不要写三段式子版本号或类似碎片化版本。


---

## 1. 当前阶段锚点

当前已完成：

1. V1.0 数据接线层；
2. V1.1 特征层；
3. V1.2 基准模型层；
4. V1.3 路径分布层；
5. V1.3 已完成路径分布与路径验证；
6. V1.3 已明确：
   - `is_trade_signal = false`
   - 禁止正式交易信号；
   - 禁止券商接口；
   - 禁止自动下单；
   - P2 只是辅助状态路径层，不作为核心依赖。

本轮任务：

```text
CNSV V1.4 —— Observation Backtest Layer / 观察级回测层
```

V1.4 要回答的问题：

```text
V1.3 路径分布、触达概率、下穿概率、回撤风险，在历史上到底有没有参考价值？
```

V1.4 是给 V1.5 人工决策辅助层准备证据，不是直接输出决策。


---

## 2. V1.4 核心定位

V1.4 是观察级回测，不是正式交易回测。

V1.4 不回答：

```text
应该不应该买？
应该不应该卖？
仓位是多少？
止盈止损在哪里？
```

V1.4 只回答：

```text
当路径分布出现某些观察条件时，历史后续表现如何？
这些路径指标是否有区分度？
哪些观察条件历史上风险更高？
哪些观察条件历史上更容易出现上行触达？
哪些观察条件历史上更容易出现下穿与回撤？
P0/P1/P2 哪个路径模型更有历史解释力？
```

V1.4 的产出是“证据层”，不是“操作层”。


---

## 3. V1.4 严禁事项

本轮仍然不是交易系统。

严禁：

1. 不生成买入信号；
2. 不生成卖出信号；
3. 不输出目标仓位；
4. 不输出目标股数；
5. 不输出止盈；
6. 不输出止损；
7. 不输出交易建议；
8. 不输出“建议买入”；
9. 不输出“建议卖出”；
10. 不输出“加仓”；
11. 不输出“减仓”；
12. 不输出“清仓”；
13. 不连接券商接口；
14. 不自动下单；
15. 不配置或使用 `TUSHARE_TOKEN`；
16. 不绕过 CNSVdata；
17. 不直接从 Tushare 拉数据；
18. 不把 observation backtest 报告命名成 signal；
19. 不把观察条件包装成交易策略；
20. 不把历史表现包装成未来承诺；
21. 不因为某个条件历史收益较好就输出操作动作。

允许输出：

```text
观察条件
历史样本数
历史平均收益
历史中位数收益
历史分位数收益
历史触达率
历史下穿率
历史回撤分布
条件分组表现
模型区分度
风险分层
观察级结论
是否允许进入 V1.5
```


---

## 4. V1.4 与 V1.3 的关系

V1.3 负责生成路径分布。  
V1.4 负责验证这些路径分布在历史观察中的价值。

V1.3 输出类似：

```text
未来 20D 触达 +5% 的路径概率是多少？
未来 20D 下穿 -5% 的路径概率是多少？
未来 20D 最大回撤分布是多少？
```

V1.4 要验证：

```text
历史上 touch_up_5pct_prob 高的时候，后续是否真的更容易触达 +5%？
历史上 touch_down_5pct_prob 高的时候，后续是否真的更容易下穿 -5%？
历史上 max_drawdown_p90 较高的时候，后续是否真的风险更大？
历史上 P1 是否比 P0 更有区分度？
历史上 P2 是否只是辅助，还是有稳定增益？
```


---

## 5. V1.4 核心回测对象

V1.4 不是回测交易动作，而是回测观察条件。

核心路径模型：

```text
P0_historical_path_replay
P1_volatility_adjusted_path
P2_state_conditional_path
```

核心 horizon：

```text
5D
10D
20D
```

核心观察指标：

```text
positive_terminal_prob
touch_up_3pct_prob
touch_up_5pct_prob
touch_up_8pct_prob
touch_down_3pct_prob
touch_down_5pct_prob
touch_down_8pct_prob
terminal_return_p10
terminal_return_p50
terminal_return_p90
max_up_return_p50
max_up_return_p90
max_down_return_p10
max_down_return_p50
max_drawdown_p50
max_drawdown_p90
path_volatility_p50
path_volatility_p90
fallback_used
state_key
state_sample_size
```

核心真实结果：

```text
actual_terminal_return
actual_positive_terminal
actual_touch_up_3pct
actual_touch_up_5pct
actual_touch_up_8pct
actual_touch_down_3pct
actual_touch_down_5pct
actual_touch_down_8pct
actual_max_up_return
actual_max_down_return
actual_max_drawdown
actual_path_volatility
```


---

## 6. 观察级回测方法

对每一个历史 `as_of_date = T`：

1. 只使用 T 日及 T 日之前的数据；
2. 调用或复用 V1.3 路径分布逻辑；
3. 生成 T 日视角下的 P0/P1/P2 路径分布；
4. 等待真实 T+1 到 T+h 的 high / low / close 出现；
5. 计算真实终点收益、最高触达、最低下穿、最大回撤；
6. 将“预测路径观察指标”与“真实路径结果”写成 observation backtest row；
7. 对所有历史 row 做分组、覆盖、校准、区分度统计；
8. 同时输出 standard walk-forward 与 purged walk-forward。

伪代码：

```text
for as_of_date in historical_dates:
    history = data[data.trade_date <= as_of_date]

    for horizon in [5, 10, 20]:
        if truth window T+1 to T+h does not exist:
            skip

        path_prediction = build_path_distribution(history, as_of_date, horizon)
        truth = calculate_actual_path_outcome(data, as_of_date, horizon)

        save row:
            as_of_date
            horizon
            model_id
            observation_features
            predicted_path_metrics
            actual_path_outcomes
            fallback_used
            state_key
            leakage_check
```


---

## 7. 必须防未来函数

V1.4 是回测层，未来函数风险比 V1.3 更严重。

必须检查：

1. 每个 as_of_date T 的训练数据最大日期 <= T；
2. 路径预测使用的数据最大日期 <= T；
3. 状态字段来自 T 日及以前；
4. 波动率字段来自 T 日及以前；
5. 真实结果只能来自 T+1 到 T+h；
6. 不能用全样本路径分布回测历史 T 日；
7. 不能用未来 high/low/close 构造 T 日预测；
8. 不能用未来真实结果反过来筛选观察条件；
9. 不能用未来收益构造状态标签；
10. purged 模式必须按 horizon 间隔抽样，降低重叠污染。

输出必须包含：

```text
observation_backtest_leakage_checks.status
observation_backtest_leakage_checks.checks
purged_sample_mode
standard_walk_forward_enabled
purged_walk_forward_enabled
```


---

## 8. 必须实现的观察分组

V1.4 必须按指标分组，而不是只输出全样本均值。

### 8.1 触达概率分组

对每个模型、每个 horizon：

```text
touch_up_3pct_prob
touch_up_5pct_prob
touch_up_8pct_prob
touch_down_3pct_prob
touch_down_5pct_prob
touch_down_8pct_prob
```

分成：

```text
low
mid
high
```

或使用分位数分桶：

```text
Q1
Q2
Q3
Q4
```

每组输出真实结果：

```text
sample_size
actual_touch_rate
actual_terminal_positive_rate
mean_terminal_return
median_terminal_return
p10_terminal_return
p90_terminal_return
actual_max_drawdown_median
actual_max_drawdown_p90
```

### 8.2 回撤风险分组

按：

```text
max_drawdown_p50
max_drawdown_p90
max_down_return_p10
max_down_return_p50
```

分组输出：

```text
sample_size
actual_max_drawdown_median
actual_max_drawdown_p90
actual_touch_down_5pct_rate
actual_touch_down_8pct_rate
mean_terminal_return
median_terminal_return
```

### 8.3 上行路径分组

按：

```text
max_up_return_p50
max_up_return_p90
touch_up_5pct_prob
positive_terminal_prob
```

分组输出：

```text
sample_size
actual_touch_up_5pct_rate
actual_touch_up_8pct_rate
actual_positive_terminal_rate
mean_terminal_return
median_terminal_return
```

### 8.4 状态路径分组

仅对 P2 输出：

```text
state_key
state_sample_size
fallback_used
```

按状态分组输出：

```text
sample_size
fallback_rate
actual_positive_terminal_rate
actual_touch_up_5pct_rate
actual_touch_down_5pct_rate
actual_max_drawdown_p90
```

P2 仍然只能作为辅助观察层，不作为主判断层。


---

## 9. 必须输出的回测指标

每个模型、每个 horizon 至少输出：

```text
sample_size
standard_sample_size
purged_sample_size
actual_positive_terminal_rate
mean_terminal_return
median_terminal_return
p10_terminal_return
p90_terminal_return

actual_touch_up_3pct_rate
actual_touch_up_5pct_rate
actual_touch_up_8pct_rate
actual_touch_down_3pct_rate
actual_touch_down_5pct_rate
actual_touch_down_8pct_rate

actual_max_up_return_mean
actual_max_up_return_median
actual_max_down_return_mean
actual_max_down_return_median
actual_max_drawdown_mean
actual_max_drawdown_median
actual_max_drawdown_p90

terminal_return_mae_vs_p50
terminal_return_rmse_vs_p50
terminal_p10_p90_coverage
max_up_p10_p90_coverage
max_down_p10_p90_coverage
drawdown_p10_p90_coverage

touch_up_3pct_brier
touch_up_5pct_brier
touch_up_8pct_brier
touch_down_3pct_brier
touch_down_5pct_brier
touch_down_8pct_brier
positive_terminal_brier

fallback_rate
avg_state_sample_size
model_coverage_rate
```


---

## 10. 观察条件有效性评估

V1.4 必须输出观察条件是否有区分度。

每个核心观察指标至少输出：

```text
bucket_count
high_bucket_sample_size
low_bucket_sample_size
high_vs_low_actual_return_delta
high_vs_low_actual_touch_delta
high_vs_low_drawdown_delta
monotonicity_score
calibration_error
conclusion
```

结论只能是观察级：

```text
useful_observation
neutral_observation
weak_observation
unstable_observation
insufficient_evidence
```

禁止输出：

```text
buy
sell
hold
increase_position
reduce_position
stop_loss
take_profit
target_price
```


---

## 11. P0/P1/P2 对比

V1.4 必须比较三个路径模型的历史观察价值。

至少输出：

```text
P1_vs_P0_terminal_coverage_delta
P1_vs_P0_touch_brier_delta
P1_vs_P0_drawdown_coverage_delta
P1_vs_P0_conclusion

P2_vs_P1_terminal_coverage_delta
P2_vs_P1_touch_brier_delta
P2_vs_P1_drawdown_coverage_delta
P2_vs_P1_fallback_rate_delta
P2_vs_P1_conclusion
```

结论只能是：

```text
P1 improves over P0
P1 is neutral versus P0
P1 underperforms P0
P2 improves over P1
P2 is neutral versus P1
P2 underperforms P1
insufficient evidence
```

P2 的结论必须附加说明：

```text
P2 is auxiliary only and must not be used as core decision dependency.
```


---

## 12. V1.4 质量门禁

新增：

```text
observation_backtest_quality
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

### 12.1 必须 FAIL 的情况

1. 出现交易信号字段；
2. 出现 buy/sell/position/stop_loss/take_profit 等字段；
3. 出现 NaN/inf；
4. 样本数为 0；
5. 缺少 P0/P1/P2 任一模型结果；
6. 缺少 5D/10D/20D 任一 horizon；
7. 未来函数检查失败；
8. purged 模式完全无法生成；
9. probability 不在 `[0, 1]`；
10. 分位数顺序错误；
11. 回撤指标方向错误且未解释；
12. 报告命名成 signal；
13. `is_trade_signal` 不是 false；
14. `forbidden_actions` 缺少 `formal_signal_generation`、`auto_order`、`broker_api`；
15. 出现目标价、止盈、止损、仓位建议字段。

### 12.2 可以 WARN 的情况

1. 某个 horizon 样本偏少；
2. 某个分组样本偏少；
3. P2 fallback_rate 偏高；
4. P2 未优于 P1；
5. 观察条件没有区分度；
6. Brier 表现较差；
7. 覆盖率明显偏离理论区间；
8. purged 样本数偏少；
9. 某些状态分组不足；
10. 某些指标只适合观察，不适合进入 V1.5。


---

## 13. 报告结构要求

新增 JSON：

```text
docs/data/latest_observation_backtest_report.json
```

建议结构：

```json
{
  "meta": {
    "system": "CNSV",
    "version": "1.4",
    "stage": "V1.4_observation_backtest",
    "report_type": "observation_backtest_report",
    "ts_code": "600150.SH",
    "name": "中国船舶",
    "generated_at": "...",
    "latest_trade_date": "...",
    "is_trade_signal": false
  },
  "cnsvdata_gate": {},
  "observation_backtest_quality": {},
  "backtest_scope": {
    "horizons": [5, 10, 20],
    "models": [
      "P0_historical_path_replay",
      "P1_volatility_adjusted_path",
      "P2_state_conditional_path"
    ],
    "standard_walk_forward": true,
    "purged_walk_forward": true,
    "backtest_type": "observation_only"
  },
  "model_backtest_metrics": {},
  "observation_bucket_metrics": {},
  "model_comparison": {},
  "observation_condition_quality": {},
  "observation_backtest_leakage_checks": {},
  "forbidden_actions": [
    "formal_signal_generation",
    "auto_order",
    "broker_api"
  ],
  "next_stage": "V1.5 human decision support"
}
```

新增 registry：

```text
docs/data/observation_backtest_registry.json
```

新增 MD 报告：

```text
reports/latest_observation_backtest_report.md
reports/archive/YYYY-MM-DD_observation_backtest_report.md
```

新增 HTML 页面：

```text
docs/backtest.html
```

并更新：

```text
docs/index.html
```

增加入口：

```text
Observation Backtest Report
```


---

## 14. Markdown 报告要求

`reports/latest_observation_backtest_report.md` 必须用中文说明：

1. 当前阶段是 V1.4；
2. 这是观察级回测，不是交易回测；
3. 使用的数据范围；
4. 回测 horizon；
5. 使用的路径模型 P0/P1/P2；
6. standard walk-forward 样本数；
7. purged walk-forward 样本数；
8. 触达概率分组结果；
9. 下穿概率分组结果；
10. 回撤风险分组结果；
11. 上行路径分组结果；
12. P0/P1/P2 对比；
13. 哪些观察条件有参考价值；
14. 哪些观察条件证据不足；
15. 哪些观察条件风险较高；
16. P2 是否只能作为辅助；
17. 是否允许进入 V1.5；
18. 明确声明：这不是交易信号，不构成买卖建议。


---

## 15. HTML 页面要求

新增：

```text
docs/backtest.html
```

页面至少展示：

```text
V1.4 阶段说明
observation_backtest_quality
standard vs purged 样本数
P0/P1/P2 总览
5D/10D/20D 回测指标
触达概率分组表
下穿概率分组表
回撤风险分组表
模型对比表
观察条件有效性表
禁止交易信号声明
```

更新：

```text
docs/index.html
```

新增入口：

```text
Observation Backtest Report
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

## 16. 建议新增文件结构

请根据仓库实际结构实现，可微调路径，但职责要清晰。

```text
src/cnsv/backtest/__init__.py
src/cnsv/backtest/observation_backtest.py
src/cnsv/backtest/backtest_metrics.py
src/cnsv/backtest/bucket_analysis.py
src/cnsv/backtest/model_comparison.py
src/cnsv/backtest/backtest_evaluator.py
src/cnsv/backtest/backtest_report.py
src/cnsv/backtest/backtest_registry.py
src/cnsv/backtest/leakage_checks.py
```

新增 CLI：

```text
src/cnsv/cli/run_observation_backtest.py
```

新增测试：

```text
tests/test_observation_backtest.py
tests/test_backtest_metrics.py
tests/test_bucket_analysis.py
tests/test_model_comparison.py
tests/test_backtest_evaluator.py
tests/test_backtest_report.py
tests/test_backtest_registry.py
tests/test_observation_backtest_cli.py
```

新增 workflow：

```text
.github/workflows/run_observation_backtest.yml
```


---

## 17. CLI 命令要求

新增命令：

```bash
python -m cnsv.cli.run_observation_backtest
```

该命令必须：

1. 读取 CNSVdata gate；
2. 确认 V1.3 path distribution / path validation 产物存在；
3. 构造 observation backtest；
4. 执行 leakage checks；
5. 执行 quality checks；
6. 生成 JSON；
7. 生成 registry；
8. 生成 MD；
9. 生成 HTML；
10. 更新 docs/index.html；
11. 写入 archive。


---

## 18. GitHub Actions 要求

新增：

```text
.github/workflows/run_observation_backtest.yml
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
```

提交产物：

```text
docs/data/latest_observation_backtest_report.json
docs/data/observation_backtest_registry.json
reports/latest_observation_backtest_report.md
reports/archive/*_observation_backtest_report.md
docs/backtest.html
docs/index.html
```

不要破坏现有 workflow：

```text
check_data.yml
run_features.yml
run_baseline_models.yml
run_baseline_validation.yml
run_path_distribution.yml
```


---

## 19. 测试要求

必须新增并跑通测试。

### 19.1 观察级回测 row 构造测试

构造 mock path prediction 和 truth window。

断言：

```text
as_of_date 正确
horizon 正确
model_id 正确
actual_terminal_return 正确
actual_touch_up_5pct 正确
actual_touch_down_5pct 正确
actual_max_drawdown 正确
```

### 19.2 防未来函数测试

断言：

```text
max_prediction_input_date <= as_of_date
truth_start_date > as_of_date
truth_end_date = as_of_date + horizon
```

### 19.3 分组测试

构造固定 observation metric。

断言：

```text
low/mid/high 或 Q1/Q2/Q3/Q4 分组正确
每组 sample_size 正确
high_vs_low_delta 正确
```

### 19.4 Brier 测试

断言：

```text
touch_up_5pct_brier 计算正确
touch_down_5pct_brier 计算正确
positive_terminal_brier 计算正确
```

### 19.5 模型对比测试

构造 P0/P1/P2 mock metrics。

断言：

```text
P1_vs_P0 delta 正确
P2_vs_P1 delta 正确
conclusion 合法
```

### 19.6 禁止交易字段测试

如果报告出现：

```text
buy_signal
sell_signal
target_position
stop_loss
take_profit
formal_signal
target_price
```

必须 FAIL。

### 19.7 CLI 测试

执行：

```bash
python -m cnsv.cli.run_observation_backtest
```

断言生成：

```text
docs/data/latest_observation_backtest_report.json
docs/data/observation_backtest_registry.json
reports/latest_observation_backtest_report.md
docs/backtest.html
docs/index.html
```


---

## 20. 自检命令

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
```

不允许只改代码不跑测试。


---

## 21. 最终输出要求

完成后请给我简洁说明，必须包含：

1. 修改了哪些文件；
2. 是否新增 V1.4 观察级回测层；
3. 是否仍然严格禁止交易信号；
4. 是否生成 observation backtest JSON；
5. 是否生成 observation backtest MD；
6. 是否生成 backtest.html；
7. 是否更新 index.html；
8. 是否覆盖 P0/P1/P2；
9. 是否覆盖 5D/10D/20D；
10. standard walk-forward 样本数；
11. purged walk-forward 样本数；
12. 触达概率分组是否完成；
13. 下穿概率分组是否完成；
14. 回撤风险分组是否完成；
15. P1 是否优于 P0；
16. P2 是否优于 P1；
17. 哪些观察条件有参考价值；
18. 哪些观察条件证据不足；
19. leakage checks 结果；
20. pytest 结果；
21. run_observation_backtest 结果；
22. 最新报告路径；
23. 是否可以进入 V1.5。


---

## 22. V1.4 验收标准

V1.4 通过条件：

1. `pytest` 通过；
2. `run_observation_backtest` 通过；
3. `latest_observation_backtest_report.json` 正常生成；
4. `observation_backtest_quality.status` 不得为 FAIL；
5. P0/P1/P2 均有结果；
6. 5D/10D/20D 全覆盖；
7. standard walk-forward 有样本；
8. purged walk-forward 有样本；
9. 触达概率分组完成；
10. 下穿概率分组完成；
11. 回撤风险分组完成；
12. P0/P1/P2 对比完成；
13. 观察条件有效性评估完成；
14. 防未来函数检查 PASS；
15. 无 NaN/inf；
16. 概率均在 `[0, 1]`；
17. 无交易信号字段；
18. `is_trade_signal = false`；
19. `forbidden_actions` 包含 `formal_signal_generation`、`auto_order`、`broker_api`；
20. `docs/backtest.html` 存在；
21. `docs/index.html` 有 backtest 入口；
22. README 或开发文档说明 V1.4；
23. `next_stage = V1.5 human decision support`。


---

## 23. V1.4 与 V1.5 的边界

V1.4 只负责历史观察证据。

V1.5 才允许开发：

```text
人工决策辅助层
观察条件整合
人工关注点
风险等级摘要
模型一致性说明
决策前检查清单
```

但 V1.5 仍然不允许自动交易，不允许连接券商，不允许输出正式下单动作。


---

## 24. 核心原则

V1.3 解决的是：

```text
未来路径可能怎么走。
```

V1.4 要解决的是：

```text
这些路径判断在历史上有没有参考价值。
```

V1.4 最重要的专业判断：

```text
观察级回测不是交易回测。
历史表现不是未来承诺。
高触达概率不是买入理由。
高下穿概率不是止损指令。
回撤分布是风险观察，不是交易命令。
V1.4 的任务是为 V1.5 人工决策辅助层提供证据。
```

只有 V1.4 通过后，才允许进入 V1.5 human decision support。
