from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS, clean_payload
from cnsv.support import SUPPORT_REPORT_TYPE, SUPPORT_STAGE, SUPPORT_VERSION
from cnsv.support.evidence_loader import status_of


def build_human_decision_support_payload(evidence_bundle: dict[str, Any]) -> dict[str, Any]:
    reports = evidence_bundle["reports"]
    availability = evidence_bundle["evidence_availability"]
    data = reports.get("data_report") or {}
    feature = reports.get("feature_report") or {}
    baseline = reports.get("baseline_model_report") or {}
    path = reports.get("path_distribution_report") or {}
    backtest = reports.get("observation_backtest_report") or {}
    features = feature.get("features") or {}
    price = features.get("price_volume") or {}
    trend = features.get("trend") or {}
    volatility = features.get("volatility") or {}
    moneyflow = features.get("moneyflow") or {}
    quality_statuses = {
        "data_quality": status_of(data, "validation"),
        "feature_quality": status_of(feature, "feature_quality"),
        "baseline_quality": status_of(baseline, "baseline_quality"),
        "path_quality": status_of(path, "path_quality"),
        "observation_backtest_quality": status_of(backtest, "observation_backtest_quality"),
    }
    conflict_reasons = [f"{k}={v}" for k, v in quality_statuses.items() if v not in {"PASS", "N/A"}]
    payload: dict[str, Any] = {
        "meta": {
            "system": "CNSV",
            "version": SUPPORT_VERSION,
            "stage": SUPPORT_STAGE,
            "report_type": SUPPORT_REPORT_TYPE,
            "ts_code": "600150.SH",
            "name": "中国船舶",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "latest_trade_date": _latest_trade_date(data, feature, baseline, path, backtest),
            "is_trade_signal": False,
        },
        "cnsvdata_gate": _stage_gate(data.get("cnsvdata_gate") or feature.get("cnsvdata_gate") or {}),
        "evidence_availability": availability,
        "current_state_summary": {
            "latest_trade_date": price.get("latest_trade_date") or (feature.get("meta") or {}).get("latest_trade_date"),
            "latest_close": price.get("latest_close") or (baseline.get("current_state") or {}).get("latest_close"),
            "trend_state": trend.get("trend_state") or (baseline.get("current_state") or {}).get("trend_state"),
            "volatility_state": volatility.get("volatility_state") or (baseline.get("current_state") or {}).get("volatility_state"),
            "flow_strength_basic": moneyflow.get("flow_strength_basic") or (baseline.get("current_state") or {}).get("flow_strength_basic"),
            "data_quality_status": quality_statuses["data_quality"],
            "feature_quality_status": quality_statuses["feature_quality"],
        },
        "model_evidence_summary": {
            "observation_backtest_summary": {
                "quality_status": quality_statuses["observation_backtest_quality"],
                "standard_sample_size": (backtest.get("backtest_scope") or {}).get("standard_sample_size"),
                "purged_sample_size": (backtest.get("backtest_scope") or {}).get("purged_sample_size"),
                "leakage_status": (backtest.get("observation_backtest_leakage_checks") or {}).get("status"),
            },
            "model_support_summary": {
                "baseline_models": list((baseline.get("baseline_models") or {}).keys()),
                "path_models": list((path.get("path_models") or {}).keys()),
                "p2_role": "辅助状态层，不作为核心决策依赖",
            },
        },
        "path_opportunity_observation": _path_snapshot(path, "opportunity"),
        "path_risk_observation": _path_snapshot(path, "risk"),
        "model_consistency_summary": {
            "model_consistency_level": "人工复核",
            "model_disagreement_points": [],
            "p2_role": "辅助状态层，不作为核心决策依赖",
        },
        "evidence_conflict_summary": {"evidence_conflict": bool(conflict_reasons), "evidence_conflict_reasons": conflict_reasons},
        "human_attention_items": [{"category": "evidence_items", "text": "上游证据已汇总，仍需人工结合市场与行业背景复核。"}],
        "human_review_checklist": [
            {"id": "data_freshness", "text": "确认 latest_trade_date 与当前人工复核日期是否匹配。"},
            {"id": "market_context", "text": "确认当天市场环境是否存在外部冲击。"},
            {"id": "path_risk", "text": "复核路径概率、回撤和风险解释。"},
        ],
        "support_levels": {
            "observation_priority": "medium",
            "risk_attention_level": "medium",
            "evidence_strength": "moderate" if not availability.get("missing_reports") else "insufficient",
            "model_consistency_level": "人工复核",
            "human_review_required": True,
        },
        "upstream_quality_statuses": quality_statuses,
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "next_stage": "V1.6 risk explanation",
    }
    payload["human_decision_support_quality"] = _evaluate(payload)
    return clean_payload(payload)


def _stage_gate(gate: dict[str, Any]) -> dict[str, Any]:
    out = dict(gate)
    out["can_generate_formal_signal"] = False
    out["can_auto_order"] = False
    out["can_connect_broker_api"] = False
    return out


def _latest_trade_date(*reports: dict[str, Any]) -> str:
    for report in reports:
        value = (report.get("meta") or {}).get("latest_trade_date") or (report.get("data_manifest") or {}).get("latest_trade_date")
        if value:
            return str(value)
    return "N/A"


def _path_snapshot(path: dict[str, Any], kind: str) -> dict[str, Any]:
    p1 = (((path.get("path_models") or {}).get("P1_volatility_adjusted_path") or {}).get("horizons") or {}).get("20D") or {}
    if kind == "opportunity":
        return {
            "positive_terminal_observation": p1.get("positive_terminal_prob"),
            "touch_up_observation": p1.get("touch_up_5pct_prob"),
            "evidence_strength": "观察项，仅供人工复核",
        }
    return {
        "downside_path_observation": p1.get("touch_down_5pct_prob"),
        "drawdown_observation": p1.get("max_drawdown_p50"),
        "risk_attention_level": "medium",
    }


def _evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    missing = payload.get("evidence_availability", {}).get("missing_reports", [])
    conflict = payload.get("evidence_conflict_summary", {}).get("evidence_conflict")
    checks = [
        {"name": "is_trade_signal_false", "status": "PASS", "detail": "V1.5 remains human decision support only"},
        {"name": "forbidden_actions_present", "status": "PASS", "detail": "formal signal and auto order remain forbidden"},
        {"name": "upstream_reports_available", "status": "WARN" if missing else "PASS", "detail": f"missing_reports={missing}"},
        {"name": "human_review_required", "status": "WARN", "detail": "manual review remains required"},
        {"name": "evidence_conflict", "status": "WARN" if conflict else "PASS", "detail": "conflicts are non-blocking human-review items"},
    ]
    failed = sum(1 for item in checks if item["status"] == "FAIL")
    warn = sum(1 for item in checks if item["status"] == "WARN")
    return {"status": "FAIL" if failed else "WARN" if warn else "PASS", "failed_count": failed, "warn_count": warn, "blocking_error_count": failed, "checks": checks}
