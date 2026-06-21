from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from cnsv.trading.utils import pct, probability_pct
from cnsv.utils.io import ensure_parent


def write_trading_json(payload: dict[str, Any], path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return target


def write_trading_markdown(payload: dict[str, Any], path: str | Path, archive_dir: str | Path | None = None) -> Path:
    target = ensure_parent(path)
    text = build_trading_markdown(payload)
    target.write_text(text, encoding="utf-8")
    if archive_dir:
        archive = ensure_parent(Path(archive_dir) / f"{date.today().isoformat()}_trading_decision_report.md")
        archive.write_text(text, encoding="utf-8")
    return target


def build_trading_markdown(payload: dict[str, Any]) -> str:
    d = payload["decision"]
    p = payload["probability"]
    dist = payload["return_distribution"]
    ev = payload["ev"]
    risk = payload["risk"]
    exit_plan = payload["exit"]
    lines = [
        "# CNSV V3.0 交易决策系统报告",
        "",
        "本报告为人工交易决策参考，不连接券商接口，不自动下单。",
        "",
        "## 今日总决策",
        f"- 标的: {payload['symbol']} {payload['name']}",
        f"- 交易日: {payload['trade_date']}",
        f"- 信号: {d['signal']} / {d['signal_cn']}",
        f"- 动作: {d['suggested_action']}",
        f"- 建议仓位: {d['position_range']}",
        "",
        "## 次日涨跌概率",
        f"- 上涨概率: {probability_pct(p['prob_up_1d'])}",
        f"- 下跌概率: {probability_pct(p['prob_down_1d'])}",
        f"- 平盘概率: {probability_pct(p['prob_flat_1d'])}",
        f"- 方向置信度: {p['direction_confidence']:.2f}",
        "",
        "## 次日涨跌幅分布",
        f"- 预期收益: {pct(dist['expected_return_1d'])}",
        f"- 中位收益: {pct(dist['median_return_1d'])}",
        f"- P10: {pct(dist['p10_return_1d'])}",
        f"- P90: {pct(dist['p90_return_1d'])}",
        "",
        "## EV 期望收益",
        f"- 原始 EV: {pct(ev['raw_ev'])}",
        f"- 成本调整 EV: {pct(ev['cost_adjusted_ev'])}",
        f"- 风险调整 EV: {pct(ev['risk_adjusted_ev'])}",
        f"- EV 评级: {ev['ev_rating_cn']}",
        "",
        "## 风险等级",
        f"- 风险等级: {risk['risk_level_cn']}",
        f"- 风控通过: {risk['risk_passed']}",
        f"- 买入拦截: {risk['buy_blocked']}",
        f"- 拦截原因: {', '.join(risk.get('buy_block_reasons', [])) or '无'}",
        "",
        "## 仓位建议",
        f"- 仓位动作: {d['position_action']}",
        f"- 仓位区间: {d['position_range']}",
        f"- 仓位说明: {d['position_reason']}",
        "",
        "## 止盈止损参考",
        f"- 止盈参考: {exit_plan['take_profit_range']}",
        f"- 止损参考: {exit_plan['stop_loss_reference']}",
        f"- 时间退出: {exit_plan['time_exit_days']} 个交易日后重新评估",
        "",
        "## 模型来源",
        f"- 基准模型: {', '.join(payload['model_sources']['baseline_models'])}",
        f"- 路径模型: {', '.join(payload['model_sources']['path_models'])}",
        "",
        "## 人工执行说明",
        f"- {payload['human_explanation']['summary']}",
        f"- {payload['human_explanation']['risk_note']}",
        f"- {payload['human_explanation']['execution_note']}",
    ]
    return "\n".join(lines) + "\n"


def write_trading_html(payload: dict[str, Any], path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(build_trading_html(payload), encoding="utf-8")
    return target


def build_trading_html(payload: dict[str, Any]) -> str:
    d = payload["decision"]
    p = payload["probability"]
    dist = payload["return_distribution"]
    ev = payload["ev"]
    risk = payload["risk"]
    exit_plan = payload["exit"]
    signal_class = "buy" if d["signal"] in {"BUY", "STRONG_BUY"} else "sell" if d["signal"] in {"SELL", "STRONG_SELL", "REDUCE"} else "blocked" if d["signal"] == "BLOCKED" else "watch"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>CNSV V3.0 交易决策系统</title>
  <style>
    :root{{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Microsoft YaHei",sans-serif;color:#1d1d1f;background:#f5f5f7;--line:#d2d2d7;--muted:#6e6e73;--blue:#06c;--green:#0b8f45;--red:#d70015;--amber:#8a5a00;--shadow:0 24px 70px rgba(0,0,0,.08)}}*{{box-sizing:border-box}}body{{margin:0;background:#f5f5f7}}main{{width:min(1180px,100%);margin:auto;padding:34px 20px 48px}}.hero{{min-height:390px;display:grid;align-items:center;text-align:center;padding:34px 0 48px}}.eyebrow{{color:var(--blue);font-size:13px;font-weight:700;letter-spacing:.08em}}h1{{font-size:34px;margin:8px 0 12px}}.subtitle{{color:var(--muted);font-size:14px}}.decision{{background:#fff;border-radius:28px;box-shadow:var(--shadow);padding:30px;margin-top:28px}}.signal{{font-size:72px;line-height:.95;font-weight:800;letter-spacing:0}}.buy{{color:var(--red)}}.sell,.blocked{{color:var(--green)}}.watch{{color:#1d1d1f}}.decision-text{{font-size:22px;font-weight:700;margin-top:12px}}.hero-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:24px}}.metric{{border:1px solid var(--line);border-radius:18px;background:#fbfbfd;padding:15px;text-align:left}}.label{{color:var(--muted);font-size:12px}}.value{{font-size:20px;font-weight:700;margin-top:7px}}section{{background:#fff;border-radius:24px;box-shadow:var(--shadow);padding:24px;margin:18px 0}}h2{{font-size:18px;margin:0 0 16px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}}.note{{color:var(--muted);font-size:13px;line-height:1.55}}.pill{{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:8px 12px;margin:4px;background:#fbfbfd;font-size:13px}}.pill strong{{margin-left:6px}}.footer{{color:var(--muted);font-size:12px;text-align:center;padding:18px}}nav{{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:16px}}nav a{{border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--blue);text-decoration:none;padding:7px 12px;font-size:12px}}@media(max-width:760px){{main{{padding:22px 14px}}h1{{font-size:25px}}.signal{{font-size:50px}}.hero-grid{{grid-template-columns:1fr 1fr}}.decision{{padding:22px}}}}
  </style>
</head>
<body>
<main>
  <div class="hero">
    <div>
      <div class="eyebrow">CNSV V3.0 交易决策系统</div>
      <h1>中国船舶 600150.SH</h1>
      <p class="subtitle">人工执行量化交易决策参考。不自动下单，不连接券商接口。</p>
      <nav><a href="index.html">主线看板</a><a href="live.html">V2.0 人工决策</a><a href="data/latest_trading_decision_report.json">原始 JSON</a></nav>
      <div class="decision">
        <div class="label">今日决策</div>
        <div class="signal {signal_class}">{d['signal']}</div>
        <div class="decision-text">{d['signal_cn']} · {d['suggested_action']}</div>
        <p class="note">{payload['human_explanation']['summary']}</p>
        <div class="hero-grid">
          <div class="metric"><div class="label">建议仓位</div><div class="value">{d['position_range']}</div></div>
          <div class="metric"><div class="label">次日上涨概率</div><div class="value">{probability_pct(p['prob_up_1d'])}</div></div>
          <div class="metric"><div class="label">风险调整 EV</div><div class="value">{pct(ev['risk_adjusted_ev'])}</div></div>
          <div class="metric"><div class="label">风险等级</div><div class="value">{risk['risk_level_cn']}</div></div>
        </div>
      </div>
    </div>
  </div>
  <section><h2>概率判断</h2><div class="grid">
    <div class="metric"><div class="label">明天上涨概率</div><div class="value">{probability_pct(p['prob_up_1d'])}</div></div>
    <div class="metric"><div class="label">明天下跌概率</div><div class="value">{probability_pct(p['prob_down_1d'])}</div></div>
    <div class="metric"><div class="label">大涨概率</div><div class="value">{probability_pct(dist['return_bins_1d']['gt_5pct'])}</div></div>
    <div class="metric"><div class="label">大跌概率</div><div class="value">{probability_pct(dist['return_bins_1d']['lt_minus_5pct'])}</div></div>
  </div></section>
  <section><h2>EV 与性价比</h2><div class="grid">
    <div class="metric"><div class="label">原始 EV</div><div class="value">{pct(ev['raw_ev'])}</div></div>
    <div class="metric"><div class="label">成本调整 EV</div><div class="value">{pct(ev['cost_adjusted_ev'])}</div></div>
    <div class="metric"><div class="label">风险调整 EV</div><div class="value">{pct(ev['risk_adjusted_ev'])}</div></div>
    <div class="metric"><div class="label">交易性价比</div><div class="value">{ev['ev_rating_cn']}</div></div>
  </div><p class="note">EV 为长期重复同类交易时的期望收益，单次交易仍可能亏损。</p></section>
  <section><h2>风控状态</h2><div class="grid">
    <div class="metric"><div class="label">当前风险</div><div class="value">{risk['risk_level_cn']}</div></div>
    <div class="metric"><div class="label">风控状态</div><div class="value">{'已拦截' if risk['buy_blocked'] else '通过'}</div></div>
    <div class="metric"><div class="label">主要风险</div><div class="value">{'；'.join(risk.get('buy_block_reasons') or risk.get('warnings') or ['无硬拦截'])}</div></div>
  </div><p class="note">{risk['human_risk_explanation']}</p></section>
  <section><h2>仓位与退出</h2><div class="grid">
    <div class="metric"><div class="label">建议仓位</div><div class="value">{d['position_range']}</div><p class="note">不建议满仓，不建议加杠杆。</p></div>
    <div class="metric"><div class="label">止盈参考</div><div class="value">{exit_plan['take_profit_range']}</div></div>
    <div class="metric"><div class="label">止损参考</div><div class="value">{exit_plan['stop_loss_reference']}</div></div>
    <div class="metric"><div class="label">时间退出</div><div class="value">{exit_plan['time_exit_days']} 个交易日</div></div>
  </div></section>
  <section><h2>人工执行说明</h2>
    <span class="pill">自动下单 <strong>关闭</strong></span>
    <span class="pill">券商接口 <strong>关闭</strong></span>
    <span class="pill">人工参考 <strong>是</strong></span>
    <p class="note">{payload['human_explanation']['execution_note']}</p>
  </section>
  <div class="footer">生成时间：{payload['generated_at']} · 数据日期：{payload['trade_date']}</div>
</main>
</body>
</html>"""


def write_trading_registry(path: str | Path) -> Path:
    target = ensure_parent(path)
    registry = [
        {
            "registry_type": "trading_decision",
            "version": "3.0",
            "stage": "V3.0_trading_decision_system",
            "outputs": [
                "latest_trading_decision_report.json",
                "trading_decision_registry.json",
                "latest_trading_decision_report.md",
                "trading.html",
            ],
        }
    ]
    target.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target
