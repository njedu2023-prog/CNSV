from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

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
        generated_date = str(payload.get("generated_at_beijing") or "")[:10]
        if len(generated_date) != 10:
            generated_date = datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()
        archive = ensure_parent(Path(archive_dir) / f"{generated_date}_trading_decision_report.md")
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
    timeline = payload.get("decision_timeline") or {}
    market = payload.get("market_snapshot") or {}
    price_paths = payload.get("price_prediction_distribution") or {}
    t1_std = ((hist.get("next_day_directional_accuracy") or {}).get("standard") or {})
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
        f"- 数据交易日: {timeline.get('data_trade_date', payload['trade_date'])}",
        f"- 信号生成日: {timeline.get('signal_date', 'N/A')}",
        f"- 预测日: {timeline.get('prediction_date', 'N/A')}",
        f"- 验证日: {timeline.get('verify_date', 'N/A')}",
        f"- 预测方向: {p.get('predicted_direction') or 'N/A'}",
        f"- 模型ID: {p.get('model_id') or 'N/A'}",
        f"- 行情基准价: {fmt_number(market.get('latest_close'))}",
        f"- 基准价涨跌幅: {fmt_pct_points(market.get('latest_pct_chg'))}",
        f"- 累计成交额: {fmt_amount(market.get('latest_amount'))}",
        f"- 行情数据时间（北京时间）: {_market_data_time(market)}",
        f"- 预测口径: {_prediction_basis_text(market.get('prediction_basis', p.get('prediction_basis')))}",
        "",
        "## 次日涨跌概率",
        f"- 上涨概率: {probability_pct(p['prob_up_1d'])}",
        f"- 下跌概率: {probability_pct(p['prob_down_1d'])}",
        f"- 次日预测方向: {p.get('predicted_direction') or 'N/A'}",
        f"- 方向置信度: {probability_pct(p['direction_confidence'])}",
        f"- 核心模型: {p.get('model_id') or 'N/A'}",
        "",
        "## 历史验证与回测",
        f"- T+1 扩展窗口方向准确率: {probability_pct(t1_std.get('directional_accuracy'))} / 样本数: {t1_std.get('sample_size', 'N/A')}",
        f"- T+1 准确率 95% 区间: {probability_pct(t1_std.get('accuracy_ci_95_low'))} ~ {probability_pct(t1_std.get('accuracy_ci_95_high'))}",
        f"- T+1 高置信样本准确率: {probability_pct(t1_std.get('high_confidence_accuracy'))} / 覆盖率: {probability_pct(t1_std.get('high_confidence_coverage'))}",
        f"- T+1 验证 Brier / AUC: {fmt_number(t1_std.get('brier_active', t1_std.get('brier_calibrated')))} / {fmt_number(t1_std.get('roc_auc'))}",
        f"- 5D 辅助模型方向准确率: {probability_pct(b2_std.get('directional_accuracy'))} / purged: {probability_pct(b2_purged.get('directional_accuracy'))}",
        f"- P2 5D 路径区间覆盖率: {probability_pct(p2_std.get('terminal_p10_p90_coverage', 0.0))} / Brier: {fmt_number(p2_std.get('positive_terminal_brier'))}",
        f"- 说明: {hist.get('interpretation', '历史验证只作为参考，不保证未来收益。')}",
        "",
        "## 模型表现追踪",
        f"- 历史统计线方向准确率: {probability_pct(historical_stats.get('direction_accuracy'))}",
        f"- 历史统计线样本数: {fmt_count(historical_stats.get('sample_count'))}",
        f"- 实盘统计线起始日期: {live_stats.get('start_date', 'N/A')}",
        f"- 实盘统计线方向准确率: {_live_accuracy_text(live_stats)}",
        f"- 实盘统计线正确/错误/样本数: {live_stats.get('correct_count', 0)} / {live_stats.get('wrong_count', 0)} / {live_stats.get('sample_count', 0)}",
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
        "## 5D / 10D / 20D 价格预测分布",
        *_price_distribution_markdown(price_paths),
        "",
        "## 模型来源",
        f"- 次日模型: {p.get('model_id') or 'N/A'}",
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
    timeline = payload.get("decision_timeline") or {}
    market = payload.get("market_snapshot") or {}
    price_paths = payload.get("price_prediction_distribution") or {}
    t1_std = ((hist.get("next_day_directional_accuracy") or {}).get("standard") or {})
    b2_std = ((hist.get("baseline_directional_accuracy") or {}).get("standard") or {})
    b2_purged = ((hist.get("baseline_directional_accuracy") or {}).get("purged") or {})
    p2_std = ((hist.get("path_probability_validation") or {}).get("standard") or {})
    p2_purged = ((hist.get("path_probability_validation") or {}).get("purged") or {})
    predicted_direction = p.get("predicted_direction") or "N/A"
    signal_class = "buy" if predicted_direction == "UP" else "sell" if predicted_direction == "DOWN" else "blocked" if d["signal"] == "BLOCKED" else "watch"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>CNSV V3.0 交易决策系统</title>
  <style>
    :root{{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Microsoft YaHei",sans-serif;color:#1d1d1f;background:#f5f5f7;--line:#d2d2d7;--muted:#6e6e73;--blue:#06c;--green:#0b8f45;--red:#d70015;--shadow:0 16px 40px rgba(0,0,0,.07)}}*{{box-sizing:border-box}}body{{margin:0;background:#f5f5f7}}.topbar{{position:fixed;top:0;left:0;right:0;z-index:20;background:rgba(0,0,0,.88);backdrop-filter:saturate(180%) blur(18px);border-bottom:1px solid rgba(255,255,255,.16)}}.topnav{{display:flex;gap:2px;overflow-x:auto;white-space:nowrap;justify-content:center;padding:9px 18px}}.topnav a{{color:#fff;text-decoration:none;font-size:12px;line-height:1.2;padding:4px 10px;border-radius:999px;opacity:.78}}.topnav a:hover,.topnav a.active{{opacity:1}}.topnav a.active{{font-weight:600;background:rgba(255,255,255,.12)}}main{{width:min(1180px,100%);margin:auto;padding:52px 18px 28px}}.hero{{display:grid;align-items:center;text-align:center;padding:16px 0 20px}}.eyebrow{{color:var(--red);font-size:12px;font-weight:700;letter-spacing:.08em}}h1{{font-size:30px;margin:5px 0 8px}}.subtitle{{color:var(--muted);font-size:13px;margin:0}}.quick{{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:10px}}.quick a{{border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--blue);text-decoration:none;padding:5px 10px;font-size:12px}}.decision{{background:#fff;border-radius:22px;box-shadow:var(--shadow);padding:18px;margin-top:16px}}.signal{{font-size:56px;line-height:.92;font-weight:800;letter-spacing:0}}.buy{{color:var(--red)}}.sell,.blocked{{color:var(--green)}}.watch{{color:#1d1d1f}}.decision-text{{font-size:18px;font-weight:700;margin-top:8px}}.hero-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin-top:14px}}.timeline-table{{width:100%;border-collapse:separate;border-spacing:0;margin-top:12px;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fbfbfd;text-align:left}}.timeline-table th,.timeline-table td{{padding:8px 10px;border-bottom:1px solid var(--line);font-size:12px}}.timeline-table tr:last-child th,.timeline-table tr:last-child td{{border-bottom:0}}.timeline-table th{{color:var(--muted);font-weight:500;width:36%}}.timeline-table td{{font-weight:700;color:#1d1d1f}}.metric{{border:1px solid var(--line);border-radius:14px;background:#fbfbfd;padding:10px;text-align:left}}.label{{color:var(--muted);font-size:12px}}.value{{font-size:17px;font-weight:700;margin-top:4px}}.value.long-text{{font-size:13px;line-height:1.45;font-weight:600;overflow-wrap:anywhere;word-break:break-word}}section{{background:#fff;border-radius:18px;box-shadow:var(--shadow);padding:16px;margin:12px 0}}h2{{font-size:16px;margin:0 0 10px}}h3{{font-size:13px;margin:0 0 6px;color:#1d1d1f}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px}}.three-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}.note{{color:var(--muted);font-size:12px;line-height:1.45;margin:8px 0 0}}.warn{{color:#8a5a00}}.metric .note{{margin-top:5px}}.pill{{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:6px 10px;margin:3px;background:#fbfbfd;font-size:12px}}.pill strong{{margin-left:6px}}.footer{{color:var(--muted);font-size:12px;text-align:center;padding:12px}}@media(max-width:760px){{.topnav{{justify-content:flex-start}}.hero{{padding:12px 0 16px}}main{{padding:50px 12px 24px}}h1{{font-size:24px}}.signal{{font-size:44px}}.hero-grid{{grid-template-columns:1fr 1fr}}.three-grid{{grid-template-columns:1fr}}.decision{{padding:14px}}.value{{font-size:16px}}.value.long-text{{font-size:13px}}}}
  </style>
  <style>
    .pair-table tbody{{display:block}}.pair-table tr{{display:grid;grid-template-columns:168px minmax(0,1fr) 168px minmax(0,1fr);align-items:stretch}}.pair-table th,.pair-table td{{width:auto;min-width:0}}.pair-table th{{padding-right:0;text-align:right;white-space:normal}}.pair-table th::after{{content:"："}}.pair-table td{{padding-left:6px;text-align:left;overflow-wrap:anywhere}}@media(max-width:760px){{.pair-table tr{{grid-template-columns:148px minmax(0,1fr)}}.pair-table tr:last-child>:nth-child(-n+2){{border-bottom:1px solid var(--line)}}}}
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
        <table class="timeline-table pair-table" aria-label="交易决策日期表">
          <tbody>
            <tr><th>数据交易日（T）</th><td>{timeline.get('data_trade_date', payload['trade_date'])}</td><th>决策适用日（T+1）</th><td>{timeline.get('prediction_date', 'N/A')}</td></tr>
            <tr><th>验证日（T+1 收盘）</th><td>{timeline.get('verify_date', 'N/A')}</td><th>生成时间（北京时间）</th><td>{payload.get('generated_at_beijing', payload['generated_at'])}</td></tr>
          </tbody>
        </table>
        <div class="signal {signal_class}">{predicted_direction}</div>
        <div class="decision-text">次日{'看涨' if predicted_direction == 'UP' else '看跌' if predicted_direction == 'DOWN' else '方向不可用'} · {d['signal_cn']} · {d['suggested_action']}</div>
        <table class="timeline-table pair-table" aria-label="实时行情数据表">
          <tbody>
            <tr><th>行情数据时间（北京时间）</th><td>{_market_data_time(market)}</td><th>行情基准价</th><td>{fmt_number(market.get('latest_close'))}</td></tr>
            <tr><th>基准价涨跌幅</th><td>{fmt_pct_points(market.get('latest_pct_chg'))}</td><th>累计成交额</th><td>{fmt_amount_yi(market.get('latest_amount'))}</td></tr>
            <tr><th>行情截止时间</th><td>{market.get('asof_time', 'N/A')}</td><th>预测口径</th><td>{_prediction_basis_text(market.get('prediction_basis', p.get('prediction_basis')))}</td></tr>
            <tr><th>MA20</th><td>{fmt_number(market.get('ma20'))}</td><th>MA5</th><td>{fmt_number(market.get('ma5'))}</td></tr>
          </tbody>
        </table>
        <div class="hero-grid">
          <div class="metric"><div class="label">次日预测方向</div><div class="value">{predicted_direction}</div></div>
          <div class="metric"><div class="label">次日上涨概率</div><div class="value">{probability_pct(p['prob_up_1d'])}</div></div>
          <div class="metric"><div class="label">T+1 历史准确率</div><div class="value">{probability_pct(t1_std.get('directional_accuracy'))}</div></div>
          <div class="metric"><div class="label">实盘方向准确率</div><div class="value">{_live_accuracy_text(live_stats)}</div></div>
          <div class="metric"><div class="label">风险调整 EV</div><div class="value">{pct(ev['risk_adjusted_ev'])}</div></div>
          <div class="metric"><div class="label">风险等级</div><div class="value">{risk['risk_level_cn']}</div></div>
        </div>
      </div>
    </div>
  </div>
  <section><h2>5D / 10D / 20D 价格预测分布</h2><div class="grid">
    {_price_distribution_tables(price_paths)}
  </div><p class="note">来自 V1.3 路径分布层的 P2 状态条件路径；只展示价格分布参考，不代表确定收益。</p></section>
  <section><h2>T+1 涨跌预测</h2><table class="timeline-table" aria-label="概率判断表">
    <tbody>
      <tr><th>明天上涨概率</th><td>{probability_pct(p['prob_up_1d'])}</td><th>明天下跌概率</th><td>{probability_pct(p['prob_down_1d'])}</td></tr>
      <tr><th>大涨概率</th><td>{probability_pct(dist['return_bins_1d']['gt_5pct'])}</td><th>大跌概率</th><td>{probability_pct(dist['return_bins_1d']['lt_minus_5pct'])}</td></tr>
    </tbody>
  </table></section>
  <section><h2>EV 与性价比</h2><div class="grid">
    <div class="metric"><div class="label">原始 EV</div><div class="value">{pct(ev['raw_ev'])}</div></div>
    <div class="metric"><div class="label">成本调整 EV</div><div class="value">{pct(ev['cost_adjusted_ev'])}</div></div>
    <div class="metric"><div class="label">风险调整 EV</div><div class="value">{pct(ev['risk_adjusted_ev'])}</div></div>
    <div class="metric"><div class="label">交易性价比</div><div class="value">{ev['ev_rating_cn']}</div></div>
  </div><p class="note">EV 为长期重复同类交易时的期望收益，单次交易仍可能亏损。</p></section>
  <section><h2>风控状态</h2><div class="grid">
    <div class="metric"><div class="label">当前风险</div><div class="value">{risk['risk_level_cn']}</div></div>
    <div class="metric"><div class="label">风控状态</div><div class="value">{'已拦截' if risk['buy_blocked'] else '通过'}</div></div>
    <div class="metric"><div class="label">主要风险</div><div class="value long-text">{'；'.join(risk.get('buy_block_reasons') or risk.get('warnings') or ['无硬拦截'])}</div></div>
  </div><p class="note">{risk['human_risk_explanation']}</p></section>
  <section><h2>仓位与退出</h2><div class="grid">
    <div class="metric"><div class="label">建议仓位</div><div class="value">{d['position_range']}</div><p class="note">不建议满仓，不建议加杠杆。</p></div>
    <div class="metric"><div class="label">止盈参考</div><div class="value">{exit_plan['take_profit_range']}</div></div>
    <div class="metric"><div class="label">止损参考</div><div class="value">{exit_plan['stop_loss_reference']}</div></div>
    <div class="metric"><div class="label">时间退出</div><div class="value">{exit_plan['time_exit_days']} 个交易日</div></div>
  </div></section>
  <section><h2>模型表现追踪</h2><div class="three-grid">
    <div class="metric"><div class="label">T+1 扩展窗口</div><div class="value">{probability_pct(historical_stats.get('direction_accuracy'))}</div><p class="note">样本数：{fmt_count(historical_stats.get('sample_count'))}</p><p class="note">95% 区间：{probability_pct(historical_stats.get('accuracy_ci_95_low'))} ~ {probability_pct(historical_stats.get('accuracy_ci_95_high'))}</p></div>
    <div class="metric"><div class="label">{live_stats.get('name', '实盘统计线')}</div><div class="value">{_live_accuracy_text(live_stats)}</div><p class="note">起始：{live_stats.get('start_date', 'N/A')} · 样本：{live_stats.get('sample_count', 0)}</p><p class="note">正确：{live_stats.get('correct_count', 0)} · 错误：{live_stats.get('wrong_count', 0)}</p></div>
    <div class="metric"><div class="label">高置信子集</div><div class="value">{probability_pct(t1_std.get('high_confidence_accuracy'))}</div><p class="note">覆盖率：{probability_pct(t1_std.get('high_confidence_coverage'))}</p><p class="note">验证 Brier：{fmt_number(t1_std.get('brier_active', t1_std.get('brier_calibrated')))} · AUC：{fmt_number(t1_std.get('roc_auc'))}</p></div>
  </div></section>
  <section><h2>人工执行说明</h2>
    <span class="pill">自动下单 <strong>关闭</strong></span>
    <span class="pill">券商接口 <strong>关闭</strong></span>
    <span class="pill">人工参考 <strong>是</strong></span>
    <p class="note">{payload['human_explanation']['execution_note']}</p>
  </section>
  <div class="footer">生成时间（北京时间）：{payload.get('generated_at_beijing', payload['generated_at'])} · 数据交易日：{payload['trade_date']} · 交易时段每 20 分钟更新，收盘后生成最终版</div>
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


def fmt_pct_points(value: Any, digits: int = 2) -> str:
    if value is None:
        return "N/A"
    try:
        return f"{float(value):.{digits}f}%"
    except (TypeError, ValueError):
        return "N/A"


def fmt_amount(value: Any) -> str:
    if value is None:
        return "N/A"
    try:
        return f"{float(value):,.2f}"
    except (TypeError, ValueError):
        return "N/A"


def fmt_amount_yi(value: Any) -> str:
    if value is None:
        return "N/A"
    try:
        return f"{float(value) / 100000:.2f} 亿"
    except (TypeError, ValueError):
        return "N/A"


def fmt_count(value: Any) -> str:
    if value is None:
        return "--"
    try:
        return str(int(value))
    except (TypeError, ValueError):
        return "--"


def _prediction_basis_text(value: Any) -> str:
    if value == "next_trading_day_close_vs_current_trade_day_close":
        return "次交易日官方收盘价 vs 本交易日官方收盘价"
    if value == "next_trading_day_close_vs_daily_close":
        return "次交易日收盘相对当日收盘"
    return str(value or "N/A")


def _market_data_time(market: dict[str, Any]) -> str:
    explicit = market.get("asof_datetime_beijing")
    if explicit:
        return str(explicit)
    trade_date = market.get("latest_trade_date")
    asof_time = market.get("asof_time")
    if trade_date and asof_time:
        return f"{trade_date} {str(asof_time)[:5]}"
    return "N/A"


def _live_accuracy_text(live_stats: dict[str, Any]) -> str:
    if not live_stats.get("sample_count"):
        return "暂无样本"
    return probability_pct(live_stats.get("direction_accuracy"))


def _price_distribution_markdown(price_paths: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for horizon in ("5D", "10D", "20D"):
        node = price_paths.get(horizon) or {}
        lines.extend(
            [
                f"- {horizon}: P10 {fmt_number(node.get('terminal_price_p10'))} / P50 {fmt_number(node.get('terminal_price_p50'))} / P90 {fmt_number(node.get('terminal_price_p90'))}",
                f"  - 期末上涨概率: {probability_pct(node.get('positive_terminal_prob'))}; 样本数: {fmt_count(node.get('sample_size'))}",
            ]
        )
    return lines


def _price_distribution_tables(price_paths: dict[str, Any]) -> str:
    tables = []
    for horizon in ("5D", "10D", "20D"):
        node = price_paths.get(horizon) or {}
        tables.append(
            f"""<div><h3>{horizon} 预测分布</h3><table class="timeline-table" aria-label="{horizon} 价格预测分布表"><tbody><tr><th>P10</th><td>{fmt_number(node.get('terminal_price_p10'))}</td><th>P50</th><td>{fmt_number(node.get('terminal_price_p50'))}</td></tr><tr><th>P90</th><td>{fmt_number(node.get('terminal_price_p90'))}</td><th>期末上涨概率</th><td>{probability_pct(node.get('positive_terminal_prob'))}</td></tr><tr><th>样本数</th><td>{fmt_count(node.get('sample_size'))}</td><th>模型层</th><td>P2</td></tr></tbody></table></div>"""
        )
    return "\n    ".join(tables)
