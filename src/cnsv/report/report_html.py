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
    :root { color-scheme: light; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; }
    body { margin: 0; background: #f5f7fa; color: #18212f; }
    main { max-width: 1120px; margin: 0 auto; padding: 28px 18px 42px; }
    h1 { font-size: 28px; margin: 0 0 8px; letter-spacing: 0; }
    .subtitle { margin: 0 0 20px; color: #5f6b7a; }
    h2 { font-size: 18px; margin: 0 0 12px; }
    section { background: #fff; border: 1px solid #d8dee8; border-radius: 8px; padding: 16px; margin: 14px 0; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 10px; }
    .metric { border: 1px solid #e3e7ee; border-radius: 6px; padding: 10px; background: #fbfcfe; min-height: 62px; }
    .label { color: #5f6b7a; font-size: 12px; }
    .value { font-size: 18px; font-weight: 650; margin-top: 4px; overflow-wrap: anywhere; }
    .ok { color: #0f7a45; }
    .warn { color: #9a6700; }
    .bad { color: #b42318; }
    table { width: 100%; border-collapse: collapse; font-size: 14px; }
    th, td { text-align: left; border-bottom: 1px solid #e3e7ee; padding: 9px 6px; vertical-align: top; }
    th { color: #5f6b7a; font-weight: 600; }
    ul { margin: 0; padding-left: 20px; }
    .notice { color: #5f6b7a; }
  </style>
</head>
<body>
<main>
  <h1>CNSV 中国船舶数据状态报告</h1>
  <p class="subtitle">主程序 V1.0 接线阶段：只展示数据准入、基础摘要和禁止动作，不生成正式买卖信号。</p>
  <section><h2>数据门禁</h2><div id="gate" class="grid"></div></section>
  <section><h2>数据概览</h2><div id="summary" class="grid"></div></section>
  <section><h2>基础特征摘要</h2><div id="features"></div></section>
  <section><h2>数据校验</h2><div id="validation"></div></section>
  <section><h2>禁止动作</h2><div id="forbidden"></div></section>
</main>
<script>
const yesNo = value => value ? "是" : "否";
const statusText = value => ({PASS: "通过", WARN: "警告", FAIL: "失败"}[value] || value || "");
const actionName = value => ({formal_signal_generation: "正式买卖信号生成", auto_order: "自动下单", broker_api: "券商接口连接"}[value] || value);
const fmt = value => {
  if (value === null || value === undefined || value === "") return "-";
  if (typeof value === "number") return Number.isInteger(value) ? String(value) : value.toFixed(4);
  if (typeof value === "boolean") return yesNo(value);
  return String(value);
};
function metric(label, value, tone = "") {
  return `<div class="metric"><div class="label">${label}</div><div class="value ${tone}">${fmt(value)}</div></div>`;
}
function table(title, rows) {
  return `<h3>${title}</h3><table><tbody>${rows.map(([k, v]) => `<tr><th>${k}</th><td>${fmt(v)}</td></tr>`).join("")}</tbody></table>`;
}
fetch("data/latest_data_report.json")
  .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
  .then(data => {
    const gate = data.cnsvdata_gate || {}, manifest = data.data_manifest || {}, loaded = data.loaded_data_summary || {}, validation = data.validation || {}, f = data.features || {};
    document.getElementById("gate").innerHTML = [
      metric("CNSVdata 是否就绪", gate.ready, gate.ready ? "ok" : "bad"),
      metric("门禁状态", statusText(gate.status), gate.status === "PASS" ? "ok" : gate.status === "WARN" ? "warn" : "bad"),
      metric("是否允许继续", gate.can_continue, gate.can_continue ? "ok" : "bad"),
      metric("是否允许回测准备", gate.can_run_backtest),
      metric("是否允许 moneyflow 强因子", gate.can_use_moneyflow_as_strong_factor),
      metric("是否允许正式信号", false, "bad")
    ].join("");
    document.getElementById("summary").innerHTML = [
      metric("标的", `${data.meta?.ts_code || ""} ${data.meta?.name || ""}`),
      metric("报告类型", "数据状态报告"),
      metric("数据最新交易日", manifest.latest_trade_date),
      metric("数据快照", manifest.snapshot_id),
      metric("日线行数", loaded.daily_rows),
      metric("1分钟行数", loaded.one_min_rows),
      metric("资金流行数", loaded.moneyflow_rows),
      metric("文件数量", manifest.file_count)
    ].join("");
    document.getElementById("features").innerHTML = [
      table("量价摘要", [["最新收盘价", f.price_volume?.latest_close], ["最新涨跌幅", f.price_volume?.latest_pct_chg], ["5日均线", f.price_volume?.ma5], ["10日均线", f.price_volume?.ma10], ["20日均线", f.price_volume?.ma20], ["1日收益", f.price_volume?.ret_1d], ["5日收益", f.price_volume?.ret_5d], ["20日收益", f.price_volume?.ret_20d], ["5日成交量比", f.price_volume?.volume_ratio_5d], ["5日成交额比", f.price_volume?.amount_ratio_5d]]),
      table("分钟结构摘要", [["日内最高价", f.minute_structure?.latest_intraday_high], ["日内最低价", f.minute_structure?.latest_intraday_low], ["日内最新价", f.minute_structure?.latest_intraday_close], ["日内振幅", f.minute_structure?.intraday_range_pct], ["收盘位置", f.minute_structure?.close_position_in_day_range], ["最近30分钟收益", f.minute_structure?.last_30min_return], ["最近60分钟收益", f.minute_structure?.last_60min_return], ["日内成交量合计", f.minute_structure?.intraday_volume_sum], ["日内成交额合计", f.minute_structure?.intraday_amount_sum]]),
      table("资金流摘要", [["净流入金额", f.moneyflow?.net_mf_amount], ["主力资金是否可用", f.moneyflow?.main_force_available], ["资金流最新交易日", f.moneyflow?.moneyflow_latest_trade_date], ["资金流滞后天数", f.moneyflow?.moneyflow_lag_days], ["基础强弱", f.moneyflow?.moneyflow_strength_basic], ["是否可作强因子", f.moneyflow?.can_use_as_strong_factor], ["资金流提示", f.moneyflow?.moneyflow_warning]])
    ].join("");
    document.getElementById("validation").innerHTML = [metric("校验状态", statusText(validation.status), validation.status === "PASS" ? "ok" : validation.status === "WARN" ? "warn" : "bad"), metric("失败项数量", validation.failed_count), metric("警告项数量", validation.warn_count)].join("") + `<table><tbody>${(validation.checks || []).map(item => `<tr><th>${item.name}</th><td>${statusText(item.status)}</td><td>${item.detail || ""}</td></tr>`).join("")}</tbody></table>`;
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
