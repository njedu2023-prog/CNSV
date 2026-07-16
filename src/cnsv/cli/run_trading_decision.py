from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from cnsv.cli.run_live_manual_decision import main as run_live_manual_decision_main
from cnsv.data.downloader import fetch_parquet
from cnsv.data.loader import remote_url
from cnsv.data.tushare_realtime import (
    build_realtime_ready,
    fetch_realtime_minutes,
    merge_intraday_history,
)
from cnsv.trading.evidence_loader import load_trading_evidence
from cnsv.trading.fusion import build_trading_decision_payload
from cnsv.trading.live_stats import build_model_performance, update_live_stats_registry
from cnsv.trading.live_html import write_live_trading_html
from cnsv.trading.report import write_trading_json, write_trading_markdown, write_trading_registry
from cnsv.utils.io import load_default_config, repo_root


def main() -> int:
    root = repo_root()
    if not (root / "docs/data/latest_live_manual_decision_report.json").exists():
        code = run_live_manual_decision_main()
        if code != 0:
            raise RuntimeError("failed to generate V2.0 live manual decision evidence")
    evidence = load_trading_evidence(root)
    _attach_trade_calendar(evidence)
    _attach_daily_price_history(evidence)
    _attach_moneyflow_history(evidence)
    realtime_ready = _attach_intraday_history(evidence)
    if not realtime_ready["ready"]:
        reason = realtime_ready.get("blocking_reason") or "realtime_not_ready"
        if realtime_ready.get("status") == "FAIL":
            raise RuntimeError(f"CNSV direct Tushare realtime gate failed: {reason}")
        print(f"trading_decision=SKIP reason={reason}")
        return 0
    payload = build_trading_decision_payload(evidence)
    live_registry = update_live_stats_registry(
        payload,
        root / "docs/data/live_stats_registry.json",
        evidence["reports"],
    )
    payload["model_performance"] = build_model_performance(payload["historical_validation"], live_registry)
    write_trading_json(payload, root / "docs/data/latest_trading_decision_report.json")
    write_trading_registry(root / "docs/data/trading_decision_registry.json")
    write_trading_markdown(payload, root / "reports/latest_trading_decision_report.md", root / "reports/archive")
    write_live_trading_html(payload, root / "docs/trading.html")
    _ensure_trading_entry(root / "docs/index.html")
    decision = payload["decision"]
    risk = payload["risk"]
    print(
        "trading_decision="
        f"{decision['signal']} position={decision['position_range']} risk={risk['risk_level']} "
        f"auto_order={payload['auto_order_enabled']} broker_api={payload['broker_api_enabled']}"
    )
    return 0


def _attach_trade_calendar(evidence):
    try:
        source_config = load_default_config()["data_source"]
        evidence["trade_calendar"] = fetch_parquet(remote_url(source_config, "trade_calendar"), timeout=8)
        evidence["trade_calendar_source"] = "CNSVdata trade_calendar"
    except Exception as exc:
        evidence["trade_calendar"] = None
        evidence["trade_calendar_source"] = "unavailable"
        evidence["trade_calendar_error"] = str(exc)


def _attach_daily_price_history(evidence):
    try:
        source_config = load_default_config()["data_source"]
        evidence["reports"]["daily_price_history"] = fetch_parquet(remote_url(source_config, "daily"), timeout=8)
        evidence["daily_price_history_source"] = "CNSVdata daily"
    except Exception as exc:
        evidence["reports"]["daily_price_history"] = None
        evidence["daily_price_history_source"] = "unavailable"
        evidence["daily_price_history_error"] = str(exc)


def _attach_moneyflow_history(evidence):
    try:
        source_config = load_default_config()["data_source"]
        evidence["reports"]["moneyflow_history"] = fetch_parquet(remote_url(source_config, "moneyflow"), timeout=8)
        evidence["moneyflow_history_source"] = "CNSVdata moneyflow"
    except Exception as exc:
        evidence["reports"]["moneyflow_history"] = None
        evidence["moneyflow_history_source"] = "unavailable"
        evidence["moneyflow_history_error"] = str(exc)


def _attach_intraday_history(evidence):
    now = datetime.now(ZoneInfo("Asia/Shanghai"))
    preflight = build_realtime_ready(None, now=now, trade_calendar=evidence.get("trade_calendar"))
    if preflight.get("blocking_reason") != "tushare_realtime_minutes_unavailable":
        evidence["reports"]["intraday_realtime_ready"] = preflight
        evidence["reports"]["intraday_minute_history"] = None
        return preflight
    current = fetch_realtime_minutes(now=now)
    ready = build_realtime_ready(current, now=now, trade_calendar=evidence.get("trade_calendar"))
    evidence["reports"]["intraday_realtime_ready"] = ready
    evidence["intraday_history_source"] = "Tushare rt_min_daily direct realtime"
    if not ready["ready"]:
        evidence["reports"]["intraday_minute_history"] = None
        return ready

    source_config = load_default_config()["data_source"]
    historical = fetch_parquet(remote_url(source_config, "intraday_minute_history"), timeout=30)
    evidence["reports"]["intraday_minute_history"] = merge_intraday_history(historical, current)
    evidence["intraday_history_source"] = "Tushare rt_min_daily + CNSVdata historical 1min"
    return ready


def _ensure_trading_entry(path):
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    if 'href="trading.html"' not in text:
        text = text.replace("</nav>", '<a href="trading.html">V3.0 交易决策</a></nav>', 1)
    text = text.replace("CNSV V2.0 主线看板", "CNSV V3.0 主线看板")
    text = text.replace("中国船舶主线看板", "中国船舶主线决策看板")
    text = text.replace("V2.0 实盘人工决策入口。页面不生成交易动作。", "V2.0 实盘人工决策入口与 V3.0 人工交易决策参考。页面不自动下单。")
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
