from __future__ import annotations

from pathlib import Path

from cnsv.utils.io import ensure_parent

HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CNSV V1.2.2 Baseline Validation</title>
  <style>
    :root{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Microsoft YaHei",sans-serif;--page:#f5f5f7;--surface:#fff;--line:#d2d2d7;--text:#1d1d1f;--muted:#6e6e73;--blue:#0066cc;--green:#0aa846;--red:#e30000;--amber:#b26a00;--shadow:0 18px 44px rgba(0,0,0,.06)}
    *{box-sizing:border-box} body{margin:0;background:var(--page);color:var(--text)} main{width:min(100%,1180px);margin:auto;padding:38px 24px 48px} header{text-align:center;padding:18px 0 28px}.eyebrow{color:var(--blue);font-size:13px;font-weight:700;letter-spacing:.08em;margin:0 0 8px} h1{font-size:18px;margin:0}.subtitle{color:var(--muted);font-size:13px;margin:12px auto 0;max-width:780px;line-height:1.45} nav{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:16px} nav a{border:1px solid var(--line);border-radius:999px;color:var(--blue);text-decoration:none;padding:6px 11px;font-size:12px;background:#fff} section{background:var(--surface);border-radius:20px;padding:22px 26px;margin:16px 0;box-shadow:var(--shadow);overflow:hidden} h2{font-size:14px;margin:0 0 14px}.chips{display:flex;flex-wrap:wrap;gap:8px}.chip{border:1px solid var(--line);border-radius:999px;background:#fff;padding:7px 11px;color:var(--muted);font-size:12px}.chip strong{color:var(--text);margin-left:6px}.ok{color:var(--green)!important;font-weight:700}.bad{color:var(--red)!important;font-weight:700}.warn{color:var(--amber)!important;font-weight:700}.table-wrap{overflow-x:auto} table{width:100%;border-collapse:collapse;min-width:760px;background:#fff;font-size:12px} th,td{border-top:1px solid #e8e8ed;text-align:left;padding:9px 10px;white-space:nowrap} th{color:var(--muted)} .footer{color:var(--muted);font-size:12px;text-align:center;padding:18px 0 4px}@media(max-width:640px){main{padding:22px 14px 36px}header{text-align:left}nav{justify-content:flex-start}section{border-radius:18px;padding:18px}}
  </style>
</head>
<body>
<main>
  <header>
    <p class="eyebrow">CNSV V1.2.2 BASELINE VALIDATION</p>
    <h1>中国船舶基准模型验证看板</h1>
    <p class="subtitle">使用 walk-forward 与 purged walk-forward 验证 B0/B1/B2/B3 的历史分布质量；本页不是交易信号，不提供买卖建议。</p>
    <nav><a href="index.html">特征看板</a><a href="baseline.html">基准模型</a><a href="data/latest_baseline_validation_report.json">JSON 数据</a></nav>
  </header>
  <section><h2>验证总览</h2><div id="overview" class="chips"></div></section>
  <section><h2>防未来函数与样本降重叠</h2><div id="leakage" class="chips"></div></section>
  <section><h2>Standard Walk-forward 指标</h2><div id="standard"></div></section>
  <section><h2>Purged Walk-forward 指标</h2><div id="purged"></div></section>
  <section><h2>B2 vs B1 对比</h2><div id="compare"></div></section>
  <section><h2>禁止动作与下一阶段</h2><div id="guardrails" class="chips"></div></section>
  <div id="footer" class="footer"></div>
</main>
<script>
const fmt=(v,k="")=>v===null||v===undefined?"N/A":typeof v==="number"?(k.includes("rate")||k.includes("coverage")||k.includes("accuracy")?`${(v*100).toFixed(2)}%`:v.toFixed(4)):v;
const tone=v=>v==="PASS"?"ok":v==="FAIL"?"bad":v==="WARN"?"warn":"";
const chip=(l,v,c=tone(v))=>`<span class="chip">${l}<strong class="${c}">${fmt(v)}</strong></span>`;
const table=rows=>`<div class="table-wrap"><table><thead><tr>${rows[0].map(h=>`<th>${h}</th>`).join("")}</tr></thead><tbody>${rows.slice(1).map(r=>`<tr>${r.map(v=>`<td>${v}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
function metricTable(metrics){const rows=[["模型","周期","样本","区间覆盖","Brier","方向准确率","p50 MAE","fallback"]]; for(const [m,hs] of Object.entries(metrics||{})){for(const [h,r] of Object.entries(hs||{})){rows.push([m,h,fmt(r.sample_size),fmt(r.p10_p90_interval_coverage,"coverage"),fmt(r.positive_prob_brier),fmt(r.directional_accuracy,"accuracy"),fmt(r.mae_median),fmt(r.fallback_rate,"rate")]);}} return table(rows);}
fetch("data/latest_baseline_validation_report.json").then(r=>r.json()).then(p=>{
 const q=p.validation_quality||{}, s=p.validation_scope||{}, l=p.leakage_checks||{};
 overview.innerHTML=[chip("版本",(p.meta||{}).version),chip("阶段",(p.meta||{}).stage),chip("状态",q.status),chip("FAIL",q.failed_count),chip("WARN",q.warn_count),chip("交易信号",(p.meta||{}).is_trade_signal?"YES":"NO",(p.meta||{}).is_trade_signal?"bad":"ok")].join("");
 leakage.innerHTML=[chip("状态",l.status),chip("检查次数",l.check_count),chip("validation_step",s.validation_step),chip("purged 模式",s.purged_sample_mode),chip("覆盖周期",(s.horizons||[]).join("/"))].join("");
 standard.innerHTML=metricTable((p.model_metrics||{}).standard_walk_forward_metrics);
 purged.innerHTML=metricTable((p.model_metrics||{}).purged_walk_forward_metrics);
 const cr=[["模式","周期","覆盖率差","Brier 差","Pinball 差","方向准确率差","结论"]]; for(const [mode,hs] of Object.entries(p.b2_vs_b1||{})){for(const [h,r] of Object.entries(hs||{})){cr.push([mode,h,fmt(r.B2_vs_B1_interval_coverage_delta),fmt(r.B2_vs_B1_brier_delta),fmt(r.B2_vs_B1_pinball_loss_delta),fmt(r.B2_vs_B1_directional_accuracy_delta),r.B2_vs_B1_conclusion]);}} compare.innerHTML=table(cr);
 guardrails.innerHTML=(p.forbidden_actions||[]).map(x=>chip("禁止",x)).concat([chip("下一阶段",p.next_stage)]).join("");
 footer.textContent=`generated_at: ${(p.meta||{}).generated_at||"N/A"}`;
}).catch(e=>{overview.innerHTML=`<span class="bad">加载失败：${e}</span>`});
</script>
</body>
</html>
"""


def write_baseline_validation_report_html(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(HTML, encoding="utf-8")
    return target
