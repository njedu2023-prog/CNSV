from __future__ import annotations

from pathlib import Path

from cnsv.utils.io import ensure_parent

HTML = """<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>CNSV V1.3 Path Dashboard</title>
  <style>
    :root{font-family:-apple-system,BlinkMacSystemFont,\"SF Pro Text\",\"PingFang SC\",\"Microsoft YaHei\",sans-serif;--page:#f5f5f7;--surface:#fff;--line:#d2d2d7;--text:#1d1d1f;--muted:#6e6e73;--blue:#0066cc;--green:#08a045;--red:#e30000;--amber:#b26a00;--shadow:0 18px 44px rgba(0,0,0,.06)}
    *{box-sizing:border-box} body{margin:0;background:var(--page);color:var(--text)} main{width:min(100%,1180px);margin:auto;padding:38px 24px 48px} header{text-align:center;padding:18px 0 28px}.eyebrow{color:var(--blue);font-size:13px;font-weight:700;letter-spacing:.08em;margin:0 0 8px} h1{font-size:18px;margin:0}.subtitle{color:var(--muted);font-size:13px;margin:12px auto 0;max-width:820px;line-height:1.45} nav{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:16px} nav a{border:1px solid var(--line);border-radius:999px;color:var(--blue);text-decoration:none;padding:6px 11px;font-size:12px;background:#fff} section{background:var(--surface);border-radius:20px;padding:22px 26px;margin:16px 0;box-shadow:var(--shadow);overflow:hidden} h2{font-size:14px;margin:0 0 14px}.chips{display:flex;flex-wrap:wrap;gap:8px}.chip{border:1px solid var(--line);border-radius:999px;background:#fff;padding:7px 11px;color:var(--muted);font-size:12px}.chip strong{color:var(--text);margin-left:6px}.ok{color:var(--green)!important;font-weight:700}.bad{color:var(--red)!important;font-weight:700}.warn{color:var(--amber)!important;font-weight:700}.table-wrap{overflow-x:auto} table{width:100%;border-collapse:collapse;min-width:900px;background:#fff;font-size:12px} th,td{border-top:1px solid #e8e8ed;text-align:left;padding:9px 10px;white-space:nowrap} th{color:var(--muted)} .footer{color:var(--muted);font-size:12px;text-align:center;padding:18px 0 4px}@media(max-width:640px){main{padding:22px 14px 36px}header{text-align:left}nav{justify-content:flex-start}section{border-radius:18px;padding:18px}}
  </style>
</head>
<body>
<main>
  <header>
    <p class=\"eyebrow\">CNSV V1.3 PATH DISTRIBUTION</p>
    <h1>中国船舶路径分布与路径验证看板</h1>
    <p class=\"subtitle\">展示 5D/10D/20D 的路径观察、触达概率与 walk-forward 验证。本页不是交易信号，不提供买卖建议、仓位、止盈止损。</p>
    <nav><a href=\"index.html\">特征看板</a><a href=\"baseline.html\">基准模型</a><a href=\"validation.html\">基准验证</a><a href=\"data/latest_path_distribution_report.json\">路径分布 JSON</a><a href=\"data/latest_path_validation_report.json\">路径验证 JSON</a></nav>
  </header>
  <section><h2>路径分布总览</h2><div id=\"overview\" class=\"chips\"></div></section>
  <section><h2>P0/P1/P2 路径分布</h2><div id=\"models\"></div></section>
  <section><h2>路径验证质量</h2><div id=\"validation\" class=\"chips\"></div></section>
  <section><h2>Standard Walk-forward</h2><div id=\"standard\"></div></section>
  <section><h2>Purged Walk-forward</h2><div id=\"purged\"></div></section>
  <section><h2>禁止动作与下一阶段</h2><div id=\"guardrails\" class=\"chips\"></div></section>
  <div id=\"footer\" class=\"footer\"></div>
</main>
<script>
const fmt=(v,k=\"\")=>v===null||v===undefined?\"N/A\":typeof v===\"number\"?(k.includes(\"prob\")||k.includes(\"coverage\")||k.includes(\"rate\")||k.includes(\"return\")||k.includes(\"drawdown\")?`${(v*100).toFixed(2)}%`:v.toFixed(4)):v;
const tone=v=>v===\"PASS\"?\"ok\":v===\"FAIL\"?\"bad\":v===\"WARN\"?\"warn\":\"\";
const chip=(l,v,c=tone(v))=>`<span class=\"chip\">${l}<strong class=\"${c}\">${fmt(v)}</strong></span>`;
const table=rows=>`<div class=\"table-wrap\"><table><thead><tr>${rows[0].map(h=>`<th>${h}</th>`).join(\"\")}</tr></thead><tbody>${rows.slice(1).map(r=>`<tr>${r.map(v=>`<td>${v}</td>`).join(\"\")}</tr>`).join(\"\")}</tbody></table></div>`;
function modelTable(p){const rows=[[\"模型\",\"周期\",\"路径数\",\"终点P50\",\"最高P90\",\"最低P10\",\"回撤P50\",\"+5%触达\",\"-5%下穿\",\"fallback\"]]; for(const [m,model] of Object.entries((p||{}).path_models||{})){for(const [h,r] of Object.entries(model.horizons||{})){rows.push([m,h,fmt(r.path_count),fmt(r.terminal_return_p50,\"return\"),fmt(r.max_up_return_p90,\"return\"),fmt(r.max_down_return_p10,\"return\"),fmt(r.max_drawdown_p50,\"drawdown\"),fmt(r.touch_up_5pct_prob,\"prob\"),fmt(r.touch_down_5pct_prob,\"prob\"),r.fallback_used?\"YES\":\"NO\"]);}} return table(rows);}
function validationTable(metrics){const rows=[[\"模型\",\"周期\",\"样本\",\"终点覆盖\",\"上行覆盖\",\"下行覆盖\",\"+5% Brier\",\"-5% Brier\",\"RMSE\",\"fallback\"]]; for(const [m,hs] of Object.entries(metrics||{})){for(const [h,r] of Object.entries(hs||{})){rows.push([m,h,fmt(r.sample_size),fmt(r.terminal_p10_p90_coverage,\"coverage\"),fmt(r.max_up_p10_p90_coverage,\"coverage\"),fmt(r.max_down_p10_p90_coverage,\"coverage\"),fmt(r.touch_up_5pct_brier),fmt(r.touch_down_5pct_brier),fmt(r.path_rmse_terminal),fmt(r.fallback_rate,\"rate\")]);}} return table(rows);}
Promise.all([fetch(\"data/latest_path_distribution_report.json\").then(r=>r.json()),fetch(\"data/latest_path_validation_report.json\").then(r=>r.json())]).then(([d,v])=>{
 const q=d.path_quality||{}, vq=v.path_validation_quality||{}, leak=v.path_leakage_checks||{};
 overview.innerHTML=[chip(\"版本\",(d.meta||{}).version),chip(\"阶段\",(d.meta||{}).stage),chip(\"path_quality\",q.status),chip(\"latest_trade_date\",(d.meta||{}).latest_trade_date),chip(\"交易信号\",(d.meta||{}).is_trade_signal?\"YES\":\"NO\",(d.meta||{}).is_trade_signal?\"bad\":\"ok\")].join(\"\");
 models.innerHTML=modelTable(d);
 validation.innerHTML=[chip(\"validation_quality\",vq.status),chip(\"FAIL\",vq.failed_count),chip(\"WARN\",vq.warn_count),chip(\"leakage\",leak.status),chip(\"检查次数\",leak.check_count),chip(\"purged\",leak.purged_sample_mode)].join(\"\");
 standard.innerHTML=validationTable(v.standard_walk_forward_metrics);
 purged.innerHTML=validationTable(v.purged_walk_forward_metrics);
 guardrails.innerHTML=(d.forbidden_actions||[]).map(x=>chip(\"禁止\",x)).concat([chip(\"下一阶段\",d.next_stage)]).join(\"\");
 footer.textContent=`distribution generated_at: ${(d.meta||{}).generated_at||\"N/A\"} | validation generated_at: ${(v.meta||{}).generated_at||\"N/A\"}`;
}).catch(e=>{overview.innerHTML=`<span class=\"bad\">加载失败：${e}</span>`});
</script>
</body>
</html>
"""


def write_path_report_html(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(HTML, encoding="utf-8")
    return target
