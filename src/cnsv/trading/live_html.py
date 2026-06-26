from __future__ import annotations

from pathlib import Path
from typing import Any

from cnsv.utils.io import ensure_parent


def write_live_trading_html(payload: dict[str, Any], path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(build_live_trading_html(payload), encoding="utf-8")
    return target


def build_live_trading_html(payload: dict[str, Any] | None = None) -> str:
    return """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>CNSV V3.0 交易决策系统</title>
  <style>
    :root{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Microsoft YaHei",sans-serif;color:#1d1d1f;background:#f5f5f7;--line:#d2d2d7;--muted:#6e6e73;--blue:#06c;--green:#0b8f45;--red:#d70015;--shadow:0 16px 40px rgba(0,0,0,.07)}*{box-sizing:border-box}body{margin:0;background:#f5f5f7}.topbar{position:fixed;top:0;left:0;right:0;z-index:20;background:rgba(0,0,0,.88);backdrop-filter:saturate(180%) blur(18px);border-bottom:1px solid rgba(255,255,255,.16)}.topnav{display:flex;gap:2px;overflow-x:auto;white-space:nowrap;justify-content:center;padding:9px 18px}.topnav a{color:#fff;text-decoration:none;font-size:12px;line-height:1.2;padding:4px 10px;border-radius:999px;opacity:.78}.topnav a:hover,.topnav a.active{opacity:1}.topnav a.active{font-weight:600;background:rgba(255,255,255,.12)}main{width:min(1180px,100%);margin:auto;padding:52px 18px 28px}.hero{display:grid;align-items:center;text-align:center;padding:16px 0 20px}.eyebrow{color:var(--red);font-size:12px;font-weight:700;letter-spacing:.08em}h1{font-size:30px;margin:5px 0 8px}.decision{background:#fff;border-radius:22px;box-shadow:var(--shadow);padding:18px;margin-top:16px}.signal{font-size:56px;line-height:.92;font-weight:800;letter-spacing:0}.buy{color:var(--red)}.sell,.blocked{color:var(--green)}.watch{color:#1d1d1f}.decision-text{font-size:18px;font-weight:700;margin-top:8px}.hero-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin-top:14px}.timeline-table{width:100%;border-collapse:separate;border-spacing:0;margin-top:12px;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fbfbfd;text-align:left}.timeline-table th,.timeline-table td{padding:8px 10px;border-bottom:1px solid var(--line);font-size:12px}.timeline-table tr:last-child th,.timeline-table tr:last-child td{border-bottom:0}.timeline-table th{color:var(--muted);font-weight:500;width:36%}.timeline-table td{font-weight:700;color:#1d1d1f}.metric{border:1px solid var(--line);border-radius:14px;background:#fbfbfd;padding:10px;text-align:left}.label{color:var(--muted);font-size:12px}.value{font-size:17px;font-weight:700;margin-top:4px}section{background:#fff;border-radius:18px;box-shadow:var(--shadow);padding:16px;margin:12px 0}h2{font-size:16px;margin:0 0 10px}h3{font-size:13px;margin:0 0 6px;color:#1d1d1f}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px}.three-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.note{color:var(--muted);font-size:12px;line-height:1.45;margin:8px 0 0}.pill{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:6px 10px;margin:3px;background:#fbfbfd;font-size:12px}.pill strong{margin-left:6px}.footer{color:var(--muted);font-size:12px;text-align:center;padding:12px}.error{color:var(--red);font-weight:700}@media(max-width:760px){.topnav{justify-content:flex-start}.hero{padding:12px 0 16px}main{padding:50px 12px 24px}h1{font-size:24px}.signal{font-size:44px}.hero-grid{grid-template-columns:1fr 1fr}.three-grid{grid-template-columns:1fr}.decision{padding:14px}.value{font-size:16px}}
  </style>
</head>
<body>
<div class="topbar"><nav class="topnav" aria-label="CNSV 全量菜单"><a href="trading.html" class="active">交易决策</a><a href="data.html">数据状态</a><a href="features.html">核心特征</a><a href="baseline.html">基准模型</a><a href="validation.html">基准验证</a><a href="path.html">路径分布</a><a href="backtest.html">观察回测</a><a href="decision_support.html">人工辅助</a><a href="risk.html">风控解释</a><a href="live.html">人工确认</a></nav></div>
<main>
  <div class="hero">
    <div>
      <div class="eyebrow">CNSV V3.0 交易决策系统</div>
      <h1>中国船舶 600150.SH</h1>
      <div class="decision">
        <div class="label">今日决策</div>
        <table class="timeline-table" aria-label="交易决策日期表"><tbody>
          <tr><th>信号生成日</th><td data-field="timeline.signal_date">加载中</td><th>预测日</th><td data-field="timeline.prediction_date">加载中</td></tr>
          <tr><th>验证日</th><td data-field="timeline.verify_date">加载中</td><th>数据交易日</th><td data-field="timeline.data_trade_date">加载中</td></tr>
        </tbody></table>
        <div id="signal" class="signal watch">LOADING</div>
        <div id="decisionText" class="decision-text">读取最新交易决策数据</div>
        <table class="timeline-table" aria-label="收盘数据表"><tbody>
          <tr><th>收盘数据日</th><td data-field="market.latest_trade_date">加载中</td><th>最新收盘价</th><td data-field="market.latest_close">加载中</td></tr>
          <tr><th>收盘涨跌幅</th><td data-field="market.latest_pct_chg">加载中</td><th>成交额</th><td data-field="market.latest_amount_yi">加载中</td></tr>
          <tr><th>MA20</th><td data-field="market.ma20">加载中</td><th>MA5</th><td data-field="market.ma5">加载中</td></tr>
        </tbody></table>
        <div class="hero-grid">
          <div class="metric"><div class="label">建议仓位</div><div class="value" data-field="decision.position_range">加载中</div></div>
          <div class="metric"><div class="label">次日上涨概率</div><div class="value" data-field="probability.prob_up_1d">加载中</div></div>
          <div class="metric"><div class="label">历史方向准确率</div><div class="value" data-field="validation.directional_accuracy">加载中</div></div>
          <div class="metric"><div class="label">实盘方向准确率</div><div class="value" data-field="live.direction_accuracy">加载中</div></div>
          <div class="metric"><div class="label">风险调整 EV</div><div class="value" data-field="ev.risk_adjusted_ev">加载中</div></div>
          <div class="metric"><div class="label">风险等级</div><div class="value" data-field="risk.risk_level_cn">加载中</div></div>
        </div>
      </div>
    </div>
  </div>
  <section><h2>5D / 10D / 20D 价格预测分布</h2><div class="grid"><div id="priceDistribution">加载中</div></div><p class="note">来自 V1.3 路径分布层的 P2 状态条件路径；只展示价格分布参考，不代表确定收益。</p></section>
  <section><h2>概率判断</h2><table class="timeline-table" aria-label="概率判断表"><tbody>
    <tr><th>明天上涨概率</th><td data-field="probability.prob_up_1d">加载中</td><th>明天下跌概率</th><td data-field="probability.prob_down_1d">加载中</td></tr>
    <tr><th>大涨概率</th><td data-field="dist.gt_5pct">加载中</td><th>大跌概率</th><td data-field="dist.lt_minus_5pct">加载中</td></tr>
  </tbody></table></section>
  <section><h2>EV 与性价比</h2><div class="grid">
    <div class="metric"><div class="label">原始 EV</div><div class="value" data-field="ev.raw_ev">加载中</div></div>
    <div class="metric"><div class="label">成本调整 EV</div><div class="value" data-field="ev.cost_adjusted_ev">加载中</div></div>
    <div class="metric"><div class="label">风险调整 EV</div><div class="value" data-field="ev.risk_adjusted_ev">加载中</div></div>
    <div class="metric"><div class="label">交易性价比</div><div class="value" data-field="ev.ev_rating_cn">加载中</div></div>
  </div><p class="note">EV 为长期重复同类交易时的期望收益，单次交易仍可能亏损。</p></section>
  <section><h2>风控状态</h2><div class="grid">
    <div class="metric"><div class="label">当前风险</div><div class="value" data-field="risk.risk_level_cn">加载中</div></div>
    <div class="metric"><div class="label">风控状态</div><div class="value" data-field="risk.status">加载中</div></div>
    <div class="metric"><div class="label">主要风险</div><div class="value" data-field="risk.reasons">加载中</div></div>
  </div><p class="note" data-field="risk.human_risk_explanation">加载中</p></section>
  <section><h2>仓位与退出</h2><div class="grid">
    <div class="metric"><div class="label">建议仓位</div><div class="value" data-field="decision.position_range">加载中</div><p class="note">不建议满仓，不建议加杠杆。</p></div>
    <div class="metric"><div class="label">止盈参考</div><div class="value" data-field="exit.take_profit_range">加载中</div></div>
    <div class="metric"><div class="label">止损参考</div><div class="value" data-field="exit.stop_loss_reference">加载中</div></div>
    <div class="metric"><div class="label">时间退出</div><div class="value" data-field="exit.time_exit_days">加载中</div></div>
  </div></section>
  <section><h2>模型表现追踪</h2><div class="three-grid">
    <div class="metric"><div class="label">历史统计线</div><div class="value" data-field="historical.direction_accuracy">加载中</div><p class="note" data-field="historical.sample_count">加载中</p><p class="note">历史验证 / walk-forward / purged</p></div>
    <div class="metric"><div class="label">实盘统计线</div><div class="value" data-field="live.direction_accuracy">加载中</div><p class="note" data-field="live.summary">加载中</p><p class="note" data-field="live.correct_wrong">加载中</p></div>
    <div class="metric"><div class="label">历史验证补充</div><div class="value" data-field="validation.b2">加载中</div><p class="note" data-field="validation.sample">加载中</p><p class="note" data-field="validation.path">加载中</p></div>
  </div></section>
  <section><h2>人工执行说明</h2><span class="pill">自动下单 <strong>关闭</strong></span><span class="pill">券商接口 <strong>关闭</strong></span><span class="pill">人工参考 <strong>是</strong></span><p class="note" data-field="human.execution_note">加载中</p></section>
  <div class="footer" id="footer">加载最新交易决策数据</div>
</main>
<script>
const DATA_URL = "data/latest_trading_decision_report.json";
const pick = (obj, path, fallback = null) => path.split(".").reduce((cur, key) => cur && cur[key] !== undefined ? cur[key] : undefined, obj) ?? fallback;
const fmtNumber = (value, digits = 4) => value === null || value === undefined || Number.isNaN(Number(value)) ? "N/A" : Number(value).toFixed(digits);
const fmtPct = (value) => value === null || value === undefined || Number.isNaN(Number(value)) ? "N/A" : `${(Number(value) * 100).toFixed(2)}%`;
const fmtPctPoints = (value) => value === null || value === undefined || Number.isNaN(Number(value)) ? "N/A" : `${Number(value).toFixed(2)}%`;
const fmtAmountYi = (value) => value === null || value === undefined || Number.isNaN(Number(value)) ? "N/A" : `${(Number(value) / 100000).toFixed(2)} 亿`;
const fmtCount = (value) => value === null || value === undefined || Number.isNaN(Number(value)) ? "--" : String(Number(value).toFixed(0));
const signalClass = (signal) => ["BUY","STRONG_BUY"].includes(signal) ? "buy" : ["SELL","STRONG_SELL","REDUCE"].includes(signal) ? "sell" : signal === "BLOCKED" ? "blocked" : "watch";
const setText = (field, value) => document.querySelectorAll(`[data-field="${field}"]`).forEach((el) => { el.textContent = value ?? "N/A"; });
const priceTable = (label, node = {}) => `<div><h3>${label} 预测分布</h3><table class="timeline-table" aria-label="${label} 价格预测分布表"><tbody><tr><th>P10</th><td>${fmtNumber(node.terminal_price_p10)}</td><th>P50</th><td>${fmtNumber(node.terminal_price_p50)}</td></tr><tr><th>P90</th><td>${fmtNumber(node.terminal_price_p90)}</td><th>期末上涨概率</th><td>${fmtPct(node.positive_terminal_prob)}</td></tr><tr><th>样本数</th><td>${fmtCount(node.sample_size)}</td><th>模型层</th><td>P2</td></tr></tbody></table></div>`;
function render(payload) {
  const decision = payload.decision || {}, probability = payload.probability || {}, dist = payload.return_distribution || {}, bins = dist.return_bins_1d || {}, ev = payload.ev || {}, risk = payload.risk || {}, exitPlan = payload.exit || {}, timeline = payload.decision_timeline || {}, market = payload.market_snapshot || {}, performance = payload.model_performance || {}, historicalStats = performance.historical_stats || {}, liveStats = performance.live_stats || {}, historical = payload.historical_validation || {}, b2Std = pick(historical, "baseline_directional_accuracy.standard", {}), b2Purged = pick(historical, "baseline_directional_accuracy.purged", {}), p2Std = pick(historical, "path_probability_validation.standard", {}), pricePaths = payload.price_prediction_distribution || {};
  const signal = decision.signal || "N/A";
  const signalNode = document.getElementById("signal");
  signalNode.className = `signal ${signalClass(signal)}`;
  signalNode.textContent = signal;
  document.getElementById("decisionText").textContent = `${decision.signal_cn || "N/A"} · ${decision.suggested_action || "N/A"}`;
  setText("timeline.signal_date", timeline.signal_date || "N/A"); setText("timeline.prediction_date", timeline.prediction_date || "N/A"); setText("timeline.verify_date", timeline.verify_date || "N/A"); setText("timeline.data_trade_date", timeline.data_trade_date || payload.trade_date || "N/A");
  setText("market.latest_trade_date", market.latest_trade_date || timeline.data_trade_date || payload.trade_date || "N/A"); setText("market.latest_close", fmtNumber(market.latest_close)); setText("market.latest_pct_chg", fmtPctPoints(market.latest_pct_chg)); setText("market.latest_amount_yi", fmtAmountYi(market.latest_amount)); setText("market.ma20", fmtNumber(market.ma20)); setText("market.ma5", fmtNumber(market.ma5));
  setText("decision.position_range", decision.position_range || "N/A"); setText("probability.prob_up_1d", fmtPct(probability.prob_up_1d)); setText("probability.prob_down_1d", fmtPct(probability.prob_down_1d)); setText("validation.directional_accuracy", fmtPct(b2Std.directional_accuracy)); setText("live.direction_accuracy", liveStats.sample_count ? fmtPct(liveStats.direction_accuracy) : "暂无样本");
  setText("ev.raw_ev", fmtPct(ev.raw_ev)); setText("ev.cost_adjusted_ev", fmtPct(ev.cost_adjusted_ev)); setText("ev.risk_adjusted_ev", fmtPct(ev.risk_adjusted_ev)); setText("ev.ev_rating_cn", ev.ev_rating_cn || "N/A"); setText("dist.gt_5pct", fmtPct(bins.gt_5pct)); setText("dist.lt_minus_5pct", fmtPct(bins.lt_minus_5pct));
  setText("risk.risk_level_cn", risk.risk_level_cn || "N/A"); setText("risk.status", risk.buy_blocked ? "已拦截" : "通过"); setText("risk.reasons", (risk.buy_block_reasons || risk.warnings || ["无硬拦截"]).join("；")); setText("risk.human_risk_explanation", risk.human_risk_explanation || "");
  setText("exit.take_profit_range", exitPlan.take_profit_range || "N/A"); setText("exit.stop_loss_reference", exitPlan.stop_loss_reference || "N/A"); setText("exit.time_exit_days", exitPlan.time_exit_days === undefined ? "N/A" : `${exitPlan.time_exit_days} 个交易日`);
  setText("historical.direction_accuracy", fmtPct(historicalStats.direction_accuracy)); setText("historical.sample_count", `样本数：${fmtCount(historicalStats.sample_count)}`); setText("live.summary", `起始：${liveStats.start_date || "2026-06-21"} · 样本：${liveStats.sample_count || 0}`); setText("live.correct_wrong", `正确：${liveStats.correct_count || 0} · 错误：${liveStats.wrong_count || 0}`);
  setText("validation.b2", `B2 5D ${fmtPct(b2Std.directional_accuracy)}`); setText("validation.sample", `standard：${fmtCount(b2Std.sample_size)} · purged：${fmtPct(b2Purged.directional_accuracy)}`); setText("validation.path", `P2 覆盖：${fmtPct(p2Std.terminal_p10_p90_coverage)} · Brier：${fmtNumber(p2Std.positive_terminal_brier)}`); setText("human.execution_note", pick(payload, "human_explanation.execution_note", ""));
  document.getElementById("priceDistribution").outerHTML = ["5D", "10D", "20D"].map((h) => priceTable(h, pricePaths[h])).join("");
  document.getElementById("footer").textContent = `生成时间：${payload.generated_at || "N/A"} · 数据日期：${payload.trade_date || "N/A"} · 数据源：${DATA_URL}`;
}
fetch(`${DATA_URL}?t=${Date.now()}`, {cache: "no-store"}).then((response) => { if (!response.ok) throw new Error(`HTTP ${response.status}`); return response.json(); }).then(render).catch((err) => { document.getElementById("signal").className = "signal blocked"; document.getElementById("signal").textContent = "DATA ERROR"; document.getElementById("decisionText").innerHTML = `<span class="error">无法读取最新交易决策 JSON：${err.message}</span>`; document.getElementById("footer").textContent = `数据读取失败：${DATA_URL}`; });
</script>
</body>
</html>"""
