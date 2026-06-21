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
    hist = payload.get("historical_validation") or {}
    performance = payload.get("model_performance") or {}
    historical_stats = performance.get("historical_stats") or {}
    live_stats = performance.get("live_stats") or {}
    b2_std = ((hist.get("baseline_directional_accuracy") or {}).get("standard") or {})
    b2_purged = ((hist.get("baseline_directional_accuracy") or {}).get("purged") or {})
    p2_std = ((hist.get("path_probability_validation") or {}).get("standard") or {})
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
        "## 历史验证与回测",
        f"- B2 5D 标准样本方向准确率: {probability_pct(b2_std.get('directional_accuracy', 0.0))} / 样本数: {b2_std.get('sample_size', 'N/A')}",
        f"- B2 5D purged 样本方向准确率: {probability_pct(b2_purged.get('directional_accuracy', 0.0))} / 样本数: {b2_purged.get('sample_size', 'N/A')}",
        f"- P2 5D 路径区间覆盖率: {probability_pct(p2_std.get('terminal_p10_p90_coverage', 0.0))} / Brier: {fmt_number(p2_std.get('positive_terminal_brier'))}",
        f"- 说明: {hist.get('interpretation', '历史验证只作为参考，不保证未来收益。')}",
        "",
        "## 模型表现追踪",
        f"- 历史统计线方向准确率: {probability_pct(historical_stats.get('direction_accuracy'))}",
        f"- 历史统计线样本数: {fmt_count(historical_stats.get('sample_count'))}",
        f"- 实盘统计线起始日期: {live_stats.get('start_date', '2026-06-21')}",
        f"- 实盘统计线方向准确率: {_live_accuracy_text(live_stats)}",
        f"- 实盘统计线正确/错误/样本数: {live_stats.get('correct_count', 0)} / {live_stats.get('wrong_count', 0)} / {live_stats.get('sample_count', 0)}",
        "- 样本不足提示: 实盘统计线样本仍然较少，暂不建议单独依赖该准确率判断系统有效性。" if (live_stats.get("sample_count") or 0) < 20 else "",
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
    hist = payload.get("historical_validation") or {}
    performance = payload.get("model_performance") or {}
    historical_stats = performance.get("historical_stats") or {}
    live_stats = performance.get("live_stats") or {}
    b2_std = ((hist.get("baseline_directional_accuracy") or {}).get("standard") or {})
    b2_purged = ((hist.get("baseline_directional_accuracy") or {}).get("purged") or {})
    p2_std = ((hist.get("path_probability_validation") or {}).get("standard") or {})
    p2_purged = ((hist.get("path_probability_validation") or {}).get("purged") or {})
    live_sample_count = live_stats.get("sample_count") or 0
    live_sample_note = (
        "<p class=\"note warn\">实盘统计线样本仍然较少，暂不建议单独依赖该准确率判断系统有效性。</p>"
        if live_sample_count < 20
        else ""
    )
    signal_class = "buy" if d["signal"] in {"BUY", "STRONG_BUY"} else "sell" if d["signal"] in {"SELL", "STRONG_SELL", "REDUCE"} else "blocked" if d["signal"] == "BLOCKED" else "watch"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>CNSV V3.0 交易决策系统</title>
  <style>
    :root{{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Microsoft YaHei",sans-serif;color:#1d1d1f;background:#f5f5f7;--line:#d2d2d7;--muted:#6e6e73;--blue:#06c;--green:#0b8f45;--red:#d70015;--shadow:0 16px 40px rgba(0,0,0,.07)}}*{{box-sizing:border-box}}body{{margin:0;background:#f5f5f7}}.topbar{{position:fixed;top:0;left:0;right:0;z-index:20;background:rgba(0,0,0,.88);backdrop-filter:saturate(180%) blur(18px);border-bottom:1px solid rgba(255,255,255,.16)}}.topnav{{display:flex;gap:2px;overflow-x:auto;white-space:nowrap;justify-content:center;padding:9px 18px}}.topnav a{{color:#fff;text-decoration:none;font-size:12px;line-height:1.2;padding:4px 10px;border-radius:999px;opacity:.78}}.topnav a:hover,.topnav a.active{{opacity:1}}.topnav a.active{{font-weight:600;background:rgba(255,255,255,.12)}}main{{width:min(1180px,100%);margin:auto;padding:52px 18px 28px}}.hero{{display:grid;align-items:center;text-align:center;padding:16px 0 20px}}.eyebrow{{color:var(--blue);font-size:12px;font-weight:700;letter-spacing:.08em}}h1{{font-size:30px;margin:5px 0 8px}}.subtitle{{color:var(--muted);font-size:13px;margin:0}}.quick{{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:10px}}.quick a{{border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--blue);text-decoration:none;padding:5px 10px;font-size:12px}}.decision{{background:#fff;border-radius:22px;box-shadow:var(--shadow);padding:18px;margin-top:16px}}.signal{{font-size:56px;line-height:.92;font-weight:800;letter-spacing:0}}.buy{{color:var(--red)}}.sell,.blocked{{color:var(--green)}}.watch{{color:#1d1d1f}}.decision-text{{font-size:18px;font-weight:700;margin-top:8px}}.hero-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin-top:14px}}.metric{{border:1px solid var(--line);border-radius:14px;background:#fbfbfd;padding:10px;text-align:left}}.label{{color:var(--muted);font-size:12px}}.value{{font-size:17px;font-weight:700;margin-top:4px}}section{{background:#fff;border-radius:18px;box-shadow:var(--shadow);padding:16px;margin:12px 0}}h2{{font-size:16px;margin:0 0 10px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px}}.note{{color:var(--muted);font-size:12px;line-height:1.45;margin:8px 0 0}}.warn{{color:#8a5a00}}.metric .note{{margin-top:5px}}.pill{{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:6px 10px;margin:3px;background:#fbfbfd;font-size:12px}}.pill strong{{margin-left:6px}}.footer{{color:var(--muted);font-size:12px;text-align:center;padding:12px}}@media(max-width:760px){{.topnav{{justify-content:flex-start}}.hero{{padding:12px 0 16px}}main{{padding:50px 12px 24px}}h1{{font-size:24px}}.signal{{font-size:44px}}.hero-grid{{grid-template-columns:1fr 1fr}}.decision{{padding:14px}}.value{{font-size:16px}}}}
  </style>
</head>
<body>
<div class="topbar"><nav class="topnav" aria-label="CNSV 全量菜单"><a href="trading.html" class="active">V3.0 交易决策</a><a href="data/latest_data_report.json">数据状态</a><a href="data/latest_feature_report.json">核心特征</a><a href="baseline.html">V1.2 基准模型</a><a href="validation.html">V1.2.2 验证</a><a href="path.html">V1.3 路径分布</a><a href="backtest.html">V1.4 观察级回测</a><a href="decision_support.html">V1.5 人工决策辅助</a><a href="risk.html">V1.6 风控解释</a><a href="live.html">V2.0 实盘人工决策</a></nav></div>
<main>
  <div class="hero">
    <div>
      <div class="eyebrow">CNSV V3.0 交易决策系统</div>
      <h1>中国船舶 600150.SH</h1>
      <p class="subtitle">人工执行量化交易决策参考。不自动下单，不连接券商接口。</p>
      <div class="quick"><a href="index.html">主线看板</a><a href="live.html">V2.0 人工决策</a><a href="data/latest_trading_decision_report.json">原始 JSON</a></div>
      <div class="decision">
        <div class="label">今日决策</div>
        <div class="signal {signal_class}">{d['signal']}</div>
        <div class="decision-text">{d['signal_cn']} · {d['suggested_action']}</div>
        <p class="note">{payload['human_explanation']['summary']}</p>
        <div class="hero-grid">
          <div class="metric"><div class="label">建议仓位</div><div class="value">{d['position_range']}</div></div>
          <div class="metric"><div class="label">次日上涨概率</div><div class="value">{probability_pct(p['prob_up_1d'])}</div></div>
          <div class="metric"><div class="label">历史方向准确率</div><div class="value">{probability_pct(b2_std.get('directional_accuracy', 0.0))}</div></div>
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
  <section><h2>模型表现追踪</h2><div class="grid">
    <div class="metric"><div class="label">{historical_stats.get('name', '历史统计线')}</div><div class="value">方向准确率：{probability_pct(historical_stats.get('direction_accuracy'))}</div><p class="note">样本数：{fmt_count(historical_stats.get('sample_count'))}</p><p class="note">{historical_stats.get('description', '包含历史验证、walk-forward、purged walk-forward 等历史样本。')}</p></div>
    <div class="metric"><div class="label">{live_stats.get('name', '实盘统计线')}</div><div class="value">方向准确率：{_live_accuracy_text(live_stats)}</div><p class="note">起始日期：{live_stats.get('start_date', '2026-06-21')} · 样本数：{live_stats.get('sample_count', 0)}</p><p class="note">正确次数：{live_stats.get('correct_count', 0)} · 错误次数：{live_stats.get('wrong_count', 0)}</p><p class="note">{live_stats.get('description', '只统计 V3.0 正式运行后的真实表现。')}</p></div>
    <div class="metric"><div class="label">历史验证补充</div><div class="value">B2 5D：{probability_pct(b2_std.get('directional_accuracy', 0.0))}</div><p class="note">standard 样本：{fmt_count(b2_std.get('sample_size'))} · purged：{probability_pct(b2_purged.get('directional_accuracy'))}</p><p class="note">P2 覆盖率：{probability_pct(p2_std.get('terminal_p10_p90_coverage'))} · Brier：{fmt_number(p2_std.get('positive_terminal_brier'))}</p></div>
  </div>{live_sample_note}</section>
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


def fmt_number(value: Any, digits: int = 4) -> str:
    if value is None:
        return "N/A"
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return "N/A"


def fmt_count(value: Any) -> str:
    if value is None:
        return "--"
    try:
        return str(int(value))
    except (TypeError, ValueError):
        return "--"


def _live_accuracy_text(live_stats: dict[str, Any]) -> str:
    if not live_stats.get("sample_count"):
        return "暂无样本"
    return probability_pct(live_stats.get("direction_accuracy"))
