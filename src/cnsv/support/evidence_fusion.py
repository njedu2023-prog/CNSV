from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS, clean_payload
from cnsv.support import SUPPORT_REPORT_TYPE, SUPPORT_STAGE, SUPPORT_VERSION
from cnsv.support.attention_items import build_human_attention_items
from cnsv.support.consistency import build_model_consistency_summary
from cnsv.support.evidence_loader import status_of
from cnsv.support.review_checklist import build_human_review_checklist
from cnsv.support.support_evaluator import evaluate_human_decision_support
from cnsv.support.support_levels import classify_evidence_strength, classify_risk_attention, derive_support_levels


def build_human_decision_support_payload(evidence_bundle: dict[str, Any]) -> dict[str, Any]:
    reports = evidence_bundle["reports"]
    availability = evidence_bundle["evidence_availability"]
    data = reports.get("data_report") or {}
    feature = reports.get("feature_report") or {}
    baseline = reports.get("baseline_model_report") or {}
    baseline_validation = reports.get("baseline_validation_report") or {}
    path = reports.get("path_distribution_report") or {}
    path_validation = reports.get("path_validation_report") or {}
    backtest = reports.get("observation_backtest_report") or {}
    features = feature.get("features") or {}
    price = features.get("price_volume") or {}
    trend = features.get("trend") or {}
    volatility = features.get("volatility") or {}
    moneyflow = features.get("moneyflow") or {}
    path_models = path.get("path_models") or {}
    baseline_models = baseline.get("baseline_models") or {}
    comparison = (backtest.get("model_comparison") or {}).get("standard_walk_forward") or {}
    quality_statuses = {
        "data_quality": status_of(data, "validation"),
        "feature_quality": status_of(feature, "feature_quality"),
        "baseline_quality": status_of(baseline, "baseline_quality"),
        "validation_quality": status_of(baseline_validation, "validation_quality"),
        "path_quality": status_of(path, "path_quality"),
        "path_validation_quality": status_of(path_validation, "path_validation_quality"),
        "observation_backtest_quality": status_of(backtest, "observation_backtest_quality"),
        "leakage_checks": str((backtest.get("observation_backtest_leakage_checks") or {}).get("status") or "MISSING"),
    }
    standard_sample = int((backtest.get("backtest_scope") or {}).get("standard_sample_size") or 0)
    purged_sample = int((backtest.get("backtest_scope") or {}).get("purged_sample_size") or 0)
    high_fallback = _p2_fallback_high(backtest)
    evidence_strength = classify_evidence_strength(quality_statuses, standard_sample, purged_sample, high_fallback)
    risk_attention = classify_risk_attention(path_models)
    consistency = build_model_consistency_summary(baseline_models, path_models, comparison)
    evidence_conflict, conflict_reasons = _evidence_conflicts(path_models, comparison, quality_statuses, high_fallback)
    support_levels = derive_support_levels(evidence_strength, consistency["model_consistency_level"], risk_attention, evidence_conflict, availability.get("missing_reports", []))
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
                "standard_sample_size": standard_sample,
                "purged_sample_size": purged_sample,
                "leakage_status": (backtest.get("observation_backtest_leakage_checks") or {}).get("status"),
            },
            "model_support_summary": {
                "baseline_models": list(baseline_models.keys()),
                "path_models": list(path_models.keys()),
                "p2_role": "辅助状态层，不作为核心决策依赖",
            },
        },
        "path_opportunity_observation": _path_snapshot(path_models, "opportunity"),
        "path_risk_observation": _path_snapshot(path_models, "risk"),
        "model_consistency_summary": consistency,
        "evidence_conflict_summary": {"evidence_conflict": evidence_conflict, "evidence_conflict_reasons": conflict_reasons},
        "human_attention_items": [],
        "human_review_checklist": build_human_review_checklist(),
        "support_levels": support_levels,
        "upstream_quality_statuses": quality_statuses,
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "next_stage": "V1.6 risk explanation",
    }
    payload["human_attention_items"] = build_human_attention_items(availability, support_levels, consistency, conflict_reasons)
    payload["human_decision_support_quality"] = evaluate_human_decision_support(payload)
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


def _path_snapshot(models: dict[str, Any], kind: str) -> dict[str, Any]:
    p1 = ((models.get("P1_volatility_adjusted_path") or {}).get("horizons") or {}).get("20D") or {}
    if kind == "opportunity":
        return {
            "positive_terminal_observation": p1.get("positive_terminal_prob"),
            "touch_up_observation": p1.get("touch_up_5pct_prob"),
            "evidence_strength": "观察项，仅供人工复核",
        }
    return {
        "downside_path_observation": p1.get("touch_down_5pct_prob"),
        "drawdown_observation": p1.get("max_drawdown_p50"),
        "risk_attention_level": classify_risk_attention({"P1_volatility_adjusted_path": {"horizons": {"20D": p1}}}),
    }


def _p2_fallback_high(backtest: dict[str, Any]) -> bool:
    metrics = (backtest.get("model_backtest_metrics") or {}).get("standard_walk_forward") or {}
    p2 = metrics.get("P2_state_conditional_path") or {}
    rates = [float(row.get("fallback_rate") or 0) for row in p2.values()]
    return bool(rates and max(rates) >= 0.30)


def _evidence_conflicts(path_models: dict[str, Any], comparison: dict[str, Any], quality_statuses: dict[str, str], high_fallback: bool) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    p1 = ((path_models.get("P1_volatility_adjusted_path") or {}).get("horizons") or {}).get("20D") or {}
    if float(p1.get("touch_up_5pct_prob") or 0) >= 0.45 and float(p1.get("touch_down_5pct_prob") or 0) >= 0.45:
        reasons.append("上行触达概率与下行触达概率同时偏高，路径机会与风险并存。")
    for horizon, row in comparison.items():
        if "underperform" in str(row.get("P1_vs_P0_conclusion") or ""):
            reasons.append(f"{horizon} P1 相对 P0 表现偏弱。")
    if high_fallback:
        reasons.append("P2 fallback_rate 偏高，P2 只能作为辅助观察。")
    for name, status in quality_statuses.items():
        if status not in {"PASS", "N/A"}:
            reasons.append(f"{name} 状态为 {status}，需要降级复核。")
    return bool(reasons), reasons
