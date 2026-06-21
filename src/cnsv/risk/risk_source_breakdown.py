from __future__ import annotations

from typing import Any

from cnsv.risk.risk_evidence_loader import quality_status


def build_risk_source_breakdown(reports: dict[str, Any], availability: dict[str, Any]) -> dict[str, dict[str, Any]]:
    data = reports.get("data_report") or {}
    feature = reports.get("feature_report") or {}
    baseline = reports.get("baseline_model_report") or {}
    path_validation = reports.get("path_validation_report") or {}
    backtest = reports.get("observation_backtest_report") or {}
    support = reports.get("human_decision_support_report") or {}

    state = support.get("current_state_summary") or baseline.get("current_state") or {}
    conflicts = support.get("evidence_conflict_summary") or {}
    p2 = _p2_metrics(reports.get("path_distribution_report") or {}, backtest)
    purged = int((backtest.get("backtest_scope") or {}).get("purged_sample_size") or 0)
    path20 = _path_20d(reports.get("path_distribution_report") or {})
    missing = availability.get("missing_reports", [])

    return {
        "data_risk": _entry("data_risk", "high" if missing else _status_level(quality_status(data, "validation")), "数据门禁、数据新鲜度与 manifest 一致性需要人工确认。", ["latest_data_report.json"], bool(missing)),
        "feature_risk": _entry("feature_risk", "medium" if _has_unknown(state) else _status_level(quality_status(feature, "feature_quality")), "趋势、波动率、资金流状态共同决定特征风险；unknown 状态需要降级复核。", ["latest_feature_report.json", "latest_human_decision_support_report.json"], _has_unknown(state)),
        "baseline_model_risk": _entry("baseline_model_risk", "medium" if _model_conflict(support) else _status_level(quality_status(baseline, "baseline_quality")), "基准模型分布与验证结果用于识别 B 模型之间的方向分歧。", ["latest_baseline_model_report.json", "latest_baseline_validation_report.json"], _model_conflict(support)),
        "path_distribution_risk": _entry("path_distribution_risk", _path_level(path20), "路径下穿概率、最大回撤与路径波动率共同构成路径分布风险。", ["latest_path_distribution_report.json", "latest_path_validation_report.json"], True),
        "path_validation_risk": _entry("path_validation_risk", _status_level(quality_status(path_validation, "path_validation_quality")), "路径验证质量用于判断路径分布证据是否需要降级。", ["latest_path_validation_report.json"], quality_status(path_validation, "path_validation_quality") != "PASS"),
        "observation_backtest_risk": _entry("observation_backtest_risk", "high" if purged < 50 else "medium" if purged < 120 else _status_level(quality_status(backtest, "observation_backtest_quality")), "观察级回测只提供历史观察证据，purged 样本偏少时需要提高复核强度。", ["latest_observation_backtest_report.json"], purged < 120),
        "decision_support_risk": _entry("decision_support_risk", "medium" if quality_status(support, "human_decision_support_quality") == "WARN" else _status_level(quality_status(support, "human_decision_support_quality")), "V1.5 WARN 代表人工复核要求，不是阻断错误，但需要在 V1.6 明确解释。", ["latest_human_decision_support_report.json"], quality_status(support, "human_decision_support_quality") != "PASS"),
        "p2_auxiliary_risk": _entry("p2_auxiliary_risk", "high" if p2["fallback_rate_high"] else "medium", "P2 是辅助状态层，状态样本空间可能碎片化，不能作为核心依赖。", ["latest_path_distribution_report.json", "latest_observation_backtest_report.json"], True),
        "evidence_conflict_risk": _entry("evidence_conflict_risk", "high" if conflicts.get("evidence_conflict") else "low", "多模型证据存在方向差异时必须人工复核，不得转化为交易动作。", ["latest_human_decision_support_report.json"], bool(conflicts.get("evidence_conflict"))),
        "system_boundary_risk": _entry("system_boundary_risk", "low", "当前阶段仅允许风险解释，禁止正式交易信号、自动交易和外部执行接口。", ["latest_human_decision_support_report.json"], True),
    }


def _entry(risk_type: str, level: str, reason: str, evidence: list[str], review: bool) -> dict[str, Any]:
    return {"risk_type": risk_type, "risk_level": level, "risk_reason": reason, "risk_evidence": evidence, "source_reports": evidence, "human_review_required": review}


def _status_level(status: str) -> str:
    if status == "FAIL":
        return "severe"
    if status in {"WARN", "MISSING"}:
        return "high"
    if status == "PASS":
        return "low"
    return "medium"


def _has_unknown(state: dict[str, Any]) -> bool:
    return any(str(value).lower() in {"unknown", "none", "n/a", ""} for value in state.values())


def _model_conflict(support: dict[str, Any]) -> bool:
    return bool((support.get("model_consistency_summary") or {}).get("model_disagreement_points"))


def _path_20d(path: dict[str, Any]) -> dict[str, Any]:
    p1 = (((path.get("path_models") or {}).get("P1_volatility_adjusted_path") or {}).get("horizons") or {}).get("20D") or {}
    return {
        "touch_down_5pct_prob": float(p1.get("touch_down_5pct_prob") or 0),
        "max_drawdown_p50": float(p1.get("max_drawdown_p50") or 0),
        "path_volatility_p90": float(p1.get("path_volatility_p90") or 0),
    }


def _path_level(path20: dict[str, Any]) -> str:
    if path20["touch_down_5pct_prob"] >= 0.55 or path20["max_drawdown_p50"] <= -0.10:
        return "high"
    if path20["touch_down_5pct_prob"] >= 0.35 or path20["max_drawdown_p50"] <= -0.05:
        return "medium"
    return "low"


def _p2_metrics(path: dict[str, Any], backtest: dict[str, Any]) -> dict[str, Any]:
    metrics = ((backtest.get("model_backtest_metrics") or {}).get("standard_walk_forward") or {}).get("P2_state_conditional_path") or {}
    rates = [float(row.get("fallback_rate") or 0) for row in metrics.values()]
    p2 = (((path.get("path_models") or {}).get("P2_state_conditional_path") or {}).get("horizons") or {})
    samples = [int((row or {}).get("state_sample_size") or 0) for row in p2.values()]
    return {"fallback_rate_high": bool(rates and max(rates) >= 0.30), "min_state_sample_size": min(samples) if samples else 0}
