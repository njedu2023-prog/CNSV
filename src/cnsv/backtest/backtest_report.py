from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from cnsv.utils.io import ensure_parent


def write_observation_backtest_json(payload: dict[str, Any], path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return target


def write_observation_backtest_md(payload: dict[str, Any], path: str | Path, archive_dir: str | Path | None = None) -> Path:
    target = ensure_parent(path)
    text = build_observation_backtest_markdown(payload)
    target.write_text(text, encoding="utf-8")
    if archive_dir:
        archive = ensure_parent(Path(archive_dir) / f"{date.today().isoformat()}_observation_backtest_report.md")
        archive.write_text(text, encoding="utf-8")
    return target


def build_observation_backtest_markdown(payload: dict[str, Any]) -> str:
    q = payload.get("observation_backtest_quality", {})
    scope = payload.get("backtest_scope", {})
    lines = [
        "# CNSV V1.4 观察级回测报告",
        "",
        "本报告是观察级回测，不是交易回测；不生成交易信号，不构成买卖建议，不输出仓位、目标价、止盈或止损。",
        "",
        "## 阶段与范围",
        f"- 版本: {payload.get('meta', {}).get('version')}",
        f"- 阶段: {payload.get('meta', {}).get('stage')}",
        f"- latest_trade_date: {payload.get('meta', {}).get('latest_trade_date')}",
        f"- horizons: {scope.get('horizons')}",
        f"- models: {', '.join(scope.get('models', []))}",
        f"- standard walk-forward 样本数: {scope.get('standard_sample_size')}",
        f"- purged walk-forward 样本数: {scope.get('purged_sample_size')}",
        "",
        "## 质量门禁",
        f"- 状态: {q.get('status')}",
        f"- FAIL 数量: {q.get('failed_count')}",
        f"- WARN 数量: {q.get('warn_count')}",
        "",
        "## 模型指标总览",
    ]
    lines += _metric_lines(payload.get("model_backtest_metrics", {}).get("standard_walk_forward", {}))
    lines += ["", "## Purged Walk-forward"]
    lines += _metric_lines(payload.get("model_backtest_metrics", {}).get("purged_walk_forward", {}))
    lines += ["", "## 触达概率分组", "- 已完成 touch_up/touch_down 3%/5%/8% 的 low/mid/high 分组。"]
    lines += ["", "## 下穿概率分组", "- 已完成 touch_down 3%/5%/8% 的分组与真实下穿率统计。"]
    lines += ["", "## 回撤风险分组", "- 已完成 max_drawdown 与 max_down_return 分组。"]
    lines += ["", "## 上行路径分组", "- 已完成 max_up_return、touch_up_5pct_prob、positive_terminal_prob 分组。"]
    lines += ["", "## P0/P1/P2 对比"]
    for horizon, row in payload.get("model_comparison", {}).get("standard_walk_forward", {}).items():
        lines.append(f"- {horizon}: {row.get('P1_vs_P0_conclusion')}; {row.get('P2_vs_P1_conclusion')}; {row.get('P2_auxiliary_note')}")
    lines += ["", "## 观察条件有效性", *_condition_lines(payload.get("observation_condition_quality", {}))]
    leak = payload.get("observation_backtest_leakage_checks", {})
    lines += [
        "",
        "## 防未来函数",
        f"- 状态: {leak.get('status')}",
        f"- 检查次数: {leak.get('check_count')}",
        f"- purged_sample_mode: {leak.get('purged_sample_mode')}",
        "",
        "## 禁止动作",
        "- 正式交易信号: NO",
        "- 买入/卖出建议: NO",
        "- 目标仓位/目标股数: NO",
        "- 止盈止损/目标价: NO",
        f"- forbidden_actions: {', '.join(payload.get('forbidden_actions', []))}",
        "",
        "## 下一阶段",
        f"- {payload.get('next_stage')}",
    ]
    return "\n".join(lines) + "\n"


def write_observation_backtest_html(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(_HTML, encoding="utf-8")
    return target


def _metric_lines(metrics: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for model_id, horizons in metrics.items():
        lines += ["", f"### {model_id}"]
        for horizon, row in horizons.items():
            lines.append(
                f"- {horizon}: sample={row.get('sample_size')}, "
                f"positive={_pct(row.get('actual_positive_terminal_rate'))}, "
                f"mean_return={_pct(row.get('mean_terminal_return'))}, "
                f"+5%={_pct(row.get('actual_touch_up_5pct_rate'))}, "
                f"-5%={_pct(row.get('actual_touch_down_5pct_rate'))}, "
                f"drawdown_p90={_pct(row.get('actual_max_drawdown_p90'))}, "
                f"fallback={_pct(row.get('fallback_rate'))}"
            )
    return lines


def _condition_lines(quality: dict[str, Any]) -> list[str]:
    counts: dict[str, int] = {}
    for family in quality.values():
        for metric in family.values():
            counts[metric.get("conclusion", "N/A")] = counts.get(metric.get("conclusion", "N/A"), 0) + 1
    return [f"- {key}: {value}" for key, value in sorted(counts.items())] or ["- N/A"]


def _pct(value: Any) -> str:
    return "N/A" if value is None else f"{float(value) * 100:.2f}%"


_HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CNSV V1.4 观察级回测</title>
  <style>
    :root{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Microsoft YaHei",sans-serif;--page:#f5f5f7;--surface:#fff;--line:#d2d2d7;--text:#1d1d1f;--muted:#6e6e73;--blue:#06c;--green:#0b8f45;--red:#d70015;--shadow:0 18px 44px rgba(0,0,0,.06)}
    *{box-sizing:border-box}body{margin:0;background:var(--page);color:var(--text)}main{width:min(100%,1180px);margin:auto;padding:38px 24px 48px}header{text-align:center;padding:18px 0 28px}.eyebrow{color:var(--blue);font-size:13px;font-weight:700;letter-spacing:.08em;margin:0 0 8px}h1{font-size:18px;margin:0}.subtitle{color:var(--muted);font-size:13px;margin:12px auto 0;max-width:840px;line-height:1.45}nav{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:16px}nav a{border:1px solid var(--line);border-radius:999px;color:var(--blue);text-decoration:none;padding:6px 11px;font-size:12px;background:#fff}section{background:var(--surface);border-radius:20px;padding:22px 26px;margin:16px 0;box-shadow:var(--shadow);overflow:hidden}h2{font-size:14px;margin:0 0 14px}.chips{display:flex;flex-wrap:wrap;gap:8px}.chip{border:1px solid var(--line);border-radius:999px;background:#fff;padding:7px 11px;color:var(--muted);font-size:12px}.chip strong{color:var(--text);margin-left:6px}.ok{color:var(--green)!important;font-weight:700}.bad{color:var(--red)!important;font-weight:700}.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;min-width:900px;background:#fff;font-size:12px}th,td{border-top:1px solid #e8e8ed;text-align:left;padding:9px 10px;white-space:nowrap}th{color:var(--muted)}.footer{color:var(--muted);font-size:12px;text-align:center;padding:18px 0 4px}@media(max-width:640px){main{padding:22px 14px 36px}header{text-align:left}nav{justify-content:flex-start}section{border-radius:18px;padding:18px}}
  </style>
</head>
<body>
<main>
  <header>
    <p class="eyebrow">CNSV V1.4 OBSERVATION BACKTEST</p>
    <h1>中国船舶观察级回测看板</h1>
    <p class="subtitle">验证 V1.3 路径分布、触达概率、下穿概率与回撤风险的历史参考价值。本页不是交易回测，不生成交易信号。</p>
    <nav><a href="index.html">主线看板</a><a href="path.html">路径分布</a><a href="data/latest_observation_backtest_report.json">JSON</a></nav>
  </header>
  <section><h2>阶段总览</h2><div id="overview" class="chips"></div></section>
  <section><h2>P0/P1/P2 总览</h2><div id="models"></div></section>
  <section><h2>触达概率分组</h2><div id="touch"></div></section>
  <section><h2>回撤风险分组</h2><div id="drawdown"></div></section>
  <section><h2>模型对比</h2><div id="comparison"></div></section>
  <section><h2>观察条件有效性</h2><div id="condition"></div></section>
  <section><h2>禁止交易信号声明</h2><div id="guardrails" class="chips"></div></section>
  <div id="footer" class="footer"></div>
</main>
<script>
const fmt=(v,k="")=>v===null||v===undefined?"N/A":typeof v==="number"?(k.includes("rate")||k.includes("return")||k.includes("coverage")||k.includes("drawdown")||k.includes("delta")?`${(v*100).toFixed(2)}%`:v.toFixed(4)):v;
const cls=v=>v==="PASS"?"ok":v==="FAIL"?"bad":"";
const chip=(l,v,c=cls(v))=>`<span class="chip">${l}<strong class="${c}">${fmt(v)}</strong></span>`;
const table=rows=>`<div class="table-wrap"><table><thead><tr>${rows[0].map(h=>`<th>${h}</th>`).join("")}</tr></thead><tbody>${rows.slice(1).map(r=>`<tr>${r.map(v=>`<td>${v}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
function metricsTable(m){const rows=[["模型","周期","样本","正收益","均值收益","+5%触达","-5%下穿","回撤P90","fallback"]]; for(const [model,hs] of Object.entries(m||{})){for(const [h,r] of Object.entries(hs||{})){rows.push([model,h,fmt(r.sample_size),fmt(r.actual_positive_terminal_rate,"rate"),fmt(r.mean_terminal_return,"return"),fmt(r.actual_touch_up_5pct_rate,"rate"),fmt(r.actual_touch_down_5pct_rate,"rate"),fmt(r.actual_max_drawdown_p90,"drawdown"),fmt(r.fallback_rate,"rate")]);}} return table(rows);}
function bucketTable(groups){const rows=[["模型","周期","指标","low样本","high样本","high-low收益差","high-low触达差","结论"]]; for(const [model,hs] of Object.entries(groups||{})){for(const [h,ms] of Object.entries(hs||{})){for(const [metric,g] of Object.entries(ms||{})){const b=g.buckets||{}; rows.push([model,h,metric,fmt((b.low||{}).sample_size),fmt((b.high||{}).sample_size),fmt(((b.high||{}).mean_terminal_return||0)-((b.low||{}).mean_terminal_return||0),"delta"),fmt(((b.high||{}).actual_touch_rate||0)-((b.low||{}).actual_touch_rate||0),"delta"),"观察"]);}}} return table(rows);}
function compareTable(c){const rows=[["周期","P1 vs P0","P2 vs P1","P1触达Brier差","P2触达Brier差","P2说明"]]; for(const [h,r] of Object.entries(c||{})){rows.push([h,r.P1_vs_P0_conclusion,r.P2_vs_P1_conclusion,fmt(r.P1_vs_P0_touch_brier_delta),fmt(r.P2_vs_P1_touch_brier_delta),r.P2_auxiliary_note]);} return table(rows);}
function conditionTable(q){const rows=[["分类","指标","结论","high样本","low样本","触达差","单调性"]]; for(const [fam,ms] of Object.entries(q||{})){for(const [metric,r] of Object.entries(ms||{})){rows.push([fam,metric,r.conclusion,fmt(r.high_bucket_sample_size),fmt(r.low_bucket_sample_size),fmt(r.high_vs_low_actual_touch_delta,"delta"),fmt(r.monotonicity_score)]);}} return table(rows);}
fetch("data/latest_observation_backtest_report.json").then(r=>r.json()).then(d=>{
 const q=d.observation_backtest_quality||{}, s=d.backtest_scope||{}, l=d.observation_backtest_leakage_checks||{};
 overview.innerHTML=[chip("版本",d.meta.version),chip("阶段",d.meta.stage),chip("质量",q.status),chip("standard样本",s.standard_sample_size),chip("purged样本",s.purged_sample_size),chip("leakage",l.status),chip("交易信号",d.meta.is_trade_signal?"YES":"NO",d.meta.is_trade_signal?"bad":"ok")].join("");
 models.innerHTML=metricsTable((d.model_backtest_metrics||{}).standard_walk_forward);
 touch.innerHTML=bucketTable(((d.observation_bucket_metrics||{}).touch_probability_groups||{}));
 drawdown.innerHTML=bucketTable(((d.observation_bucket_metrics||{}).drawdown_risk_groups||{}));
 comparison.innerHTML=compareTable(((d.model_comparison||{}).standard_walk_forward||{}));
 condition.innerHTML=conditionTable(d.observation_condition_quality||{});
 guardrails.innerHTML=(d.forbidden_actions||[]).map(x=>chip("禁止",x)).concat([chip("下一阶段",d.next_stage)]).join("");
 footer.textContent=`generated_at: ${d.meta.generated_at}`;
}).catch(e=>overview.innerHTML=`<span class="bad">加载失败：${e}</span>`);
</script>
</body>
</html>
"""
