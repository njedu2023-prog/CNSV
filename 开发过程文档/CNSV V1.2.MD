继续 CNSV 主程序仓库开发。

当前阶段：CNSV V1.2 基准模型层。

现状确认：

1. V1.0 数据接线层已完成。
2. V1.1 基础特征增强与资金流核心层已完成。
3. 当前 V1.2 文档已经更新到：
   `开发过程文档/CNSV 主程序 V1.2 基准模型层开发文档.MD`
4. 但现在 `Run CNSV Baseline Models` 工作流显示：
   `0 workflow runs / This workflow has no runs yet`
5. 所以 V1.2 目前不能算完成，必须继续开发并跑通验收。

请按 V1.2 文档继续完成基准模型层，重点不是再做特征层，而是完成 baseline models。

必须完成：

1. 实现 B0 随机游走 / 不变价格模型。
2. 实现 B1 历史无条件收益分布模型。
3. 实现 B2 状态分组历史收益分布模型。
4. 实现 B3 简单波动率调整模型。
5. 实现 baseline_runner。
6. 实现 baseline_evaluator。
7. 实现 baseline_registry。
8. 实现 baseline_schema。
9. 实现 baseline report 的 JSON / MD / HTML 输出。
10. 实现 CLI：
   `python -m cnsv.cli.run_baseline_models`
11. 确保 `.github/workflows/run_baseline_models.yml` 可以手动触发。
12. 跑通一次 `Run CNSV Baseline Models` workflow。
13. 生成并提交以下产物：
   - `docs/data/latest_baseline_model_report.json`
   - `docs/data/baseline_registry.json`
   - `reports/latest_baseline_model_report.md`
   - `docs/baseline.html`
   - 更新后的 `docs/index.html`

验收标准：

1. `pytest` 必须通过。
2. `python -m cnsv.cli.run_baseline_models` 必须可运行。
3. `Run CNSV Baseline Models` 必须至少成功运行一次。
4. `baseline_quality.status` 必须为 `PASS`。
5. `failed_count = 0`。
6. B0 / B1 / B2 / B3 必须全部有输出。
7. 5D / 10D / 20D 必须全部有输出。
8. `is_trade_signal = false`。
9. `can_generate_formal_signal = false`。
10. `forbidden_actions` 必须包含 `formal_signal_generation`。

严格禁止：

1. 不生成正式买卖信号。
2. 不输出买入/卖出建议。
3. 不输出目标仓位。
4. 不输出目标股数。
5. 不输出止损价/止盈价。
6. 不开发 20D 路径采样。
7. 不开发触碰概率。
8. 不开发目标先到概率。
9. 不开发正式回测引擎。
10. 不连接券商。
11. 不自动下单。
12. 不使用 `TUSHARE_TOKEN`。
13. 不绕过 CNSVdata。
14. 不把 baseline report 命名为 signal report。

完成后请按下面格式汇报：

一、修改文件清单  
二、新增文件清单  
三、删除文件清单，如无写“无”  
四、pytest 是否通过  
五、`python -m cnsv.cli.run_baseline_models` 是否可运行  
六、`Run CNSV Baseline Models` workflow 是否成功运行  
七、`latest_baseline_model_report.json` 是否生成  
八、`baseline_registry.json` 是否生成  
九、`latest_baseline_model_report.md` 是否生成  
十、`docs/baseline.html` 是否生成  
十一、B0/B1/B2/B3 是否全部输出  
十二、5D/10D/20D 是否全部输出  
十三、baseline_quality 当前状态  
十四、是否仍然禁止 formal_signal_generation  
十五、是否可以进入 V1.3  

最重要原则：

没有成功跑过 `Run CNSV Baseline Models`，没有生成 baseline 报告产物，就不能算 V1.2 完成。
