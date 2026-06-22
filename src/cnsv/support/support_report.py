from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from cnsv.report.site_chrome import apply_site_chrome
from cnsv.utils.io import ensure_parent


def write_human_decision_support_json(payload: dict[str, Any], path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return target


def write_human_decision_support_md(payload: dict[str, Any], path: str | Path, archive_dir: str | Path | None = None) -> Path:
    text = build_human_decision_support_markdown(payload)
    target = ensure_parent(path)
    target.write_text(text, encoding="utf-8")
    if archive_dir:
        archive = ensure_parent(Path(archive_dir) / f"{date.today().isoformat()}_human_decision_support_report.md")
        archive.write_text(text, encoding="utf-8")
    return target


def build_human_decision_support_markdown(payload: dict[str, Any]) -> str:
    meta = payload.get("meta", {})
    quality = payload.get("human_decision_support_quality", {})
    return "\n".join([
        "# CNSV V1.5 人工决策辅助报告",
        "",
        "本报告是人工决策辅助，不是交易信号；不构成方向性操作建议，不输出交易执行参数或自动交易动作。",
        "",
        f"- version: {meta.get('version')}",
        f"- stage: {meta.get('stage')}",
        f"- latest_trade_date: {meta.get('latest_trade_date')}",
        f"- quality: {quality.get('status')}",
        f"- forbidden_actions: {', '.join(payload.get('forbidden_actions', []))}",
        "",
    ])


def write_human_decision_support_html(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(apply_site_chrome(_HTML, "decision_support"), encoding="utf-8")
    return target


_HTML = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CNSV V1.5 人工决策辅助</title><style>:root{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Microsoft YaHei",sans-serif;--page:#f5f5f7;--surface:#fff;--line:#d2d2d7;--text:#1d1d1f;--muted:#6e6e73;--blue:#06c;--green:#0b8f45;--red:#d70015;--shadow:0 18px 44px rgba(0,0,0,.06)}*{box-sizing:border-box}body{margin:0;background:var(--page);color:var(--text)}main{width:min(100%,1180px);margin:auto;padding:38px 24px 48px}header{text-align:center;padding:18px 0 28px}.eyebrow{color:var(--blue);font-size:13px;font-weight:700;letter-spacing:.08em;margin:0 0 8px}h1{font-size:18px;margin:0}.subtitle{color:var(--muted);font-size:13px;margin:12px auto 0;max-width:860px;line-height:1.45}nav{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:16px}nav a{border:1px solid var(--line);border-radius:999px;color:var(--blue);text-decoration:none;padding:6px 11px;font-size:12px;background:#fff}section{background:var(--surface);border-radius:20px;padding:22px 26px;margin:16px 0;box-shadow:var(--shadow)}h2{font-size:14px;margin:0 0 14px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:10px}.card{border:1px solid var(--line);border-radius:16px;padding:14px;background:#fbfbfd}.label{color:var(--muted);font-size:12px}.value{font-weight:700;font-size:13px;margin-top:8px;overflow-wrap:anywhere}.footer{color:var(--muted);font-size:12px;text-align:center}</style></head><body><main><header><p class="eyebrow">CNSV V1.5 HUMAN DECISION SUPPORT</p><h1>中国船舶人工决策辅助看板</h1><p class="subtitle">供人工复核；页面不生成交易信号。</p><nav><a href="index.html">主线看板</a><a href="backtest.html">V1.4 观察级回测</a><a href="data/latest_human_decision_support_report.json">JSON</a></nav></header><section><h2>阶段总览</h2><div id="overview" class="grid"></div></section><section><h2>当前状态摘要</h2><div id="state" class="grid"></div></section><section><h2>人工关注点</h2><div id="attention" class="grid"></div></section><section><h2>禁止交易信号声明</h2><div id="guard" class="grid"></div></section><div id="footer" class="footer"></div></main><script>const fmt=v=>v===null||v===undefined?'N/A':typeof v==='object'?JSON.stringify(v):v;const card=(l,v)=>`<div class="card"><div class="label">${l}</div><div class="value">${fmt(v)}</div></div>`;fetch('data/latest_human_decision_support_report.json').then(r=>r.json()).then(d=>{const m=d.meta||{},q=d.human_decision_support_quality||{};overview.innerHTML=[card('版本',m.version),card('阶段',m.stage),card('质量',q.status),card('交易信号',m.is_trade_signal?'YES':'NO')].join('');state.innerHTML=Object.entries(d.current_state_summary||{}).map(([k,v])=>card(k,v)).join('');attention.innerHTML=(d.human_attention_items||[]).map(x=>card(x.category,x.text)).join('');guard.innerHTML=(d.forbidden_actions||[]).map(x=>card('禁止动作',x)).join('');footer.textContent='generated_at: '+(m.generated_at||'N/A')});</script></body></html>"""
