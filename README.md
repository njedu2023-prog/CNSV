# CNSV

CNSV 是中国船舶 `600150.SH` 实盘人工量化波段系统的主程序仓库。

## V1.1 当前阶段

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
```

报告输出：

```text
docs/data/latest_data_report.json
docs/data/latest_feature_report.json
docs/data/feature_registry.json
reports/latest_data_report.md
reports/latest_feature_report.md
reports/archive/YYYY-MM-DD_data_report.md
reports/archive/YYYY-MM-DD_feature_report.md
docs/index.html
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
