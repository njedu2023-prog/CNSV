from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS, clean_payload
from cnsv.risk import RISK_REPORT_TYPE, RISK_STAGE, RISK_VERSION
from cnsv.risk.risk_checklist import build_risk_review_checklist
from cnsv.risk.risk_evaluator import evaluate_risk_explanation
from cnsv.risk.risk_scenarios import build_risk_scenario_cards
from cnsv.risk.risk_scoring import score_overall_risk
from cnsv.risk.risk_source_breakdown import build_risk_source_breakdown


def build_risk_explanation_payload(evidence_bundle: dict[str, Any]) -> dict[str, Any]:
    reports = evidence_bundle["reports"]
    availability = evidence_bundle["risk_evidence_availability"]
    data = reports.get("data_report") or {}
    feature = reports.get("feature_report") or {}
    baseline = reports.get("baseline_model_report") or {}
    path = reports.get("path_distribution_report") or {}
    backtest = reports.get("observation_backtest_report") or {}
    support = reports.get("human_decision_support_report") or {}
    breakdown = build_risk_source_breakdown(reports, availability)
    summary = score_overall_risk(availability, breakdown, support)
    payload: dict[str, Any] = {
        "meta": {"system": "CNSV", "version": RISK_VERSION, "stage": RISK_STAGE, "report_type": RISK_REPORT_TYPE, "ts_code": "600150.SH", "name": "中国船舶", "generated_at": datetime.now(timezone.utc).isoformat(), "latest_trade_date": _latest_trade_date(data, feature, baseline, path, backtest, support), "is_trade_signal": False},
        "cnsvdata_gate": _stage_gate(data.get("cnsvdata_gate") or support.get("cnsvdata_gate") or {}),
        "risk_evidence_availability": availability,
        "overall_risk_summary": summary,
        "risk_source_breakdown": breakdown,
        "data_risk_explanation": _data_risk(data, feature, availability),
        "feature_risk_explanation": _feature_risk(feature, support),
        "baseline_model_risk_explanation": _baseline_risk(baseline, reports.get("baseline_validation_report") or {}, support),
        "path_distribution_risk_explanation": _path_risk(path, reports.get("path_validation_report") or {}),
        "observation_backtest_risk_explanation": _backtest_risk(backtest),
        "decision_support_risk_explanation": _support_risk(support),
        "p2_auxiliary_risk_explanation": _p2_risk(path, backtest, support),
        "evidence_conflict_risk_explanation": _conflict_risk(support),
        "risk_scenario_cards": [],
        "risk_review_checklist": build_risk_review_checklist(),
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "next_stage": "V2.0 live manual decision system",
        "v2_readiness": "allowed_for_preparation_only_after_human_review",
    }
    payload["risk_scenario_cards"] = build_risk_scenario_cards(payload)
    payload["risk_explanation_quality"] = evaluate_risk_explanation(payload)
    return clean_payload(payload)


def _stage_gate(gate: dict[str, Any]) -> dict[str, Any]:
    out = dict(gate)
    out["can_generate_formal_signal"] = False
    out["can_auto_order"] = False
    out["can_connect_broker_api"] = False
    out["risk_stage_permission"] = "V1.6 only explains risk evidence for human review."
    return out


def _latest_trade_date(*reports: dict[str, Any]) -> str:
    for report in reports:
        date = (report.get("meta") or {}).get("latest_trade_date") or (report.get("data_manifest") or {}).get("latest_trade_date")
        if date:
            return str(date)
    return "N/A"


def _risk_item(level: str, reason: str, evidence: list[str], review: bool = True) -> dict[str, Any]:
    return {"risk_level": level, "risk_reason": reason, "risk_evidence": evidence, "human_review_required": review}


def _data_risk(data: dict[str, Any], feature: dict[str, Any], availability: dict[str, Any]) -> dict[str, Any]:
    missing = availability.get("missing_reports", [])
    gate = data.get("cnsvdata_gate") or feature.get("cnsvdata_gate") or {}
    return {
        "risk_level": "high" if missing else "low",
        "data_freshness_risk": _risk_item("medium", "需要确认最新交易日是否仍然有效。", ["latest_data_report.json"]),
        "data_gate_risk": _risk_item("low" if (gate.get("status") or gate.get("gate_status")) == "PASS" else "high", "CNSVdata gate 必须保持可用。", ["latest_data_report.json"]),
        "missing_data_risk": _risk_item("high" if missing else "low", "缺失报告会导致 V1.6 降级解释。", missing or ["无缺失"]),
        "quality_check_risk": _risk_item("low", "数据质量检查用于确认基础输入完整性。", ["latest_data_report.json"]),
        "manifest_consistency_risk": _risk_item("low", "manifest 与报告快照需人工抽查。", ["latest_data_report.json"]),
    }


def _feature_risk(feature: dict[str, Any], support: dict[str, Any]) -> dict[str, Any]:
    state = support.get("current_state_summary") or {}
    trend = state.get("trend_state")
    vol = state.get("volatility_state")
    flow = state.get("flow_strength_basic")
    unknown = any(str(v).lower() in {"unknown", "n/a", ""} for v in [trend, vol, flow])
    return {
        "risk_level": "medium" if unknown or flow in {"mixed", "weak"} else "low",
        "trend_state_risk": _risk_item("medium" if trend in {"downtrend", "unknown"} else "low", f"趋势状态为 {trend}，需要结合路径风险复核。", ["latest_feature_report.json"]),
        "volatility_state_risk": _risk_item("medium" if vol not in {"normal_vol", "normal"} else "low", f"波动率状态为 {vol}。", ["latest_feature_report.json"]),
        "flow_strength_basic_risk": _risk_item("medium" if flow in {"mixed", "weak"} else "low", f"资金流强弱状态为 {flow}。", ["latest_feature_report.json"]),
        "moneyflow_reliability_risk": _risk_item("medium", "moneyflow 只能作为强因子观察，不是单独结论。", ["latest_feature_report.json"]),
        "feature_unknown_risk": _risk_item("high" if unknown else "low", "unknown 状态会降低风险解释置信度。", ["latest_feature_report.json"]),
        "feature_conflict_risk": _risk_item("medium" if trend == "downtrend" and flow == "mixed" else "low", "趋势与资金流可能出现解释冲突。", ["latest_feature_report.json"]),
    }


def _baseline_risk(baseline: dict[str, Any], validation: dict[str, Any], support: dict[str, Any]) -> dict[str, Any]:
    disagreements = (support.get("model_consistency_summary") or {}).get("model_disagreement_points") or []
    b2 = (((baseline.get("baseline_models") or {}).get("B2_state_grouped_distribution") or {}).get("horizons") or {})
    samples = [int((row or {}).get("state_sample_size") or 0) for row in b2.values() if row]
    min_sample = min(samples) if samples else 0
    return {
        "risk_level": "medium" if disagreements or min_sample < 30 else "low",
        "baseline_distribution_risk": _risk_item("medium", "基准分布仅为历史/状态分布观察。", ["latest_baseline_model_report.json"]),
        "B1_B3_conflict_risk": _risk_item("medium" if disagreements else "low", "B1 与 B3 分布方向差异需要人工复核。", disagreements or ["无显著分歧"]),
        "B2_state_sample_risk": _risk_item("high" if min_sample < 30 else "medium", f"B2 最小状态样本数为 {min_sample}。", ["latest_baseline_model_report.json"]),
        "positive_prob_calibration_risk": _risk_item("medium", "正向概率校准只能用于观察，不代表确定结果。", ["latest_baseline_validation_report.json"]),
        "quantile_coverage_risk": _risk_item("low" if (validation.get("validation_quality") or {}).get("status") == "PASS" else "medium", "分位覆盖需要结合验证层。", ["latest_baseline_validation_report.json"]),
    }


def _path_risk(path: dict[str, Any], validation: dict[str, Any]) -> dict[str, Any]:
    p1 = ((((path.get("path_models") or {}).get("P1_volatility_adjusted_path") or {}).get("horizons") or {}).get("20D") or {})
    touch_down = float(p1.get("touch_down_5pct_prob") or 0)
    drawdown = float(p1.get("max_drawdown_p50") or 0)
    level = "high" if touch_down >= 0.55 or drawdown <= -0.10 else "medium" if touch_down >= 0.35 or drawdown <= -0.05 else "low"
    return {
        "risk_level": level,
        "downside_path_risk": _risk_item(level, "20D 下行路径概率需要人工复核。", ["latest_path_distribution_report.json"]),
        "touch_down_risk": _risk_item(level, f"20D touch_down_5pct_prob={touch_down:.4f}。", ["latest_path_distribution_report.json"]),
        "max_drawdown_risk": _risk_item("medium" if drawdown <= -0.05 else "low", f"20D max_drawdown_p50={drawdown:.4f}。", ["latest_path_distribution_report.json"]),
        "path_volatility_risk": _risk_item("medium", "路径波动率放大时需要额外复核。", ["latest_path_distribution_report.json"]),
        "terminal_distribution_risk": _risk_item("medium", "终端分布为历史路径观察，不代表未来承诺。", ["latest_path_validation_report.json"]),
    }


def _backtest_risk(backtest: dict[str, Any]) -> dict[str, Any]:
    scope = backtest.get("backtest_scope") or {}
    purged = int(scope.get("purged_sample_size") or 0)
    comparison = (backtest.get("model_comparison") or {}).get("standard_walk_forward") or {}
    p1_under = any("underperform" in str(row.get("P1_vs_P0_conclusion") or "") for row in comparison.values())
    return {"risk_level": "high" if purged < 50 else "medium" if p1_under else "low", "observation_backtest_evidence_risk": _risk_item("medium", "观察级回测不是正式回测引擎。", ["latest_observation_backtest_report.json"]), "bucket_stability_risk": _risk_item("medium", "分桶稳定性需要结合 condition quality。", ["latest_observation_backtest_report.json"]), "purged_sample_risk": _risk_item("high" if purged < 50 else "medium", f"purged_sample_size={purged}。", ["latest_observation_backtest_report.json"]), "condition_effectiveness_risk": _risk_item("medium", "条件有效性仅支持观察复核。", ["latest_observation_backtest_report.json"]), "P1_vs_P0_risk": _risk_item("medium" if p1_under else "low", "P1 相对 P0 表现偏弱时需要复核。", ["latest_observation_backtest_report.json"]), "P2_vs_P1_risk": _risk_item("medium", "P2 为辅助层，不作为核心比较结论。", ["latest_observation_backtest_report.json"])}


def _support_risk(support: dict[str, Any]) -> dict[str, Any]:
    levels = support.get("support_levels") or {}
    conflict = (support.get("evidence_conflict_summary") or {}).get("evidence_conflict")
    return {"risk_level": "high" if conflict else "medium" if levels.get("human_review_required") else "low", "evidence_strength_risk": _risk_item("medium" if levels.get("evidence_strength") != "strong" else "low", f"evidence_strength={levels.get('evidence_strength')}", ["latest_human_decision_support_report.json"]), "model_consistency_risk": _risk_item("medium" if levels.get("model_consistency_level") != "consistent" else "low", f"model_consistency_level={levels.get('model_consistency_level')}", ["latest_human_decision_support_report.json"]), "evidence_conflict_risk": _risk_item("high" if conflict else "low", "V1.5 证据冲突必须进入风险解释。", ["latest_human_decision_support_report.json"]), "human_review_required_risk": _risk_item("medium" if levels.get("human_review_required") else "low", "人工复核为风险控制要求。", ["latest_human_decision_support_report.json"]), "attention_item_risk": _risk_item("medium" if support.get("human_attention_items") else "low", "人工关注点需要逐条复核。", ["latest_human_decision_support_report.json"])}


def _p2_risk(path: dict[str, Any], backtest: dict[str, Any], support: dict[str, Any]) -> dict[str, Any]:
    p2 = ((((path.get("path_models") or {}).get("P2_state_conditional_path") or {}).get("horizons") or {}))
    samples = [int((row or {}).get("state_sample_size") or 0) for row in p2.values()]
    min_sample = min(samples) if samples else 0
    metrics = (((backtest.get("model_backtest_metrics") or {}).get("standard_walk_forward") or {}).get("P2_state_conditional_path") or {})
    rates = [float(row.get("fallback_rate") or 0) for row in metrics.values()]
    max_fallback = max(rates) if rates else 0
    level = "high" if max_fallback >= 0.30 or min_sample < 30 else "medium"
    return {"p2_auxiliary_risk_level": level, "p2_fallback_risk": _risk_item(level, f"P2 max_fallback_rate={max_fallback:.4f}。", ["latest_observation_backtest_report.json"]), "p2_state_sample_risk": _risk_item("high" if min_sample < 30 else "medium", f"P2 min_state_sample_size={min_sample}。", ["latest_path_distribution_report.json"]), "p2_state_space_fragmentation_risk": _risk_item("medium", "状态空间分组容易碎片化，需要避免核心依赖。", ["latest_path_distribution_report.json"]), "p2_core_dependency_forbidden": True, "p2_role": "辅助状态层，不作为核心决策依赖"}


def _conflict_risk(support: dict[str, Any]) -> dict[str, Any]:
    conflict = support.get("evidence_conflict_summary") or {}
    reasons = conflict.get("evidence_conflict_reasons") or []
    return {"risk_level": "high" if conflict.get("evidence_conflict") else "low", "evidence_conflict": bool(conflict.get("evidence_conflict")), "risk_reason": "证据冲突需要人工复核，不得转化为交易动作。", "risk_evidence": reasons, "source_reports": ["latest_human_decision_support_report.json"], "human_review_required": bool(conflict.get("evidence_conflict"))}
