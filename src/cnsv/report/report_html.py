from __future__ import annotations

from pathlib import Path

from cnsv.utils.io import ensure_parent

HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CNSV 中国船舶数据状态报告</title>
  <style>
    :root {
      color-scheme: light;
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      --page: #f5f5f7;
      --surface: #ffffff;
      --surface-soft: #fbfbfd;
      --text: #1d1d1f;
      --muted: #6e6e73;
      --line: #d2d2d7;
      --blue: #0066cc;
      --green: #11845b;
      --red: #b42318;
      --amber: #9a6700;
      --shadow: 0 18px 44px rgba(0, 0, 0, 0.06);
    }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--page); color: var(--text); -webkit-font-smoothing: antialiased; }
    main { width: min(100%, 1120px); margin: 0 auto; padding: 44px 24px 56px; }
    .hero { text-align: center; padding: 24px 0 34px; }
    .eyebrow { margin: 0 0 8px; color: var(--blue); font-size: 13px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
    h1 { font-size: 14px; margin: 0; letter-spacing: 0; line-height: 1.25; font-weight: 700; }
    .subtitle { max-width: 760px; margin: 14px auto 0; color: var(--muted); font-size: 19px; line-height: 1.42; }
    h2 { font-size: 14px; margin: 0 0 18px; line-height: 1.25; font-weight: 700; }
    h3 { font-size: 18px; margin: 0; }
    section { background: var(--surface); border-radius: 22px; padding: 28px; margin: 18px 0; overflow: hidden; box-shadow: var(--shadow); }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr)); gap: 14px; }
    .metric { border: 1px solid rgba(210, 210, 215, .8); border-radius: 18px; padding: 18px; background: var(--surface-soft); min-height: 104px; display: flex; flex-direction: column; justify-content: space-between; }
    .label { color: var(--muted); font-size: 14px; line-height: 1.35; font-weight: 500; }
    .value { font-size: 14px; font-weight: 700; margin-top: 12px; overflow-wrap: anywhere; line-height: 1.25; letter-spacing: 0; }
    #gate .value { font-size: 12px; }
    .ok { color: var(--green); }
    .warn { color: var(--amber); }
    .bad { color: var(--red); }
    details { border: 1px solid rgba(210, 210, 215, .9); border-radius: 18px; background: var(--surface-soft); margin: 14px 0; overflow: hidden; }
    summary { cursor: pointer; list-style: none; padding: 18px 20px; display: flex; align-items: center; justify-content: space-between; gap: 18px; }
    summary::-webkit-details-marker { display: none; }
    summary::after { content: "展开"; color: var(--blue); font-size: 14px; white-space: nowrap; font-weight: 600; }
    details[open] summary::after { content: "收起"; }
    .summary-main { min-width: 0; }
    .summary-title { font-size: 14px; font-weight: 700; margin-bottom: 12px; line-height: 1.25; }
    .chips { display: flex; flex-wrap: wrap; gap: 10px; }
    .chip { border: 1px solid var(--line); background: #fff; border-radius: 999px; padding: 7px 12px; color: #424245; font-size: 14px; overflow-wrap: anywhere; }
    table { width: 100%; border-collapse: collapse; font-size: 12px; background: #fff; }
    th, td { text-align: left; border-top: 1px solid #e8e8ed; padding: 12px 16px; vertical-align: top; }
    th { color: var(--muted); font-weight: 600; width: 46%; }
    ul { margin: 0; padding-left: 20px; }
    li { margin: 8px 0; }
    .notice { color: var(--muted); }
    @media (max-width: 640px) {
      main { padding: 22px 14px 36px; }
      .hero { text-align: left; padding: 10px 0 18px; }
      h1 { font-size: 14px; }
      .subtitle { font-size: 17px; margin-left: 0; }
      section { border-radius: 18px; padding: 18px; }
      .metric { min-height: 92px; }
      summary { align-items: flex-start; padding: 16px; }
      th, td { display: block; width: 100%; padding: 8px 10px; }
      td { border-top: 0; padding-top: 0; }
    }
  </style>
</head>
<body>
<main>
  <header class="hero">
    <p class="eyebrow">CNSV V1.0 DATA REPORT</p>
    <h1>中国船舶数据状态报告</h1>
    <p class="subtitle">接线阶段只展示数据准入、基础摘要和禁止动作，不生成正式 buy/sell signal。</p>
  </header>
  <section><h2>数据门禁</h2><div id="gate" class="grid"></div></section>
  <section><h2>数据概览</h2><div id="summary" class="grid"></div></section>
  <section><h2>特征摘要</h2><div id="features"></div></section>
  <section><h2>数据校验</h2><div id="validation"></div></section>
  <section><h2>禁止动作</h2><div id="forbidden"></div></section>
</main>
<script>
const yesNo = value => value ? "YES" : "NO";
const statusText = value => ({PASS: "PASS", WARN: "WARN", FAIL: "FAIL"}[value] || value || "");
const actionName = value => ({formal_signal_generation: "正式信号生成", auto_order: "自动下单", broker_api: "Broker API"}[value] || value);
const strengthName = value => ({positive: "偏强", negative: "偏弱", neutral: "中性"}[value] || value);
const checkName = value => ({
  daily_non_empty: "daily 非空",
  one_min_non_empty: "1min 非空",
  moneyflow_non_empty: "moneyflow 非空",
  daily_core_fields: "daily 核心字段",
  one_min_core_fields: "1min 核心字段",
  moneyflow_core_fields: "moneyflow 核心字段",
  latest_trade_date_daily_vs_1min: "daily 与 1min 交易日一致",
  latest_trade_date_daily_vs_moneyflow: "daily 与 moneyflow 交易日一致",
  daily_close_vs_1min_latest_close: "daily close 与 1min 最新价一致"
}[value] || value);
const detailText = value => {
  if (!value) return "";
  return String(value)
    .replace("daily must not be empty", "日线数据不能为空")
    .replace("1min must not be empty", "1分钟数据不能为空")
    .replace("moneyflow must not be empty", "资金流数据不能为空")
    .replace("missing fields: []", "核心字段齐全")
    .replace("relative diff=", "相对差异=");
};
const fmt = value => {
  if (value === null || value === undefined || value === "") return "-";
  if (typeof value === "number") return Number.isInteger(value) ? String(value) : value.toFixed(4);
  if (typeof value === "boolean") return yesNo(value);
  return String(value);
};
function metric(label, value, tone = "") {
  return `<div class="metric"><div class="label">${label}</div><div class="value ${tone}">${fmt(value)}</div></div>`;
}
function rows(items) {
  return `<table><tbody>${items.map(([k, v]) => `<tr><th>${k}</th><td>${fmt(v)}</td></tr>`).join("")}</tbody></table>`;
}
function fold(title, chips, tableRows) {
  return `<details><summary><div class="summary-main"><div class="summary-title">${title}</div><div class="chips">${chips.map(([k, v]) => `<span class="chip">${k}：${fmt(v)}</span>`).join("")}</div></div></summary>${rows(tableRows)}</details>`;
}
fetch("data/latest_data_report.json")
  .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
  .then(data => {
    const gate = data.cnsvdata_gate || {}, manifest = data.data_manifest || {}, loaded = data.loaded_data_summary || {}, validation = data.validation || {}, f = data.features || {};
    document.getElementById("gate").innerHTML = [
      metric("CNSVdata 就绪", gate.ready, gate.ready ? "ok" : "bad"),
      metric("门禁状态", statusText(gate.status), gate.status === "PASS" ? "ok" : gate.status === "WARN" ? "warn" : "bad"),
      metric("允许继续", gate.can_continue, gate.can_continue ? "ok" : "bad"),
      metric("允许回测准备", gate.can_run_backtest),
      metric("允许 moneyflow 强因子", gate.can_use_moneyflow_as_strong_factor),
      metric("允许正式信号", false, "bad")
    ].join("");
    document.getElementById("summary").innerHTML = [
      metric("标的", `${data.meta?.ts_code || ""} ${data.meta?.name || ""}`),
      metric("报告类型", "数据状态报告"),
      metric("最新交易日", manifest.latest_trade_date),
      metric("Snapshot ID", manifest.snapshot_id),
      metric("daily 行数", loaded.daily_rows),
      metric("1min 行数", loaded.one_min_rows),
      metric("moneyflow 行数", loaded.moneyflow_rows),
      metric("文件数量", manifest.file_count)
    ].join("");
    document.getElementById("features").innerHTML = [
      fold("量价摘要", [["收盘价", f.price_volume?.latest_close], ["涨跌幅", f.price_volume?.latest_pct_chg], ["20日均线", f.price_volume?.ma20]], [["最新收盘价", f.price_volume?.latest_close], ["最新涨跌幅", f.price_volume?.latest_pct_chg], ["5日均线", f.price_volume?.ma5], ["10日均线", f.price_volume?.ma10], ["20日均线", f.price_volume?.ma20], ["1D 收益", f.price_volume?.ret_1d], ["5D 收益", f.price_volume?.ret_5d], ["20D 收益", f.price_volume?.ret_20d], ["5D 成交量比", f.price_volume?.volume_ratio_5d], ["5D 成交额比", f.price_volume?.amount_ratio_5d]]),
      fold("1min 结构", [["日内最高", f.minute_structure?.latest_intraday_high], ["日内最低", f.minute_structure?.latest_intraday_low], ["最新价", f.minute_structure?.latest_intraday_close]], [["日内最高", f.minute_structure?.latest_intraday_high], ["日内最低", f.minute_structure?.latest_intraday_low], ["日内最新价", f.minute_structure?.latest_intraday_close], ["日内振幅", f.minute_structure?.intraday_range_pct], ["收盘位置", f.minute_structure?.close_position_in_day_range], ["最近 30min 收益", f.minute_structure?.last_30min_return], ["最近 60min 收益", f.minute_structure?.last_60min_return], ["日内成交量", f.minute_structure?.intraday_volume_sum], ["日内成交额", f.minute_structure?.intraday_amount_sum]]),
      fold("moneyflow 摘要", [["净流入", f.moneyflow?.net_mf_amount], ["强弱", strengthName(f.moneyflow?.moneyflow_strength_basic)], ["强因子", f.moneyflow?.can_use_as_strong_factor]], [["净流入金额", f.moneyflow?.net_mf_amount], ["主力资金可用", f.moneyflow?.main_force_available], ["moneyflow 交易日", f.moneyflow?.moneyflow_latest_trade_date], ["moneyflow 滞后天数", f.moneyflow?.moneyflow_lag_days], ["基础强弱", strengthName(f.moneyflow?.moneyflow_strength_basic)], ["可作强因子", f.moneyflow?.can_use_as_strong_factor], ["moneyflow 提示", f.moneyflow?.moneyflow_warning]])
    ].join("");
    document.getElementById("validation").innerHTML = [
      metric("校验状态", statusText(validation.status), validation.status === "PASS" ? "ok" : validation.status === "WARN" ? "warn" : "bad"),
      metric("FAIL 数量", validation.failed_count),
      metric("WARN 数量", validation.warn_count)
    ].join("") + `<details><summary><div class="summary-main"><div class="summary-title">校验明细</div><div class="chips"><span class="chip">${(validation.checks || []).length} checks</span></div></div></summary><table><tbody>${(validation.checks || []).map(item => `<tr><th>${checkName(item.name)}</th><td>${statusText(item.status)}</td><td>${detailText(item.detail)}</td></tr>`).join("")}</tbody></table></details>`;
    document.getElementById("forbidden").innerHTML = `<ul>${(data.forbidden_actions || []).map(item => `<li>${actionName(item)}</li>`).join("")}</ul>`;
  })
  .catch(err => { document.getElementById("gate").innerHTML = `<p class="notice">无法读取数据报告：${err}</p>`; });
</script>
</body>
</html>
"""


def write_report_html(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(HTML, encoding="utf-8")
    return target
