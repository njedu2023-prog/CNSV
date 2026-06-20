# CNSV V1.2.2 Baseline Validation Layer 开发口令

继续 CNSV 主程序仓库主线，不回退旧话题，不推倒重来。

仓库：

https://github.com/njedu2023-prog/CNSV

## 0. 当前状态

CNSV V1.2.1 已完成并通过验收。

当前已确认：

- B2_state_grouped_distribution 已修复，不再长期 `state_sample_size = 0`；
- 当前状态键为：`downtrend|normal_vol|mixed`；
- B2 在 5D / 10D / 20D 上的 `state_sample_size` 均为 105；
- `fallback_used = false`；
- `baseline_quality.status = PASS`；
- `is_trade_signal = false`；
- `can_generate_formal_signal = false`；
- `forbidden_actions` 仍包含 `formal_signal_generation`、`auto_order`、`broker_api`。

但是当前仍有两个专业化问题必须修正：

1. `latest_baseline_model_report.json` 里的 `meta.version` 仍是 `1.2.0`；
2. `baseline_registry` 里的 `stage` 仍是 `V1.2_baseline_model`；
3. `next_stage` 直接写成 `V1.3 20D path distribution`，但专业流程上，V1.3 前必须先做 V1.2.2 验证层。

本轮任务：

**完成 CNSV V1.2.2 —— Baseline Validation / Walk-forward 验证层。**

目标不是做交易信号，也不是做路径预测，而是验证 B0/B1/B2/B3 的历史分布预测质量，证明这些基准模型到底“值不值得信”。

---

# 一、先做 V1.2.1 元数据收口

请先修正 V1.2.1 的版本标记问题。

## 1. 报告 meta 版本

把当前基准模型报告 meta 中的版本明确改为：

```json
"version": "1.2.1"
```

## 2. 报告 stage

新增或同步 stage 字段：

```json
"stage": "V1.2.1_state_grouped_baseline_fix"
```

## 3. baseline_registry stage

`baseline_registry` 每个模型的 stage 同步更新为：

```json
"stage": "V1.2.1_state_grouped_baseline_fix"
```

## 4. README 文档说明

README 或相关开发文档中补充：

```text
V1.2.1 修复 B2 状态分组历史样本为 0 的问题。
B2 当前可真实使用 trend_state / volatility_state / flow_strength_basic 构成的历史同状态样本。
V1.2.1 仍然不是交易信号层。
```

## 5. next_stage 修正

不要直接写 V1.3，改为：

```text
V1.2.2 baseline validation / walk-forward validation
```

---

# 二、V1.2.2 核心目标

新增一个专业验证层，用 walk-forward 方法验证 B0/B1/B2/B3 在历史 5D / 10D / 20D 上的分布预测质量。

必须回答以下问题：

1. B2 是否真的优于 B1；
2. B3 波动率调整是否过度压缩区间；
3. B0/B1/B2/B3 的 p10/p50/p90 分布是否有历史覆盖能力；
4. positive_prob 是否有校准价值；
5. 是否存在未来函数；
6. 是否存在重叠样本污染；
7. 是否仍然严格不生成任何交易信号。

---

# 三、严禁事项

本轮是 V1.2.2 验证层，不是交易系统。

严禁：

1. 不生成买入信号；
2. 不生成卖出信号；
3. 不输出目标仓位；
4. 不输出目标股数；
5. 不输出止盈止损；
6. 不输出交易建议；
7. 不连接券商接口；
8. 不自动下单；
9. 不配置或使用 TUSHARE_TOKEN；
10. 不绕过 CNSVdata；
11. 不直接从 Tushare 拉数据；
12. 不开发正式交易回测；
13. 不开发 20D 路径抽样；
14. 不把 validation 报告命名成 signal；
15. 不把验证结果包装成实盘推荐。

V1.2.2 只能输出：

- 模型验证指标；
- 覆盖率；
- 校准度；
- 误差；
- fallback 统计；
- B2 vs B1 对比；
- 风险提示；
- 是否通过验证门禁。

---

# 四、建议新增文件

请根据仓库结构合理新增或调整文件。建议路径如下，若实际结构不同，以现有仓库为准。

```text
src/cnsv/validation/baseline_validation.py
src/cnsv/validation/walk_forward.py
src/cnsv/validation/metrics.py
src/cnsv/validation/leakage_checks.py

src/cnsv/cli/run_baseline_validation.py

tests/test_baseline_validation.py
tests/test_walk_forward_validation.py
tests/test_validation_metrics.py
tests/test_validation_leakage_checks.py
tests/test_baseline_validation_cli.py

docs/data/latest_baseline_validation_report.json
docs/data/baseline_validation_registry.json
reports/latest_baseline_validation_report.md
reports/archive/YYYY-MM-DD_baseline_validation_report.md
docs/validation.html

.github/workflows/run_baseline_validation.yml
```

不要破坏现有文件：

```text
src/cnsv/cli/run_baseline_models.py
docs/data/latest_baseline_model_report.json
reports/latest_baseline_model_report.md
docs/baseline.html
```

V1.2.2 是新增验证层，不是替换 V1.2.1 基准模型层。

---

# 五、Walk-forward 验证逻辑

必须严格模拟历史时点。

对每一个可验证交易日 T：

1. 只能使用 T 日及 T 日之前的数据；
2. 生成 B0/B1/B2/B3 对 5D / 10D / 20D 的预测分布；
3. 等到真实 T+5 / T+10 / T+20 收益出现后，对比验证；
4. 记录每个模型、每个 horizon 的预测值和真实值；
5. 汇总验证指标。

伪代码逻辑：

```text
for each as_of_date T:
    train_history = data[data.trade_date <= T]
    future_truth = data[data.trade_date > T]

    for horizon in [5, 10, 20]:
        if T+horizon 不存在:
            skip

        prediction = run_baseline_models_as_of(T, train_history)
        actual_return = close(T+horizon) / close(T) - 1

        save validation row:
            as_of_date
            horizon
            model_id
            p10_return
            p50_return
            p90_return
            positive_prob
            actual_return
            actual_positive
            state_key
            state_sample_size
            fallback_used
```

必须确保：

```text
不能用 T+1 之后的数据构造 T 日状态
不能用完整全样本分布验证历史 T 日
不能让 B1/B2/B3 在历史 T 日偷看未来收益
```

---

# 六、必须输出的验证指标

每个模型、每个 horizon 至少输出以下指标：

```text
sample_size
valid_prediction_count
actual_positive_rate
mean_actual_return
median_actual_return

p10_coverage
p90_coverage
p10_p90_interval_coverage
median_error
mean_error
mae_median
rmse_median

positive_prob_brier
directional_accuracy
pinball_loss_p10
pinball_loss_p50
pinball_loss_p90

fallback_rate
avg_state_sample_size
min_state_sample_size
state_coverage_rate
```

指标解释：

1. `p10_p90_interval_coverage`  
   检查真实收益是否落在 p10 到 p90 之间。理论上这是 80% 区间，实际覆盖率不能离谱。

2. `positive_prob_brier`  
   验证上涨概率是否有校准价值。

3. `pinball_loss`  
   验证分位数预测质量。

4. `directional_accuracy`  
   验证 p50 或 expected_return 的方向判断能力。

5. `fallback_rate`  
   验证 B2 是否经常回退。

---

# 七、验证门禁要求

新增 `baseline_validation_quality`。

必须包含：

```json
{
  "status": "PASS/WARN/FAIL",
  "failed_count": 0,
  "warn_count": 0,
  "blocking_error_count": 0,
  "checks": []
}
```

## 必须 FAIL 的情况

1. 出现交易信号字段；
2. 出现 buy/sell/position/stop_loss/take_profit 等字段；
3. 出现 NaN/inf；
4. walk-forward 使用了未来数据；
5. 验证样本数为 0；
6. B2 声称没有 fallback，但 state_sample_size 小于最低要求；
7. p10 > p50 或 p50 > p90；
8. 价格或收益分位数明显异常且没有解释；
9. validation 报告缺少 B0/B1/B2/B3 任一模型；
10. validation 结果覆盖不了 5D/10D/20D。

## 可以 WARN 的情况

1. 某个 horizon 样本偏少；
2. B2 fallback_rate 偏高；
3. B2 没有显著优于 B1；
4. p10-p90 覆盖率明显低于 70% 或高于 90%；
5. positive_prob_brier 表现差；
6. state_coverage_rate 偏低。

---

# 八、B2 vs B1 对比要求

V1.2.2 必须专门输出 B2 相对于 B1 的对比。

至少包括：

```text
B2_vs_B1_interval_coverage_delta
B2_vs_B1_brier_delta
B2_vs_B1_pinball_loss_delta
B2_vs_B1_directional_accuracy_delta
B2_vs_B1_median_error_delta
B2_vs_B1_conclusion
```

结论只能是观察级，例如：

```text
B2 shows improvement
B2 is neutral versus B1
B2 underperforms B1
insufficient evidence
```

禁止写成：

```text
可以买
应该买
卖出
加仓
减仓
目标价
止损
止盈
```

---

# 九、防未来函数与重叠样本污染

新增 leakage / purged 检查。

至少做到：

1. as_of_date T 的训练数据必须 <= T；
2. actual_return 只能来自 T+horizon；
3. 状态字段必须来自 T 日及以前；
4. 对 20D 这种长 horizon，验证报告中必须提示重叠样本问题；
5. 支持一个简单的 purged validation 模式：

```text
每次验证样本之间至少间隔 horizon 个交易日
```

输出中需要同时给出：

```text
standard_walk_forward_metrics
purged_walk_forward_metrics
```

如果暂时不做复杂 purging，也必须至少实现：

```text
purged_sample_mode = every_horizon_step
```

也就是 20D 验证时，每隔 20 个交易日取一个验证点，减少重叠污染。

---

# 十、报告要求

新增 JSON 报告：

```text
docs/data/latest_baseline_validation_report.json
```

结构建议：

```json
{
  "meta": {
    "system": "CNSV",
    "version": "1.2.2",
    "stage": "V1.2.2_baseline_validation",
    "report_type": "baseline_validation_report",
    "ts_code": "600150.SH",
    "name": "中国船舶",
    "generated_at": "...",
    "is_trade_signal": false
  },
  "validation_quality": {},
  "validation_scope": {
    "horizons": [5, 10, 20],
    "models": [
      "B0_random_walk",
      "B1_historical_distribution",
      "B2_state_grouped_distribution",
      "B3_volatility_adjusted"
    ],
    "walk_forward": true,
    "purged_walk_forward": true
  },
  "model_metrics": {},
  "b2_vs_b1": {},
  "leakage_checks": {},
  "forbidden_actions": [
    "formal_signal_generation",
    "auto_order",
    "broker_api"
  ],
  "next_stage": "V1.3 20D path distribution after validation acceptance"
}
```

新增 MD 报告：

```text
reports/latest_baseline_validation_report.md
```

必须用中文解释：

1. 验证范围；
2. walk-forward 方法；
3. 是否防未来函数；
4. B0/B1/B2/B3 各自表现；
5. B2 是否优于 B1；
6. B2 fallback 情况；
7. p10-p90 覆盖率；
8. positive_prob 校准情况；
9. 是否允许进入 V1.3；
10. 明确声明：这不是交易信号。

新增页面：

```text
docs/validation.html
```

并在：

```text
docs/index.html
```

增加 Validation Report 入口。

---

# 十一、测试要求

必须新增测试并跑通。

## 1. Walk-forward 不偷看未来

构造简单 mock 数据，确保 as_of_date T 的模型输入最大日期 <= T。

断言：

```text
max_training_date <= as_of_date
```

## 2. 分位数覆盖率计算正确

构造固定 p10/p90 和 actual_return。

断言：

```text
interval_coverage 计算正确
```

## 3. Brier 分数正确

构造 positive_prob 和 actual_positive。

断言：

```text
positive_prob_brier 计算正确
```

## 4. Pinball loss 正确

构造 quantile prediction 和 actual_return。

断言：

```text
pinball_loss 计算正确
```

## 5. B2 vs B1 对比正确

构造 B1/B2 mock metrics。

断言：

```text
delta 字段正确
conclusion 合理
```

## 6. 禁止交易字段

validation report 中如出现：

```text
buy_signal
sell_signal
target_position
stop_loss
take_profit
formal_signal
```

必须 FAIL。

## 7. CLI 全链路

执行：

```bash
python -m cnsv.cli.run_baseline_validation
```

断言生成：

```text
docs/data/latest_baseline_validation_report.json
reports/latest_baseline_validation_report.md
docs/validation.html
docs/index.html
```

---

# 十二、自检命令

完成后必须执行：

```bash
pip install -r requirements.txt
pytest
python -m cnsv.cli.run_baseline_models
python -m cnsv.cli.run_baseline_validation
```

如果已有 feature/data 命令，也一起确认：

```bash
python -m cnsv.cli.generate_data_report
python -m cnsv.cli.generate_feature_report
```

不能只改代码不跑测试。

---

# 十三、GitHub Actions

新增 workflow：

```text
.github/workflows/run_baseline_validation.yml
```

要求：

1. 安装依赖；
2. 运行 pytest；
3. 运行 baseline models；
4. 运行 baseline validation；
5. 提交以下产物：

```text
docs/data/latest_baseline_validation_report.json
docs/data/baseline_validation_registry.json
reports/latest_baseline_validation_report.md
reports/archive/*_baseline_validation_report.md
docs/validation.html
docs/index.html
```

不要破坏现有：

```text
check_data.yml
run_features.yml
run_baseline_models.yml
```

---

# 十四、最终输出要求

完成后请给我一个简洁说明，必须包括：

1. 修改了哪些文件；
2. V1.2.1 版本标记是否已修正；
3. 是否新增 V1.2.2 validation 层；
4. walk-forward 是否只使用历史数据；
5. 是否做了 purged / 降重叠验证；
6. B0/B1/B2/B3 各 horizon 样本数；
7. B2 是否优于 B1；
8. p10-p90 覆盖率是否合理；
9. positive_prob_brier 表现如何；
10. 是否仍然禁止交易信号；
11. pytest 结果；
12. run_baseline_models 结果；
13. run_baseline_validation 结果；
14. 最新报告路径。

---

# 十五、验收标准

本轮通过条件：

1. pytest 通过；
2. run_baseline_models 通过；
3. run_baseline_validation 通过；
4. latest_baseline_validation_report.json 正常生成；
5. validation_quality.status 不得为 FAIL；
6. 无未来函数；
7. 无交易信号字段；
8. B2 vs B1 有清晰对比；
9. docs/index.html 有 validation 入口；
10. README 或相关文档说明 V1.2.2；
11. next_stage 改为：V1.3 需在 V1.2.2 验证接受后再启动。

核心原则：

V1.2.1 解决“B2 能不能跑”。

V1.2.2 必须解决“B2 值不值得信”。

只有 V1.2.2 通过后，才允许进入 V1.3 20D path distribution。
