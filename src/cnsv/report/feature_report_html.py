from __future__ import annotations

from pathlib import Path

from cnsv.utils.io import ensure_parent

HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CNSV 中国船舶 V1.1 特征报告</title>
  <style>
    :root { color-scheme: light; font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; --page:#f5f5f7; --surface:#fff; --soft:#fbfbfd; --text:#1d1d1f; --muted:#6e6e73; --line:#d2d2d7; --blue:#0066cc; --green:#11c04e; --red:#f51505; --shadow:0 18px 44px rgba(0,0,0,.06); }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--page); color: var(--text); -webkit-font-smoothing: antialiased; }
    main { width: min(100%, 1120px); margin: 0 auto; padding: 44px 24px 56px; }
    header { text-align: center; padding: 24px 0 34px; }
    .eyebrow { color: var(--blue); font-size: 13px; font-weight: 700; letter-spacing: .08em; margin: 0 0 8px; }
    h1 { font-size: 14px; margin: 0; line-height: 1.25; }
    .subtitle { max-width: 760px; margin: 14px auto 0; color: var(--muted); font-size: 19px; line-height: 1.42; }
    section { background: var(--surface); border-radius: 22px; padding: 24px 28px; margin: 18px 0; box-shadow: var(--shadow); overflow: hidden; }
    h2 { font-size: 14px; margin: 0 0 14px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 230px), 1fr)); gap: 14px; }
    .strip { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
    .metric { border: 1px solid rgba(210,210,215,.8); border-radius: 18px; padding: 18px; background: var(--soft); min-height: 96px; }
    .strip .metric { min-height: 0; padding: 9px 12px; border-radius: 999px; flex: 0 1 auto; display: flex; align-items: center; gap: 8px; }
    .label { color: var(--muted); font-size: 14px; line-height: 1.35; }
    .value { font-size: 14px; font-weight: 700; margin-top: 12px; overflow-wrap: anywhere; line-height: 1.25; }
    .strip .label, .strip .value { font-size: 12px; margin: 0; line-height: 1.2; white-space: nowrap; }
    #gate .value { font-size: 12px; }
    .ok { color: var(--green); } .bad { color: var(--red); }
    details { border: 1px solid rgba(210,210,215,.9); border-radius: 18px; background: var(--soft); margin: 10px 0 0; overflow: hidden; }
    summary { cursor: pointer; list-style: none; padding: 12px 14px; display: flex; align-items: center; justify-content: space-between; gap: 12px; }
    summary::-webkit-details-marker { display: none; }
    summary::after { content: "+"; color: var(--blue); font-size: 18px; font-weight: 700; line-height: 1; margin-left: auto; flex: 0 0 auto; }
    details[open] summary::after { content: "-"; }
    .summary-title { font-size: 12px; color: var(--muted); font-weight: 500; margin-bottom: 8px; }
    .chips { display: flex; flex-wrap: wrap; gap: 10px; }
    .chip { border: 1px solid var(--line); background: #fff; border-radius: 999px; padding: 7px 12px; color: #424245; font-size: 14px; }
    summary .chip { font-size: 12px; line-height: 1.2; color: #424245; font-weight: 400; }
    .chip.positive { color: var(--red); font-weight: 700; }
    .chip.negative { color: var(--green); font-weight: 700; }
    table { width: 100%; border-collapse: collapse; font-size: 12px; background: #fff; }
    th, td { text-align: left; border-top: 1px solid #e8e8ed; padding: 12px 16px; vertical-align: top; }
    th { color: var(--muted); width: 46%; }
    @media (max-width: 640px) { main { padding: 22px 14px 36px; } header { text-align: left; padding: 10px 0 18px; } .subtitle { font-size: 17px; margin-left: 0; } section { border-radius: 18px; padding: 18px; } .strip { gap: 8px; } th, td { display: block; width: 100%; padding: 8px 10px; } td { border-top: 0; padding-top: 0; } }
  </style>
</head>
<body>
<main>
  <header>
    <p class="eyebrow">CNSV V1.1 FEATURE REPORT</p>
    <h1>中国船舶数据状态与特征报告</h1>
  </header>
  <section><h2>数据报告</h2><div id="dataReport" class="strip"></div></section>
  <section><h2>特征报告</h2><div id="featureMeta" class="strip"></div></section>
  <section><h2>门禁状态</h2><div id="gate" class="strip"></div></section>
  <section><h2>特征质量</h2><div id="quality" class="strip"></div><div id="qualityDetails"></div></section>
  <section><h2>资金流摘要</h2><div id="moneyflow"></div></section>
  <section><h2>趋势摘要</h2><div id="trend" class="strip"></div></section>
  <section><h2>波动率摘要</h2><div id="volatility" class="strip"></div></section>
</main>
<script>
const yesNo = value => value ? "YES" : "NO";
const statusText = value => ({PASS: "通过", WARN: "警告", FAIL: "失败"}[value] || value || "");
const reportTypeText = value => ({feature_report: "特征报告", data_report: "数据报告"}[value] || value);
const trendText = value => ({strong_uptrend: "强上行", uptrend: "上行", downtrend: "下行", range: "震荡", unknown: "未知"}[value] || value);
const volatilityText = value => ({high_vol: "高波动", low_vol: "低波动", normal_vol: "正常波动", unknown: "未知"}[value] || value);
const checkName = value => ({
  price_volume_non_empty: "量价特征非空",
  minute_structure_non_empty: "分钟结构特征非空",
  moneyflow_non_empty: "资金流特征非空",
  trend_non_empty: "趋势特征非空",
  volatility_non_empty: "波动率特征非空",
  "price_volume.latest_close": "量价.最新收盘价",
  "price_volume.latest_amount": "量价.最新成交额",
  "price_volume.ret_1d": "量价.1D 收益",
  "minute_structure.latest_intraday_close": "分钟结构.最新价",
  "minute_structure.intraday_range_pct": "分钟结构.日内振幅",
  "moneyflow.net_mf_amount": "资金流.净流入金额",
  "moneyflow.main_force_net": "资金流.主力净流入",
  "moneyflow.flow_strength_score": "资金流.强弱分",
  "trend.trend_state": "趋势.趋势状态",
  "volatility.volatility_state": "波动率.波动状态",
  moneyflow_strong_factor_gate: "资金流强因子门禁",
  daily_row_count: "daily 行数",
  one_min_row_count: "1min 行数",
  moneyflow_row_count: "moneyflow 行数",
  latest_trade_date_daily_vs_1min: "daily 与 1min 交易日一致",
  latest_trade_date_daily_vs_moneyflow: "daily 与 moneyflow 交易日一致"
}[value] || value);
const checkDetail = value => String(value || "")
  .replace("price_volume features must not be empty", "量价特征不能为空")
  .replace("minute_structure features must not be empty", "分钟结构特征不能为空")
  .replace("moneyflow features must not be empty", "资金流特征不能为空")
  .replace("trend features must not be empty", "趋势特征不能为空")
  .replace("volatility features must not be empty", "波动率特征不能为空")
  .replace(" is required", " 为必填项")
  .replace("moneyflow can be used as strong factor", "资金流允许作为强因子")
  .replace("daily rows must be >= 60", "daily 行数必须不少于 60")
  .replace("one_min rows must be >= 60", "1min 行数必须不少于 60")
  .replace("moneyflow rows must be >= 10", "moneyflow 行数必须不少于 10");
const fmt = value => {
  if (value === null || value === undefined || value === "") return "-";
  if (typeof value === "number") return Number.isInteger(value) ? String(value) : value.toFixed(4);
  if (typeof value === "boolean") return yesNo(value);
  return String(value);
};
const statusTone = value => value === "PASS" || value === true ? "ok" : value === "FAIL" || value === false ? "bad" : "";
const metric = (label, value, tone = "") => `<div class="metric"><div class="label">${label}</div><div class="value ${tone}">${fmt(value)}</div></div>`;
const rows = items => `<table><tbody>${items.map(([k,v]) => `<tr><th>${k}</th><td>${fmt(v)}</td></tr>`).join("")}</tbody></table>`;
const fold = (title, chips, tableRows) => `<details><summary><div><div class="summary-title">${title}</div><div class="chips">${chips.map(([k,v]) => `<span class="chip">${k}：${fmt(v)}</span>`).join("")}</div></div></summary>${rows(tableRows)}</details>`;
const signedTone = value => Number(value) > 0 ? "positive" : Number(value) < 0 ? "negative" : "";
const signedChip = (label, value) => `<span class="metric"><span class="label">${label}</span><span class="value">${fmt(value)}</span></span>`;
const moneyflowRows = data => Object.entries(data || {}).map(([key, value]) => [({
  net_mf_amount: "净流入金额",
  net_mf_ratio: "净流入占比",
  small_order_net: "小单净流入",
  medium_order_net: "中单净流入",
  large_order_net: "大单净流入",
  extra_large_order_net: "超大单净流入",
  main_force_net: "主力净流入",
  main_force_ratio: "主力净流入占比",
  main_force_available: "主力资金可用",
  moneyflow_latest_trade_date: "资金流交易日",
  moneyflow_lag_days: "资金流滞后天数",
  moneyflow_strength_basic: "资金流基础强弱",
  flow_strength_basic: "资金流基础强弱",
  flow_strength_score: "资金流强弱分",
  flow_continuity_3d: "3D 连续性",
  flow_continuity_5d: "5D 连续性",
  flow_continuity_10d: "10D 连续性",
  positive_flow_days_5d: "5D 净流入天数",
  positive_flow_days_10d: "10D 净流入天数",
  flow_reversal_1d: "1D 资金反转",
  flow_reversal_3d: "3D 资金反转",
  price_flow_confirm: "价量资金确认",
  price_flow_divergence: "价量资金背离",
  volume_flow_confirm: "量能资金确认",
  moneyflow_warning: "资金流提示",
  can_use_as_strong_factor: "可作强因子"
}[key] || key), value]);
Promise.all([
  fetch("data/latest_data_report.json").then(r => r.ok ? r.json() : null).catch(() => null),
  fetch("data/latest_feature_report.json").then(r => r.ok ? r.json() : null)
]).then(([dataReport, featureReport]) => {
  dataReport = dataReport || {};
  featureReport = featureReport || {};
  if (dataReport) {
    const s = dataReport.loaded_data_summary || {};
    document.getElementById("dataReport").innerHTML = [
      metric("数据状态", dataReport.validation?.status, statusTone(dataReport.validation?.status)),
      metric("最新交易日", s.latest_trade_date),
      metric("daily 行数", s.daily_rows),
      metric("1min 行数", s.one_min_rows),
      metric("moneyflow 行数", s.moneyflow_rows)
    ].join("");
  }
  const gate = featureReport.cnsvdata_gate || {};
  const q = featureReport.feature_quality || {};
  const f = featureReport.features || {};
  document.getElementById("featureMeta").innerHTML = [
    metric("报告类型", reportTypeText(featureReport.meta?.report_type)),
    metric("版本", featureReport.meta?.version),
    metric("标的", `${featureReport.meta?.ts_code || ""} ${featureReport.meta?.name || ""}`),
    metric("下一阶段", featureReport.next_stage)
  ].join("");
  document.getElementById("gate").innerHTML = [
    metric("CNSVdata 就绪", gate.ready, statusTone(gate.ready)),
    metric("门禁状态", gate.status, statusTone(gate.status)),
    metric("允许继续", gate.can_continue, statusTone(gate.can_continue)),
    metric("允许 moneyflow 强因子", gate.can_use_moneyflow_as_strong_factor, statusTone(gate.can_use_moneyflow_as_strong_factor)),
    metric("允许正式信号", false, "bad")
  ].join("");
  document.getElementById("quality").innerHTML = [
    metric("特征质量", q.status, statusTone(q.status)),
    metric("FAIL 数量", q.failed_count),
    metric("WARN 数量", q.warn_count)
  ].join("");
  document.getElementById("qualityDetails").innerHTML = fold("质量检查明细", [["检查项", (q.checks || []).length]], (q.checks || []).map(item => [checkName(item.name), `${statusText(item.status)} ${checkDetail(item.detail)}`]));
  document.getElementById("moneyflow").innerHTML = `<details><summary><div><div class="summary-title">资金流核心层</div><div class="strip">${signedChip("净流入", f.moneyflow?.net_mf_amount)}${signedChip("主力净流入", f.moneyflow?.main_force_net)}${signedChip("强弱分", f.moneyflow?.flow_strength_score)}</div></div></summary>${rows(moneyflowRows(f.moneyflow))}</details>`;
  document.getElementById("trend").innerHTML = [
    metric("趋势状态", trendText(f.trend?.trend_state)),
    metric("MA5-MA20", f.trend?.trend_ma5_ma20),
    metric("收盘在 MA20 上方", f.trend?.close_above_ma20)
  ].join("");
  document.getElementById("volatility").innerHTML = [
    metric("波动率状态", volatilityText(f.volatility?.volatility_state)),
    metric("20D 实现波动率", f.volatility?.realized_vol_20d),
    metric("ATR 14D", f.volatility?.atr_14d)
  ].join("");
}).catch(err => {
  document.getElementById("featureMeta").innerHTML = `<p>无法读取特征报告：${err}</p>`;
});
</script>
</body>
</html>
"""


def write_feature_report_html(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(HTML, encoding="utf-8")
    return target
