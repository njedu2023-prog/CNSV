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
    h1 { font-size: 40px; margin: 0; letter-spacing: 0; line-height: 1.08; font-weight: 700; }
    .subtitle { max-width: 760px; margin: 14px auto 0; color: var(--muted); font-size: 19px; line-height: 1.42; }
    h2 { font-size: 26px; margin: 0 0 18px; line-height: 1.18; font-weight: 700; }
    h3 { font-size: 18px; margin: 0; }
    section { background: var(--surface); border-radius: 22px; padding: 28px; margin: 18px 0; overflow: hidden; box-shadow: var(--shadow); }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr)); gap: 14px; }
    .metric { border: 1px solid rgba(210, 210, 215, .8); border-radius: 18px; padding: 18px; background: var(--surface-soft); min-height: 104px; display: flex; flex-direction: column; justify-content: space-between; }
    .label { color: var(--muted); font-size: 14px; line-height: 1.35; font-weight: 500; }
    .value { font-size: 24px; font-weight: 700; margin-top: 12px; overflow-wrap: anywhere; line-height: 1.15; letter-spacing: 0; }
    .ok { color: var(--green); }
    .warn { color: var(--amber); }
    .bad { color: var(--red); }
    details { border: 1px solid rgba(210, 210, 215, .9); border-radius: 18px; background: var(--surface-soft); margin: 14px 0; overflow: hidden; }
    summary { cursor: pointer; list-style: none; padding: 18px 20px; display: flex; align-items: center; justify-content: space-between; gap: 18px; }
    summary::-webkit-details-marker { display: none; }
    summary::after { content: "Show more"; color: var(--blue); font-size: 15px; white-space: nowrap; font-weight: 600; }
    details[open] summary::after { content: "Show less"; }
    .summary-main { min-width: 0; }
    .summary-title { font-size: 24px; font-weight: 700; margin-bottom: 12px; line-height: 1.18; }
    .chips { display: flex; flex-wrap: wrap; gap: 10px; }
    .chip { border: 1px solid var(--line); background: #fff; border-radius: 999px; padding: 7px 12px; color: #424245; font-size: 14px; overflow-wrap: anywhere; }
    table { width: 100%; border-collapse: collapse; font-size: 15px; background: #fff; }
    th, td { text-align: left; border-top: 1px solid #e8e8ed; padding: 12px 16px; vertical-align: top; }
    th { color: var(--muted); font-weight: 600; width: 46%; }
    ul { margin: 0; padding-left: 20px; }
    li { margin: 8px 0; }
    .notice { color: var(--muted); }
    @media (max-width: 640px) {
      main { padding: 22px 14px 36px; }
      .hero { text-align: left; padding: 10px 0 18px; }
      h1 { font-size: 30px; }
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
    <p class="subtitle">接线阶段只展示 data readiness、基础摘要和禁止动作，不生成正式 buy/sell signal。</p>
  </header>
  <section><h2>Data Gate</h2><div id="gate" class="grid"></div></section>
  <section><h2>Data Overview</h2><div id="summary" class="grid"></div></section>
  <section><h2>Feature Summary</h2><div id="features"></div></section>
  <section><h2>Validation</h2><div id="validation"></div></section>
  <section><h2>Restricted Actions</h2><div id="forbidden"></div></section>
</main>
<script>
const yesNo = value => value ? "Yes" : "No";
const statusText = value => ({PASS: "PASS", WARN: "WARN", FAIL: "FAIL"}[value] || value || "");
const actionName = value => ({formal_signal_generation: "Formal signal generation", auto_order: "Auto order", broker_api: "Broker API"}[value] || value);
const strengthName = value => ({positive: "Positive", negative: "Negative", neutral: "Neutral"}[value] || value);
const checkName = value => ({
  daily_non_empty: "daily 非空",
  one_min_non_empty: "1min 非空",
  moneyflow_non_empty: "moneyflow 非空",
  daily_core_fields: "daily core fields",
  one_min_core_fields: "1min core fields",
  moneyflow_core_fields: "moneyflow core fields",
  latest_trade_date_daily_vs_1min: "daily vs 1min trade date",
  latest_trade_date_daily_vs_moneyflow: "daily vs moneyflow trade date",
  daily_close_vs_1min_latest_close: "daily close vs 1min latest close"
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
      metric("CNSVdata ready", gate.ready, gate.ready ? "ok" : "bad"),
      metric("Gate status", statusText(gate.status), gate.status === "PASS" ? "ok" : gate.status === "WARN" ? "warn" : "bad"),
      metric("Continue allowed", gate.can_continue, gate.can_continue ? "ok" : "bad"),
      metric("Backtest prep", gate.can_run_backtest),
      metric("moneyflow strong factor", gate.can_use_moneyflow_as_strong_factor),
      metric("Formal signal", false, "bad")
    ].join("");
    document.getElementById("summary").innerHTML = [
      metric("Symbol", `${data.meta?.ts_code || ""} ${data.meta?.name || ""}`),
      metric("Report type", "Data status"),
      metric("Latest trade date", manifest.latest_trade_date),
      metric("Snapshot ID", manifest.snapshot_id),
      metric("daily rows", loaded.daily_rows),
      metric("1min rows", loaded.one_min_rows),
      metric("moneyflow rows", loaded.moneyflow_rows),
      metric("File count", manifest.file_count)
    ].join("");
    document.getElementById("features").innerHTML = [
      fold("Price & Volume", [["Close", f.price_volume?.latest_close], ["Pct chg", f.price_volume?.latest_pct_chg], ["MA20", f.price_volume?.ma20]], [["Latest close", f.price_volume?.latest_close], ["Latest pct chg", f.price_volume?.latest_pct_chg], ["MA5", f.price_volume?.ma5], ["MA10", f.price_volume?.ma10], ["MA20", f.price_volume?.ma20], ["1D return", f.price_volume?.ret_1d], ["5D return", f.price_volume?.ret_5d], ["20D return", f.price_volume?.ret_20d], ["5D volume ratio", f.price_volume?.volume_ratio_5d], ["5D amount ratio", f.price_volume?.amount_ratio_5d]]),
      fold("1min Structure", [["Intraday high", f.minute_structure?.latest_intraday_high], ["Intraday low", f.minute_structure?.latest_intraday_low], ["Latest", f.minute_structure?.latest_intraday_close]], [["Intraday high", f.minute_structure?.latest_intraday_high], ["Intraday low", f.minute_structure?.latest_intraday_low], ["Intraday latest", f.minute_structure?.latest_intraday_close], ["Intraday range", f.minute_structure?.intraday_range_pct], ["Close position", f.minute_structure?.close_position_in_day_range], ["Last 30min return", f.minute_structure?.last_30min_return], ["Last 60min return", f.minute_structure?.last_60min_return], ["Intraday volume", f.minute_structure?.intraday_volume_sum], ["Intraday amount", f.minute_structure?.intraday_amount_sum]]),
      fold("moneyflow", [["Net inflow", f.moneyflow?.net_mf_amount], ["Strength", strengthName(f.moneyflow?.moneyflow_strength_basic)], ["Strong factor", f.moneyflow?.can_use_as_strong_factor]], [["Net inflow", f.moneyflow?.net_mf_amount], ["Main force available", f.moneyflow?.main_force_available], ["moneyflow trade date", f.moneyflow?.moneyflow_latest_trade_date], ["moneyflow lag days", f.moneyflow?.moneyflow_lag_days], ["Basic strength", strengthName(f.moneyflow?.moneyflow_strength_basic)], ["Strong factor", f.moneyflow?.can_use_as_strong_factor], ["moneyflow note", f.moneyflow?.moneyflow_warning]])
    ].join("");
    document.getElementById("validation").innerHTML = [
      metric("Validation status", statusText(validation.status), validation.status === "PASS" ? "ok" : validation.status === "WARN" ? "warn" : "bad"),
      metric("FAIL count", validation.failed_count),
      metric("WARN count", validation.warn_count)
    ].join("") + `<details><summary><div class="summary-main"><div class="summary-title">Validation details</div><div class="chips"><span class="chip">${(validation.checks || []).length} checks</span></div></div></summary><table><tbody>${(validation.checks || []).map(item => `<tr><th>${checkName(item.name)}</th><td>${statusText(item.status)}</td><td>${detailText(item.detail)}</td></tr>`).join("")}</tbody></table></details>`;
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
