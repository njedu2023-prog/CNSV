# CNSV

CNSV 是中国船舶 `600150.SH` 实盘人工量化波段系统的主程序仓库。

## V3.0 当前系统

当前最高目标是预测中国船舶下一交易日官方收盘价相对本交易日官方收盘价的涨跌方向。

盘中实时链路由 CNSV 主程序直接调用 Tushare `rt_min_daily`，不再等待 CNSVdata 的盘中仓库提交。CNSVdata 继续提供历史日线、资金流、交易日历和历史分钟训练集，并在收盘后归档正式数据。

北京时间自动任务：

```text
上午 09:15、09:35、09:55、10:15、10:35、10:55、11:15、11:30
下午 13:00、13:20、13:40、14:00、14:20、14:40、15:00、15:10
终局 20:04
```

`09:15` 是盘前启动与健康检查。Tushare 连续竞价分钟线从 `09:30` 开始，因此 09:15 不生成或覆盖预测；从 09:35 起使用当日实时分钟数据滚动计算。GitHub Actions 使用仓库 Secret `TUSHARE_TOKEN`，令牌不得写入代码、配置、日志或报告。

## 历史 V1.3 阶段

V1.3 是路径分布层。V1.3 在 V1.2 基准终点分布与 V1.2.2 walk-forward 验证层之后，构建 5D/10D/20D 的观察级路径分布与路径验证。

V1.3 新增：

- `P0_historical_path_replay` 历史路径回放
- `P1_volatility_adjusted_path` 波动率调整路径回放
- `P2_state_conditional_path` 状态条件路径回放，样本不足时透明回退到 P1
- Path Quality 检查
- Path Validation / walk-forward 与 purged walk-forward 验证
- `latest_path_distribution_report.json`、`latest_path_validation_report.json`
- `path_distribution_registry.json`
- `latest_path_distribution_report.md`、`latest_path_validation_report.md`
- `docs/path.html` 路径分布与路径验证看板

V1.3 仍然不做：

- 不生成正式买卖信号
- 不输出买入/卖出建议
- 不输出目标仓位或目标股数
- 不输出止盈止损
- 不开发正式交易回测
- 不连接券商接口
- 不自动下单
- 不配置或使用 `TUSHARE_TOKEN`
- 不绕过 `CNSVdata`

下一阶段是 `V1.4 observation backtest after path validation acceptance`。

## V1.2 基准模型层

当前阶段是基准模型层。V1.2 在 V1.1 特征层基础上，构建透明、可解释、可测试的 5D/10D/20D 终端收益分布基准模型。

V1.2.1 修复 B2 状态分组历史样本为 0 的问题。B2 当前可真实使用 `trend_state` / `volatility_state` / `flow_strength_basic` 构成的历史同状态样本。V1.2.1 仍然不是交易信号层。

V1.2.2 新增 Baseline Validation / Walk-forward 验证层，用历史切片验证 B0/B1/B2/B3 的分布覆盖率、校准度、误差、fallback 统计和 B2 vs B1 对比。V1.3 需在 V1.2.2 验证接受后再启动。

V1.2 新增：

- `B0_random_walk` 随机游走基准
- `B1_historical_distribution` 历史分布基准
- `B2_state_grouped_distribution` 状态分组历史分布，样本不足时透明回退
- `B3_volatility_adjusted` 波动率调整历史分布
- Baseline Quality 检查
- Baseline Registry
- `latest_baseline_model_report.json`、`latest_baseline_model_report.md`
- `docs/baseline.html` 基准模型看板

V1.2 仍然不做：

- 不生成正式买卖信号
- 不输出买入/卖出建议
- 不输出目标仓位或目标股数
- 不输出止盈止损
- 不开发 20D 路径抽样或触达概率
- 不开发正式回测引擎
- 不连接券商接口
- 不自动下单
- 不配置或使用 `TUSHARE_TOKEN`
- 不绕过 `CNSVdata`

## V1.1 特征层

当前阶段是基础特征增强与资金流核心层。V1.1 在 V1.0 数据接线层已经跑通的基础上，构建稳定、可解释、可测试的基础特征层。

V1.1 新增：

- 增强量价特征、分钟结构特征、资金流特征
- 新增趋势特征和波动率特征
- 新增 Feature Quality 检查
- 新增 Feature Registry
- 新增 `latest_feature_report.json`、`latest_feature_report.md`
- 更新 `docs/index.html` 展示 Data Report 和 Feature Report

V1.1 仍然不做：

- 不生成正式买卖信号
- 不输出买入/卖出建议
- 不输出目标仓位或目标股数
- 不开发 20D 路径预测
- 不开发正式回测引擎
- 不连接券商接口
- 不自动下单
- 不配置或使用 `TUSHARE_TOKEN`
- 不绕过 `CNSVdata`

## V1.0 数据接线层

当前阶段是主程序接线开发。目标是安全读取上游 `njedu2023-prog/CNSVdata`，识别数据是否可用，生成数据状态报告，并严格禁止正式交易信号。

V1.0 只做：

- 读取 `metadata/downstream_ready.json`
- 读取 `metadata/data_manifest.json`
- 在 gate 通过后读取 processed parquet
- 校验基础数据可用性
- 构建基础量价、分钟结构、资金流摘要
- 生成 `latest_data_report.json`、`latest_data_report.md` 和 `docs/index.html`

V1.0 不做：

- 不直接拉取 Tushare
- 不配置或使用 `TUSHARE_TOKEN`
- 不绕过 CNSVdata
- 不连接券商接口
- 不自动下单
- 不生成正式买卖信号
- 不生成 high confidence signal
- 不把数据报告命名为 `latest_signal`

## 上游数据

默认读取路径：

```text
https://raw.githubusercontent.com/njedu2023-prog/CNSVdata/refs/heads/main
```

第一读取入口必须是：

```text
metadata/downstream_ready.json
```

Gate 规则：

- `ready=false`：阻断，不读取 parquet
- `status=FAIL`：阻断，不读取 parquet
- `status=WARN`：降级继续，只允许数据状态和观察级读取
- `status=PASS`：正常读取
- `can_generate_formal_signal=false`：始终禁止正式信号

## 本地命令

```bash
pip install -r requirements.txt
pytest
python -m cnsv.cli.check_data
python -m cnsv.cli.build_features
python -m cnsv.cli.generate_data_report
python -m cnsv.cli.generate_feature_report
python -m cnsv.cli.run_baseline_models
python -m cnsv.cli.run_baseline_validation
python -m cnsv.cli.run_path_distribution
python -m cnsv.cli.run_path_validation
```

报告输出：

```text
docs/data/latest_data_report.json
docs/data/latest_feature_report.json
docs/data/feature_registry.json
docs/data/latest_baseline_model_report.json
docs/data/baseline_registry.json
docs/data/latest_path_distribution_report.json
docs/data/latest_path_validation_report.json
docs/data/path_distribution_registry.json
reports/latest_data_report.md
reports/latest_feature_report.md
reports/latest_baseline_model_report.md
reports/latest_path_distribution_report.md
reports/latest_path_validation_report.md
reports/archive/YYYY-MM-DD_data_report.md
reports/archive/YYYY-MM-DD_feature_report.md
reports/archive/YYYY-MM-DD_baseline_model_report.md
reports/archive/YYYY-MM-DD_path_distribution_report.md
reports/archive/YYYY-MM-DD_path_validation_report.md
docs/index.html
docs/baseline.html
docs/path.html
```

## GitHub Actions

`.github/workflows/check_data.yml` 会执行：

```text
pip install -r requirements.txt
pytest
python -m cnsv.cli.generate_data_report
```

随后提交 `reports` 和 `docs` 的报告更新。

`.github/workflows/run_features.yml` 会执行：

```text
pip install -r requirements.txt
pytest
python -m cnsv.cli.generate_feature_report
```

随后提交 V1.1 Feature Report、Feature Registry 和 `docs/index.html`。

`.github/workflows/run_baseline_models.yml` 会执行：

```text
pip install -r requirements.txt
pytest
python -m cnsv.cli.run_baseline_models
```

随后提交 V1.2 Baseline Model Report、Baseline Registry 和 `docs/baseline.html`。

`.github/workflows/run_path_distribution.yml` 会执行：

```text
pip install -r requirements.txt
pytest
python -m cnsv.cli.run_baseline_models
python -m cnsv.cli.run_baseline_validation
python -m cnsv.cli.run_path_distribution
python -m cnsv.cli.run_path_validation
```

随后提交 V1.3 Path Distribution、Path Validation、Path Registry 和 `docs/path.html`。
