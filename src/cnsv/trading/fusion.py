from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any

import pandas as pd

from cnsv.trading import FORBIDDEN_TRADING_AUTOMATION, TRADING_REPORT_TYPE, TRADING_STAGE, TRADING_VERSION
from cnsv.trading.ev_engine import compute_ev
from cnsv.trading.exit_engine import compute_exit_plan
from cnsv.trading.live_stats import build_model_performance, predicted_direction
from cnsv.trading.position_engine import compute_position
from cnsv.trading.probability import compute_next_day_probability
from cnsv.trading.return_distribution import compute_return_distribution
from cnsv.trading.risk_control import evaluate_trading_risk
from cnsv.trading.signal_engine import decide_signal
from cnsv.trading.utils import pct

CN_MARKET_HOLIDAY_FALLBACK = {
    "2026-01-01",
    "2026-02-16",
    "2026-02-17",
    "2026-02-18",
    "2026-02-19",
    "2026-02-20",
    "2026-02-23",
    "2026-04-06",
    "2026-05-01",
    "2026-05-04",
    "2026-05-05",
    "2026-06-19",
    "2026-09-25",
    "2026-10-01",
    "2026-10-02",
    "2026-10-05",
    "2026-10-06",
    "2026-10-07",
}


def build_trading_decision_payload(evidence_bundle: dict[str, Any]) -> dict[str, Any]:
    reports = evidence_bundle["reports"]
    probability = compute_next_day_probability(reports)
    distribution = compute_return_distribution(reports, probability)
    ev = compute_ev(distribution)
    risk = evaluate_trading_risk(reports, probability, distribution, ev)
    signal = decide_signal(probability, distribution, ev, risk)
    position = compute_position(signal, probability, ev, risk)
    exit_plan = compute_exit_plan(reports, distribution, risk)
    historical_validation = _historical_validation(reports)
    data_report = reports.get("data_report") or {}
    feature_report = reports.get("feature_report") or {}
    meta = feature_report.get("meta") or data_report.get("meta") or {}
    features = feature_report.get("features") or {}
    price_volume = features.get("price_volume") or {}
    trade_date = meta.get("latest_trade_date") or (data_report.get("data_manifest") or {}).get("latest_trade_date") or "N/A"
    decision = {
        **signal,
        **position,
    }
    timeline = _decision_timeline(trade_date, decision, evidence_bundle)
    market_snapshot = {
        "latest_trade_date": price_volume.get("latest_trade_date") or trade_date,
        "latest_close": price_volume.get("latest_close"),
        "latest_pct_chg": price_volume.get("latest_pct_chg"),
        "latest_amount": price_volume.get("latest_amount"),
        "ma5": price_volume.get("ma5"),
        "ma20": price_volume.get("ma20"),
    }
    payload = {
        "version": TRADING_VERSION,
        "stage": TRADING_STAGE,
        "report_type": TRADING_REPORT_TYPE,
        "symbol": "600150.SH",
        "name": "中国船舶",
        "trade_date": trade_date,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data_status": ((data_report.get("cnsvdata_gate") or {}).get("status") or "N/A"),
        "is_trade_signal": signal["signal"] not in {"BLOCKED", "WATCH"},
        "manual_reference_only": True,
        "auto_order_enabled": False,
        "broker_api_enabled": False,
        "direct_execution_enabled": False,
        "forbidden_actions": FORBIDDEN_TRADING_AUTOMATION,
        "cnsvdata_gate": data_report.get("cnsvdata_gate") or {},
        "decision": decision,
        "decision_timeline": timeline,
        "market_snapshot": market_snapshot,
        "price_prediction_distribution": _price_prediction_distribution(reports),
        "probability": probability,
        "return_distribution": distribution,
        "ev": ev,
        "risk": risk,
        "exit": exit_plan,
        "historical_validation": historical_validation,
        "model_performance": build_model_performance(historical_validation),
        "human_explanation": _human_explanation(decision, probability, ev, risk),
        "model_sources": _model_sources(reports),
        "missing_reports": evidence_bundle.get("missing_reports", []),
    }
    if evidence_bundle.get("missing_reports"):
        payload["decision"]["signal"] = "BLOCKED"
        payload["decision"]["signal_cn"] = "风控阻断"
        payload["decision"]["suggested_action"] = "缺少上游证据，不允许输出买卖建议"
        payload["decision"]["suggested_position_pct"] = 0.0
        payload["decision"]["position_range"] = "0%"
        payload["risk"]["blocked"] = True
        payload["risk"]["risk_passed"] = False
        payload["risk"]["block_reasons"] = payload["risk"].get("block_reasons", []) + ["缺少上游报告"]
        payload["is_trade_signal"] = False
    return payload


def _decision_timeline(trade_date: str, decision: dict[str, Any], evidence_bundle: dict[str, Any]) -> dict[str, Any]:
    signal_date = date.today().isoformat()
    calendar_dates = _open_trade_dates(evidence_bundle.get("trade_calendar"))
    prediction_date, prediction_source = _next_trade_date(trade_date, calendar_dates)
    verify_date, verify_source = _next_trade_date(prediction_date, calendar_dates)
    calendar_source = evidence_bundle.get("trade_calendar_source")
    if not calendar_source:
        calendar_source = "CNSVdata trade_calendar" if calendar_dates else "fallback_cn_market_holiday_business_day"
    return {
        "data_trade_date": trade_date,
        "signal_date": signal_date,
        "prediction_date": prediction_date,
        "verify_date": verify_date,
        "predicted_direction": predicted_direction({"decision": decision}),
        "calendar_source": calendar_source,
        "prediction_date_source": prediction_source,
        "verify_date_source": verify_source,
    }


def _open_trade_dates(calendar: Any) -> list[str]:
    if calendar is None:
        return []
    if isinstance(calendar, pd.DataFrame):
        if calendar.empty:
            return []
        frame = calendar.copy()
        date_col = "trade_date" if "trade_date" in frame.columns else "cal_date" if "cal_date" in frame.columns else frame.columns[0]
        if "is_open" in frame.columns:
            frame = frame[frame["is_open"].astype(int) == 1]
        dates = frame[date_col].astype(str).map(_date_text).dropna().tolist()
        return sorted(set(dates))
    if isinstance(calendar, dict):
        values = calendar.get("open_dates") or calendar.get("trade_dates") or calendar.get("dates") or []
    else:
        values = calendar
    if isinstance(values, (list, tuple, set)):
        dates = [_date_text(value) for value in values]
        return sorted({value for value in dates if value})
    return []


def _next_trade_date(current: str, open_dates: list[str]) -> tuple[str, str]:
    current_date = _date_text(current)
    if open_dates and current_date:
        for item in open_dates:
            if item > current_date:
                return item, "trade_calendar"
    return _next_business_day(current_date), "fallback_cn_market_holiday_business_day"


def _next_business_day(current: str) -> str:
    try:
        day = date.fromisoformat(current)
    except (TypeError, ValueError):
        day = date.today()
    day += timedelta(days=1)
    while day.weekday() >= 5 or day.isoformat() in CN_MARKET_HOLIDAY_FALLBACK:
        day += timedelta(days=1)
    return day.isoformat()


def _date_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)[:10]
    if len(text) == 8 and text.isdigit():
        return f"{text[:4]}-{text[4:6]}-{text[6:8]}"
    return text


def _historical_validation(reports: dict[str, Any]) -> dict[str, Any]:
    baseline = reports.get("baseline_validation_report") or {}
    path_validation = reports.get("path_validation_report") or {}
    backtest = reports.get("observation_backtest_report") or {}
    b2_standard = _metric(
        baseline,
        "model_metrics",
        "standard_walk_forward_metrics",
        "B2_state_grouped_distribution",
        "5D",
    )
    b2_purged = _metric(
        baseline,
        "model_metrics",
        "purged_walk_forward_metrics",
        "B2_state_grouped_distribution",
        "5D",
    )
    p2_standard = _metric(
        path_validation,
        "standard_walk_forward_metrics",
        "P2_state_conditional_path",
        "5D",
    )
    p2_purged = _metric(
        path_validation,
        "purged_walk_forward_metrics",
        "P2_state_conditional_path",
        "5D",
    )
    obs_standard = _metric(
        backtest,
        "model_backtest_metrics",
        "standard_walk_forward",
        "P2_state_conditional_path",
        "5D",
    )
    obs_purged = _metric(
        backtest,
        "model_backtest_metrics",
        "purged_walk_forward",
        "P2_state_conditional_path",
        "5D",
    )
    return {
        "scope": "5D walk-forward validation; used as V3.0 probability evidence, not profit guarantee",
        "baseline_directional_accuracy": {
            "model": "B2_state_grouped_distribution",
            "horizon": "5D",
            "standard": _pick(
                b2_standard,
                "sample_size",
                "directional_accuracy",
                "positive_prob_brier",
                "p10_p90_interval_coverage",
            ),
            "purged": _pick(
                b2_purged,
                "sample_size",
                "directional_accuracy",
                "positive_prob_brier",
                "p10_p90_interval_coverage",
            ),
        },
        "path_probability_validation": {
            "model": "P2_state_conditional_path",
            "horizon": "5D",
            "standard": _pick(
                p2_standard,
                "sample_size",
                "positive_terminal_brier",
                "terminal_p10_p90_coverage",
                "path_interval_coverage",
            ),
            "purged": _pick(
                p2_purged,
                "sample_size",
                "positive_terminal_brier",
                "terminal_p10_p90_coverage",
                "path_interval_coverage",
            ),
        },
        "observation_backtest": {
            "model": "P2_state_conditional_path",
            "horizon": "5D",
            "standard": _pick(
                obs_standard,
                "sample_size",
                "actual_positive_terminal_rate",
                "positive_terminal_brier",
                "terminal_p10_p90_coverage",
                "model_coverage_rate",
            ),
            "purged": _pick(
                obs_purged,
                "sample_size",
                "actual_positive_terminal_rate",
                "positive_terminal_brier",
                "terminal_p10_p90_coverage",
                "model_coverage_rate",
            ),
        },
        "interpretation": "方向准确率来自 B2 5D walk-forward；路径概率使用 Brier 分数和区间覆盖率衡量，Brier 越低越好。",
    }


def _metric(data: dict[str, Any], *keys: str) -> dict[str, Any]:
    node: Any = data
    for key in keys:
        if not isinstance(node, dict):
            return {}
        node = node.get(key)
    return node if isinstance(node, dict) else {}


def _pick(data: dict[str, Any], *keys: str) -> dict[str, Any]:
    return {key: data.get(key) for key in keys}


def _human_explanation(decision: dict[str, Any], probability: dict[str, Any], ev: dict[str, Any], risk: dict[str, Any]) -> dict[str, str]:
    signal = decision["signal"]
    if signal == "BLOCKED":
        summary = "当前数据或模型条件不满足交易决策要求，不允许输出买卖建议。"
    elif signal in {"BUY", "STRONG_BUY"}:
        summary = f"模型认为次日上涨概率为 {pct(probability['prob_up_1d'])}，风险调整 EV 为 {pct(ev['risk_adjusted_ev'])}，可作为人工轻仓参与参考。"
    elif signal in {"SELL", "STRONG_SELL"}:
        summary = "下行概率、EV 或尾部风险触发卖出条件，应优先降低风险暴露。"
    elif signal == "REDUCE":
        summary = "风险收益比转弱，继续满仓持有的性价比下降。"
    elif signal == "HOLD":
        summary = "当前信号未触发卖出，持仓可继续观察。"
    else:
        summary = "信号强度不足，建议继续观察，不建议主动买入。"
    return {
        "summary": summary,
        "risk_note": risk.get("human_risk_explanation") or "单次交易仍可能亏损，禁止满仓和加杠杆。",
        "execution_note": "所有信号、仓位、止盈止损均为人工参考，不代表自动交易指令。",
    }


def _model_sources(reports: dict[str, Any]) -> dict[str, Any]:
    return {
        "baseline_models": list(((reports.get("baseline_model_report") or {}).get("baseline_models") or {}).keys()),
        "path_models": list(((reports.get("path_distribution_report") or {}).get("path_models") or {}).keys()),
        "risk_report_stage": ((reports.get("risk_explanation_report") or {}).get("meta") or {}).get("stage"),
        "live_report_stage": ((reports.get("live_manual_decision_report") or {}).get("meta") or {}).get("stage"),
    }


def _price_prediction_distribution(reports: dict[str, Any]) -> dict[str, Any]:
    path = reports.get("path_distribution_report") or {}
    models = path.get("path_models") or {}
    preferred = models.get("P2_state_conditional_path") or models.get("P1_volatility_adjusted_path") or models.get("P0_historical_path_replay") or {}
    horizons = preferred.get("horizons") or {}
    output: dict[str, Any] = {}
    for horizon in ("5D", "10D", "20D"):
        node = horizons.get(horizon) or {}
        output[horizon] = {
            "model_id": node.get("model_id") or preferred.get("model_id"),
            "source_model": node.get("source_model"),
            "latest_close": node.get("latest_close"),
            "terminal_price_p10": node.get("terminal_price_p10"),
            "terminal_price_p50": node.get("terminal_price_p50"),
            "terminal_price_p90": node.get("terminal_price_p90"),
            "terminal_return_p10": node.get("terminal_return_p10"),
            "terminal_return_p50": node.get("terminal_return_p50"),
            "terminal_return_p90": node.get("terminal_return_p90"),
            "positive_terminal_prob": node.get("positive_terminal_prob"),
            "sample_size": node.get("sample_size"),
            "state_sample_size": node.get("state_sample_size"),
            "fallback_used": node.get("fallback_used", False),
            "fallback_reason": node.get("fallback_reason") or node.get("skipped_reason") or "",
        }
    return output
