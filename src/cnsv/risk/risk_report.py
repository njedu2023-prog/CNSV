from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from cnsv.utils.io import ensure_parent


def write_risk_explanation_json(payload: dict[str, Any], path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return target


def write_risk_explanation_md(payload: dict[str, Any], path: str | Path, archive_dir: str | Path | None = None) -> Path:
    target = ensure_parent(path)
    text = build_risk_explanation_markdown(payload)
    target.write_text(text, encoding="utf-8")
    if archive_dir:
        archive = ensure_parent(Path(archive_dir) / f"{date.today().isoformat()}_risk_explanation_report.md")
        archive.write_text(text, encoding="utf-8")
    return target


def build_risk_explanation_markdown(payload: dict[str, Any]) -> str:
    meta = payload.get("meta", {})
    quality = payload.get("risk_explanation_quality", {})
    availability = payload.get("risk_evidence_availability", {})
    summary = payload.get("overall_risk_summary", {})
    lines = [
        "# CNSV V1.6 风控解释报告", "", "本报告是风控解释，不是交易信号；不构成方向性操作建议，不输出交易执行参数或自动交易动作。", "",
        "## 阶段说明", f"- 版本: {meta.get('version')}", f"- 阶段: {meta.get('stage')}", f"- latest_trade_date: {meta.get('latest_trade_date')}", f"- 质量状态: {quality.get('status')}", f"- FAIL 数量: {quality.get('failed_count')}", f"- WARN 数量: {quality.get('warn_count')}", "",
        "## 上游证据可用性", f"- 全部必需证据可用: {availability.get('all_required_available')}", f"- 可用证据: {', '.join(availability.get('available_reports', []))}", f"- 缺失证据: {', '.join(availability.get('missing_reports', [])) or '无'}", "",
        "## 风险总览", f"- 总体风险等级: {summary.get('overall_risk_level')}", f"- 风险置信度: {summary.get('risk_confidence')}", f"- 主要风险来源: {', '.join(summary.get('primary_risk_sources', []))}", f"- 次要风险来源: {', '.join(summary.get('secondary_risk_sources', []))}", f"- 需要人工复核: {summary.get('human_review_required')}", f"- 风险原因: {summary.get('risk_reason')}", "",
        "## 风险来源拆解", *[f"- {key}: {item.get('risk_level')}；{item.get('risk_reason')}" for key, item in (payload.get("risk_source_breakdown") or {}).items()], "",
        "## 数据风险解释", *_section_lines(payload.get("data_risk_explanation") or {}), "", "## 特征风险解释", *_section_lines(payload.get("feature_risk_explanation") or {}), "", "## 基准模型风险解释", *_section_lines(payload.get("baseline_model_risk_explanation") or {}), "", "## 路径风险解释", *_section_lines(payload.get("path_distribution_risk_explanation") or {}), "", "## 观察级回测风险解释", *_section_lines(payload.get("observation_backtest_risk_explanation") or {}), "", "## 人工辅助证据风险解释", *_section_lines(payload.get("decision_support_risk_explanation") or {}), "", "## P2 辅助层风险解释", *_section_lines(payload.get("p2_auxiliary_risk_explanation") or {}), "", "## 证据冲突风险解释", *_section_lines(payload.get("evidence_conflict_risk_explanation") or {}), "",
        "## 风险情景卡片", *[f"- [{card.get('scenario_id')}] {card.get('scenario_name')}: {card.get('risk_level')}；{card.get('risk_explanation')}" for card in payload.get("risk_scenario_cards", [])], "",
        "## 风险复核清单", *[f"- [{item.get('id')}] {item.get('text')}" for item in payload.get("risk_review_checklist", [])], "",
        "## 禁止交易信号声明", "- 正式交易信号: NO", "- 方向性操作建议: NO", "- 交易执行参数: NO", "- 自动交易动作: NO", f"- forbidden_actions: {', '.join(payload.get('forbidden_actions', []))}", "",
        "## 是否允许进入 V2.0", f"- next_stage: {payload.get('next_stage')}", f"- V2.0 前置准备: {payload.get('v2_readiness')}",
    ]
    return "\n".join(lines) + "\n"


def write_risk_explanation_html(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(_HTML, encoding="utf-8")
    return target


def _section_lines(section: dict[str, Any]) -> list[str]:
    lines = []
    for key, value in section.items():
        if isinstance(value, dict):
            lines.append(f"- {key}: {value.get('risk_level', 'N/A')}；{value.get('risk_reason') or value.get('risk_explanation') or value}")
        elif isinstance(value, list):
            lines.append(f"- {key}: {', '.join(str(item) for item in value) or '无'}")
        else:
            lines.append(f"- {key}: {value}")
    return lines or ["- N/A"]


_HTML = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>CNSV V1.6 风控解释</title><style>:root{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Microsoft YaHei",sans-serif;--page:#f5f5f7;--surface:#fff;--line:#d2d2d7;--text:#1d1d1f;--muted:#6e6e73;--blue:#06c;--green:#0b8f45;--red:#d70015;--amber:#8a5a00;--shadow:0 18px 44px rgba(0,0,0,.06)}*{box-sizing:border-box}body{margin:0;background:var(--page);color:var(--text)}main{width:min(100%,1180px);margin:auto;padding:38px 24px 48px}header{text-align:center;padding:18px 0 28px}.eyebrow{color:var(--blue);font-size:13px;font-weight:700;letter-spacing:.08em;margin:0 0 8px}h1{font-size:18px;margin:0}.subtitle{color:var(--muted);font-size:13px;margin:12px auto 0;max-width:880px;line-height:1.45}nav{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:16px}nav a{border:1px solid var(--line);border-radius:999px;color:var(--blue);text-decoration:none;padding:6px 11px;font-size:12px;background:#fff}section{background:var(--surface);border-radius:20px;padding:22px 26px;margin:16px 0;box-shadow:var(--shadow);overflow:hidden}h2{font-size:14px;margin:0 0 14px}.chips{display:flex;flex-wrap:wrap;gap:8px}.chip{border:1px solid var(--line);border-radius:999px;background:#fff;padding:7px 11px;color:var(--muted);font-size:12px}.chip strong{color:var(--text);margin-left:6px}.ok{color:var(--green)!important;font-weight:700}.bad{color:var(--red)!important;font-weight:700}.warn{color:var(--amber)!important;font-weight:700}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.card{border:1px solid var(--line);border-radius:16px;padding:14px;background:#fbfbfd}.label{color:var(--muted);font-size:12px}.value{font-weight:700;font-size:13px;margin-top:8px;overflow-wrap:anywhere}.list{display:grid;gap:8px}.item{border:1px solid var(--line);border-radius:14px;padding:11px 13px;background:#fbfbfd;font-size:12px;line-height:1.45}.footer{color:var(--muted);font-size:12px;text-align:center;padding:18px 0 4px}@media(max-width:720px){main{padding:22px 14px 36px}header{text-align:left}nav{justify-content:flex-start}section{border-radius:18px;padding:18px}.grid{grid-template-columns:1fr}}</style></head><body><main><header><p class="eyebrow">CNSV V1.6 RISK EXPLANATION</p><h1>中国船舶风控解释看板</h1><p class="subtitle">解释 V1.0-V1.5 证据背后的数据、特征、模型、路径、回测、证据冲突与 P2 辅助层风险。页面只做风险解释，不生成交易信号。</p><nav><a href="index.html">主线看板</a><a href="decision_support.html">V1.5 人工辅助</a><a href="data/latest_risk_explanation_report.json">JSON</a></nav></header><section><h2>阶段总览</h2><div id="overview" class="chips"></div></section><section><h2>证据可用性</h2><div id="availability" class="chips"></div></section><section><h2>风险总览</h2><div id="summary" class="grid"></div></section><section><h2>风险来源拆解</h2><div id="breakdown" class="grid"></div></section><section><h2>分类风险解释</h2><div id="explain" class="list"></div></section><section><h2>风险情景卡片</h2><div id="cards" class="grid"></div></section><section><h2>风险复核清单</h2><div id="checklist" class="list"></div></section><section><h2>禁止交易信号声明</h2><div id="guardrails" class="chips"></div></section><div id="footer" class="footer"></div></main><script>const fmt=v=>v===null||v===undefined?"N/A":typeof v==="number"?v.toFixed(4):v;const cls=v=>v==="PASS"?"ok":v==="FAIL"?"bad":v==="WARN"?"warn":v==="high"||v==="severe"?"bad":v==="medium"?"warn":"";const chip=(l,v,c=cls(v))=>`<span class="chip">${l}<strong class="${c}">${fmt(v)}</strong></span>`;const card=(l,v)=>`<div class="card"><div class="label">${l}</div><div class="value">${fmt(v)}</div></div>`;const item=v=>`<div class="item">${v}</div>`;fetch("data/latest_risk_explanation_report.json").then(r=>r.json()).then(d=>{const meta=d.meta||{},q=d.risk_explanation_quality||{},av=d.risk_evidence_availability||{},s=d.overall_risk_summary||{};overview.innerHTML=[chip("版本",meta.version),chip("阶段",meta.stage),chip("质量",q.status),chip("交易信号",meta.is_trade_signal?"YES":"NO",meta.is_trade_signal?"bad":"ok")].join("");availability.innerHTML=[chip("全部可用",av.all_required_available),chip("可用数量",(av.available_reports||[]).length),chip("缺失数量",(av.missing_reports||[]).length)].concat((av.missing_reports||[]).map(x=>chip("缺失",x,"warn"))).join("");summary.innerHTML=Object.entries(s).map(([k,v])=>card(k,Array.isArray(v)?v.join(", "):v)).join("");breakdown.innerHTML=Object.entries(d.risk_source_breakdown||{}).map(([k,v])=>card(k,`${v.risk_level} · ${v.risk_reason}`)).join("");const sections=["data_risk_explanation","feature_risk_explanation","baseline_model_risk_explanation","path_distribution_risk_explanation","observation_backtest_risk_explanation","decision_support_risk_explanation","p2_auxiliary_risk_explanation","evidence_conflict_risk_explanation"];explain.innerHTML=sections.map(k=>item(`<b>${k}</b><br>${JSON.stringify(d[k]||{},null,2)}`)).join("");cards.innerHTML=(d.risk_scenario_cards||[]).map(x=>card(x.scenario_name,`${x.risk_level} · ${x.risk_explanation}`)).join("");checklist.innerHTML=(d.risk_review_checklist||[]).map(x=>item(`[${x.id}] ${x.text}`)).join("");guardrails.innerHTML=(d.forbidden_actions||[]).map(x=>chip("禁止",x,"bad")).concat([chip("下一阶段",d.next_stage)]).join("");footer.textContent=`generated_at: ${meta.generated_at}`}).catch(e=>overview.innerHTML=`<span class="bad">加载失败：${e}</span>`);</script></body></html>"""
