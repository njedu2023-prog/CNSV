from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS, clean_payload
from cnsv.report.feature_report_html import write_feature_report_html
from cnsv.utils.io import ensure_parent, repo_root

VERSION = "1.5"
STAGE = "V1.5_human_decision_support"
REQUIRED = {
    "data_report": "latest_data_report.json",
    "feature_report": "latest_feature_report.json",
    "baseline_model_report": "latest_baseline_model_report.json",
    "baseline_validation_report": "latest_baseline_validation_report.json",
    "path_distribution_report": "latest_path_distribution_report.json",
    "path_validation_report": "latest_path_validation_report.json",
    "observation_backtest_report": "latest_observation_backtest_report.json",
}
FORBIDDEN_FIELDS = {
    "buy_signal",
    "sell_signal",
    "target_position",
    "target_shares",
    "stop_loss",
    "take_profit",
    "target_price",
    "formal_signal",
    "trade_recommendation",
    "entry_level",
    "exit_level",
    "position_level",
}


def main() -> int:
    root = repo_root()
    reports, availability = _load_reports(root)
    payload = build_payload(reports, availability)
    _write_json(payload, root / "docs/data/latest_human_decision_support_report.json")
    _write_json(_registry(), root / "docs/data/human_decision_support_registry.json")
    _write_md(payload, root / "reports/latest_human_decision_support_report.md", root / "reports/archive")
    _write_html(root / "docs/decision_support.html")
    write_feature_report_html(root / "docs/index.html")
    _ensure_index_entry(root / "docs/index.html")
    quality = payload["human_decision_support_quality"]
    print(f"human_decision_support_quality={quality['status']} failed={quality['failed_count']} warn={quality['warn_count']}")
    return 0 if quality["status"] in {"PASS", "WARN"} else 1


def build_payload(reports: dict[str, Any], availability: dict[str, Any]) -> dict[str, Any]:
    data = reports.get("data_report") or {}
    feature = reports.get("feature_report") or {}
    baseline = reports.get("baseline_model_report") or {}
    baseline_validation = reports.get("baseline_validation_report") or {}
    path = reports.get("path_distribution_report") or {}
    path_validation = reports.get("path_validation_report") or {}
    backtest = reports.get("observation_backtest_report") or {}
    features = feature.get("features") or {}
    path_models = path.get("path_models") or {}
    baseline_models = baseline.get("baseline_models") or {}
    quality_statuses = {
        "data_quality": _status(data, "validation"),
        "feature_quality": _status(feature, "feature_quality"),
        "baseline_quality": _status(baseline, "baseline_quality"),
        "validation_quality": _status(baseline_validation, "validation_quality"),
        "path_quality": _status(path, "path_quality"),
        "path_validation_quality": _status(path_validation, "path_validation_quality"),
        "observation_backtest_quality": _status(backtest, "observation_backtest_quality"),
        "leakage_checks": str((backtest.get("observation_backtest_leakage_checks") or {}).get("status") or "MISSING"),
    }
    standard_sample = int((backtest.get("backtest_scope") or {}).get("standard_sample_size") or 0)
    purged_sample = int((backtest.get("backtest_scope") or {}).get("purged_sample_size") or 0)
    high_fallback = _p2_fallback_high(backtest)
    evidence_strength = _evidence_strength(quality_statuses, standard_sample, purged_sample, high_fallback)
    risk_attention = _risk_attention(path_models)
    consistency = _consistency(baseline_models, path_models, (backtest.get("model_comparison") or {}).get("standard_walk_forward") or {})
    conflict, reasons = _conflicts(path_models, (backtest.get("model_comparison") or {}).get("standard_walk_forward") or {}, quality_statuses, high_fallback)
    support_levels = {
        "observation_priority": "high" if conflict or risk_attention == "high" else "medium" if evidence_strength != "insufficient" else "low",
        "risk_attention_level": risk_attention,
        "evidence_strength": evidence_strength,
        "model_consistency_level": consistency["model_consistency_level"],
        "human_review_required": True,
    }
    payload: dict[str, Any] = {
        "meta": {
            "system": "CNSV",
            "version": VERSION,
            "stage": STAGE,
            "report_type": "human_decision_support_report",
            "ts_code": "600150.SH",
            "name": "中国船舶",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "latest_trade_date": _latest_trade_date(data, feature, baseline, path, backtest),
            "is_trade_signal": False,
        },
        "cnsvdata_gate": _stage_gate(data.get("cnsvdata_gate") or feature.get("cnsvdata_gate") or path.get("cnsvdata_gate") or {}),
        "evidence_availability": availability,
        "human_decision_support_quality": {},
        "current_state_summary": _current_state(data, feature, baseline),
        "model_evidence_summary": _model_evidence(baseline, path, backtest),
        "path_opportunity_observation": _opportunity(path_models, backtest),
        "path_risk_observation": _risk(path_models, backtest, risk_attention),
        "model_consistency_summary": consistency,
        "evidence_conflict_summary": {"evidence_conflict": conflict, "evidence_conflict_reasons": reasons},
        "human_attention_items": _attention_items(availability, support_levels, consistency, reasons),
        "human_review_checklist": _checklist(),
        "support_levels": support_levels,
        "upstream_quality_statuses": quality_statuses,
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "next_stage": "V1.6 risk explanation",
    }
    payload["human_decision_support_quality"] = _evaluate(payload)
    return clean_payload(payload)


def _load_reports(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    data_dir = root / "docs" / "data"
    reports: dict[str, Any] = {}
    availability = {"all_required_available": True, "available_reports": [], "missing_reports": [], "reports": {}}
    for key, filename in REQUIRED.items():
        path = data_dir / filename
        if not path.exists():
            reports[key] = None
            availability["all_required_available"] = False
            availability["missing_reports"].append(key)
            availability["reports"][key] = {"available": False, "path": str(path), "reason": "missing_report"}
            continue
        reports[key] = json.loads(path.read_text(encoding="utf-8"))
        availability["available_reports"].append(key)
        availability["reports"][key] = {"available": True, "path": str(path)}
    return reports, availability


def _status(report: dict[str, Any], key: str) -> str:
    if not report:
        return "MISSING"
    return str((report.get(key) or {}).get("status") or "N/A")


def _latest_trade_date(*reports: dict[str, Any]) -> str:
    for report in reports:
        value = (report.get("meta") or {}).get("latest_trade_date") or (report.get("data_manifest") or {}).get("latest_trade_date")
        if value:
            return str(value)
    return "N/A"


def _stage_gate(gate: dict[str, Any]) -> dict[str, Any]:
    out = dict(gate)
    out["can_generate_formal_signal"] = False
    out["can_auto_order"] = False
    out["can_connect_broker_api"] = False
    out["support_stage_permission"] = "V1.5 only supports human-readable evidence review."
    return out


def _current_state(data: dict[str, Any], feature: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    features = feature.get("features") or {}
    price = features.get("price_volume") or {}
    moneyflow = features.get("moneyflow") or {}
    trend = features.get("trend") or {}
    volatility = features.get("volatility") or {}
    gate = data.get("cnsvdata_gate") or feature.get("cnsvdata_gate") or {}
    return {
        "latest_trade_date": price.get("latest_trade_date") or (feature.get("meta") or {}).get("latest_trade_date"),
        "latest_close": price.get("latest_close") or (baseline.get("current_state") or {}).get("latest_close"),
        "trend_state": trend.get("trend_state") or (baseline.get("current_state") or {}).get("trend_state"),
        "volatility_state": volatility.get("volatility_state") or (baseline.get("current_state") or {}).get("volatility_state"),
        "flow_strength_basic": moneyflow.get("flow_strength_basic") or (baseline.get("current_state") or {}).get("flow_strength_basic"),
        "data_quality_status": _status(data, "validation"),
        "feature_quality_status": _status(feature, "feature_quality"),
        "cnsvdata_gate_status": gate.get("gate_status") or gate.get("status"),
    }


def _model_evidence(baseline: dict[str, Any], path: dict[str, Any], backtest: dict[str, Any]) -> dict[str, Any]:
    return {
        "terminal_distribution_summary": _terminal_summary(baseline.get("baseline_models") or {}),
        "path_distribution_summary": _path_summary(path.get("path_models") or {}),
        "observation_backtest_summary": {
            "quality_status": _status(backtest, "observation_backtest_quality"),
            "standard_sample_size": (backtest.get("backtest_scope") or {}).get("standard_sample_size"),
            "purged_sample_size": (backtest.get("backtest_scope") or {}).get("purged_sample_size"),
            "leakage_status": (backtest.get("observation_backtest_leakage_checks") or {}).get("status"),
        },
        "model_support_summary": {
            "baseline_models": list((baseline.get("baseline_models") or {}).keys()),
            "path_models": list((path.get("path_models") or {}).keys()),
            "p2_role": "辅助状态层，不作为核心决策依赖",
        },
    }


def _terminal_summary(models: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for model_id, model in models.items():
        row = ((model.get("horizons") or {}).get("20D") or {})
        out[model_id] = {"20D_median_return": row.get("median_return") or row.get("terminal_return_p50"), "20D_positive_probability": row.get("positive_probability") or row.get("positive_terminal_prob"), "sample_size": row.get("sample_size"), "fallback_used": row.get("fallback_used")}
    return out


def _path_summary(models: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for model_id, model in models.items():
        row = ((model.get("horizons") or {}).get("20D") or {})
        out[model_id] = {"20D_positive_terminal_prob": row.get("positive_terminal_prob"), "20D_touch_up_5pct_prob": row.get("touch_up_5pct_prob"), "20D_touch_down_5pct_prob": row.get("touch_down_5pct_prob"), "20D_max_drawdown_p50": row.get("max_drawdown_p50"), "fallback_used": row.get("fallback_used"), "state_sample_size": row.get("state_sample_size")}
    return out


def _opportunity(models: dict[str, Any], backtest: dict[str, Any]) -> dict[str, Any]:
    p1 = ((models.get("P1_volatility_adjusted_path") or {}).get("horizons") or {}).get("20D") or {}
    return {"upside_path_observation": _level(float(p1.get("touch_up_5pct_prob") or 0), 0.55, 0.30), "touch_up_observation": p1.get("touch_up_5pct_prob"), "positive_terminal_observation": p1.get("positive_terminal_prob"), "historical_support_level": _condition_level(((backtest.get("observation_condition_quality") or {}).get("upside_path_groups") or {})), "evidence_strength": "观察项，仅供人工复核"}


def _risk(models: dict[str, Any], backtest: dict[str, Any], risk_attention: str) -> dict[str, Any]:
    p1 = ((models.get("P1_volatility_adjusted_path") or {}).get("horizons") or {}).get("20D") or {}
    return {"downside_path_observation": p1.get("touch_down_5pct_prob"), "drawdown_observation": p1.get("max_drawdown_p50"), "touch_down_observation": p1.get("touch_down_5pct_prob"), "risk_evidence_level": _condition_level(((backtest.get("observation_condition_quality") or {}).get("drawdown_risk_groups") or {})), "risk_attention_level": risk_attention}


def _consistency(baseline_models: dict[str, Any], path_models: dict[str, Any], comparison: dict[str, Any]) -> dict[str, Any]:
    disagreements: list[str] = []
    b1 = (((baseline_models.get("B1_historical_distribution") or {}).get("horizons") or {}).get("20D") or {})
    b3 = (((baseline_models.get("B3_volatility_adjusted") or {}).get("horizons") or {}).get("20D") or {})
    p0 = (((path_models.get("P0_historical_path_replay") or {}).get("horizons") or {}).get("20D") or {})
    p1 = (((path_models.get("P1_volatility_adjusted_path") or {}).get("horizons") or {}).get("20D") or {})
    if b1 and b3 and _direction(b1.get("median_return")) != _direction(b3.get("median_return")):
        disagreements.append("B1 与 B3 的 20D 中位收益方向不一致，需要人工复核。")
    if p0 and p1 and _direction(p0.get("terminal_return_p50")) != _direction(p1.get("terminal_return_p50")):
        disagreements.append("P0 与 P1 的 20D 路径中位收益方向不一致，需要人工复核。")
    for horizon, row in comparison.items():
        if "underperform" in str(row.get("P2_vs_P1_conclusion") or "") or "fallback" in str(row.get("P2_auxiliary_note") or "").lower():
            disagreements.append(f"{horizon} P2 与 P1 存在辅助层不确定性，P2 只能作为辅助观察。")
    level = "mixed" if len(disagreements) >= 3 else "mostly_consistent" if disagreements else "consistent"
    return {"model_consistency_status": level, "model_consistency_level": level, "model_disagreement_points": disagreements, "evidence_conflict_summary": [], "p2_role": "辅助状态层，不作为核心决策依赖"}


def _conflicts(path_models: dict[str, Any], comparison: dict[str, Any], quality_statuses: dict[str, str], high_fallback: bool) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    p1 = (((path_models.get("P1_volatility_adjusted_path") or {}).get("horizons") or {}).get("20D") or {})
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


def _attention_items(availability: dict[str, Any], levels: dict[str, Any], consistency: dict[str, Any], conflict_reasons: list[str]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for missing in availability.get("missing_reports", []):
        items.append({"category": "data_items", "text": f"需要人工确认上游证据缺失：{missing}。"})
    if levels.get("risk_attention_level") == "high":
        items.append({"category": "risk_items", "text": "路径下行或回撤观察偏高，需要人工优先关注风险证据。"})
    for reason in conflict_reasons:
        items.append({"category": "model_items", "text": f"需要人工复核证据冲突：{reason}"})
    for point in consistency.get("model_disagreement_points", []):
        items.append({"category": "model_items", "text": point})
    if not items:
        items.append({"category": "evidence_items", "text": "上游证据可用，但仍需人工结合市场与行业背景复核。"})
    return items


def _checklist() -> list[dict[str, str]]:
    return [
        {"id": "data_freshness", "text": "确认 latest_trade_date 与当前人工复核日期是否匹配。"},
        {"id": "market_context", "text": "确认当天市场环境是否存在外部冲击。"},
        {"id": "industry_context", "text": "确认船舶与军工产业链是否存在重大事件。"},
        {"id": "intraday_behavior", "text": "复核分时结构与尾盘强弱是否支持当前观察。"},
        {"id": "path_risk", "text": "复核下穿概率、最大回撤与风险分组。"},
        {"id": "model_conflict", "text": "复核 B/P 模型之间的方向差异和 P2 辅助层不确定性。"},
        {"id": "evidence_quality", "text": "复核上游质量门禁、purged 样本与 fallback 情况。"},
    ]


def _evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    failed = 0
    warn = 0

    def add(name: str, passed: bool, detail: str, warning: bool = False) -> None:
        nonlocal failed, warn
        if passed:
            status = "PASS"
        elif warning:
            status = "WARN"
            warn += 1
        else:
            status = "FAIL"
            failed += 1
        checks.append({"name": name, "status": status, "detail": detail})

    meta = payload.get("meta") or {}
    levels = payload.get("support_levels") or {}
    availability = payload.get("evidence_availability") or {}
    add("version_is_1_5", meta.get("version") == VERSION, f"version={meta.get('version')}")
    add("is_trade_signal_false", meta.get("is_trade_signal") is False, "V1.5 remains observation support only")
    add("forbidden_actions_present", set(FORBIDDEN_ACTIONS).issubset(set(payload.get("forbidden_actions", []))), "required forbidden actions present")
    add("no_forbidden_trade_fields", not _contains_forbidden_key(payload), "no forbidden trade action field names")
    add("observation_backtest_available", "observation_backtest_report" not in availability.get("missing_reports", []), "V1.4 evidence required")
    add("required_sections_present", all(payload.get(k) for k in ["current_state_summary", "model_evidence_summary", "path_opportunity_observation", "path_risk_observation", "model_consistency_summary", "evidence_conflict_summary", "human_attention_items", "human_review_checklist", "support_levels"]), "all V1.5 sections exist")
    add("p2_is_auxiliary", "辅助" in str((payload.get("model_consistency_summary") or {}).get("p2_role")), "P2 remains auxiliary")
    add("missing_reports_degraded", not availability.get("missing_reports"), f"missing_reports={availability.get('missing_reports')}", warning=True)
    add("evidence_strength_not_insufficient", levels.get("evidence_strength") != "insufficient", f"evidence_strength={levels.get('evidence_strength')}", warning=True)
    add("human_review_flag", levels.get("human_review_required") is False, f"human_review_required={levels.get('human_review_required')}", warning=True)
    add("evidence_conflict", not (payload.get("evidence_conflict_summary") or {}).get("evidence_conflict"), "evidence conflict requires human review", warning=True)
    status = "FAIL" if failed else "WARN" if warn else "PASS"
    return {"status": status, "failed_count": failed, "warn_count": warn, "blocking_error_count": failed, "checks": checks}


def _evidence_strength(statuses: dict[str, str], standard_sample: int, purged_sample: int, high_fallback: bool) -> str:
    if any(status in {"MISSING", "FAIL"} for status in statuses.values()):
        return "insufficient"
    if standard_sample < 100 or purged_sample < 30:
        return "weak"
    if high_fallback:
        return "moderate"
    return "strong" if all(status == "PASS" for status in statuses.values()) else "moderate"


def _risk_attention(models: dict[str, Any]) -> str:
    p1_20d = (((models.get("P1_volatility_adjusted_path") or {}).get("horizons") or {}).get("20D") or {})
    touch_down = float(p1_20d.get("touch_down_5pct_prob") or 0)
    drawdown = abs(float(p1_20d.get("max_drawdown_p50") or 0))
    if touch_down >= 0.45 or drawdown >= 0.08:
        return "high"
    if touch_down >= 0.25 or drawdown >= 0.04:
        return "medium"
    return "low"


def _p2_fallback_high(backtest: dict[str, Any]) -> bool:
    metrics = (backtest.get("model_backtest_metrics") or {}).get("standard_walk_forward") or {}
    p2 = metrics.get("P2_state_conditional_path") or {}
    rates = [float(row.get("fallback_rate") or 0) for row in p2.values()]
    return bool(rates and max(rates) >= 0.30)


def _condition_level(condition: dict[str, Any]) -> str:
    conclusions = [str(row.get("conclusion") or "") for row in condition.values()]
    if any("useful" in item for item in conclusions):
        return "moderate"
    if any("unstable" in item for item in conclusions):
        return "weak"
    return "insufficient" if not conclusions else "weak"


def _level(value: float, high: float, medium: float) -> str:
    return "high" if value >= high else "medium" if value >= medium else "low"


def _direction(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "unknown"
    return "positive" if number > 0 else "negative" if number < 0 else "flat"


def _contains_forbidden_key(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(k) in FORBIDDEN_FIELDS or _contains_forbidden_key(v) for k, v in value.items())
    if isinstance(value, list):
        return any(_contains_forbidden_key(v) for v in value)
    return False


def _registry() -> list[dict[str, Any]]:
    return [{"registry_type": "human_decision_support", "version": VERSION, "stage": STAGE, "inputs": list(REQUIRED.values()), "outputs": ["latest_human_decision_support_report.json", "latest_human_decision_support_report.md", "decision_support.html"], "is_trade_signal": False, "forbidden": FORBIDDEN_ACTIONS, "next_stage": "V1.6 risk explanation"}]


def _write_json(payload: Any, path: Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return target


def _write_md(payload: dict[str, Any], path: Path, archive_dir: Path) -> None:
    text = _markdown(payload)
    ensure_parent(path).write_text(text, encoding="utf-8")
    ensure_parent(archive_dir / f"{date.today().isoformat()}_human_decision_support_report.md").write_text(text, encoding="utf-8")


def _markdown(payload: dict[str, Any]) -> str:
    meta = payload["meta"]
    q = payload["human_decision_support_quality"]
    levels = payload["support_levels"]
    av = payload["evidence_availability"]
    state = payload["current_state_summary"]
    conflict = payload["evidence_conflict_summary"]
    lines = [
        "# CNSV V1.5 人工决策辅助报告",
        "",
        "本报告是人工决策辅助，不是交易信号；不构成方向性操作建议，不输出交易执行参数或自动交易动作。",
        "",
        "## 阶段说明",
        f"- 版本: {meta.get('version')}",
        f"- 阶段: {meta.get('stage')}",
        f"- latest_trade_date: {meta.get('latest_trade_date')}",
        f"- 质量状态: {q.get('status')}",
        f"- FAIL 数量: {q.get('failed_count')}",
        f"- WARN 数量: {q.get('warn_count')}",
        "",
        "## 上游证据可用性",
        f"- 全部必需证据可用: {av.get('all_required_available')}",
        f"- 可用证据: {', '.join(av.get('available_reports', []))}",
        f"- 缺失证据: {', '.join(av.get('missing_reports', [])) or '无'}",
        "",
        "## 当前状态摘要",
        *[f"- {k}: {v}" for k, v in state.items()],
        "",
        "## 模型证据摘要",
        f"- 证据强度: {levels.get('evidence_strength')}",
        f"- 模型一致性: {levels.get('model_consistency_level')}",
        f"- P2 定位: {payload['model_consistency_summary'].get('p2_role')}",
        "",
        "## 路径机会观察",
        *[f"- {k}: {v}" for k, v in payload["path_opportunity_observation"].items()],
        "",
        "## 路径风险观察",
        *[f"- {k}: {v}" for k, v in payload["path_risk_observation"].items()],
        "",
        "## V1.4 观察级回测支持情况",
        *[f"- {k}: {v}" for k, v in payload["model_evidence_summary"]["observation_backtest_summary"].items()],
        "",
        "## 模型一致性与分歧",
        *[f"- {item}" for item in (payload["model_consistency_summary"].get("model_disagreement_points") or ["无阻断性分歧"])],
        "",
        "## 证据冲突",
        f"- 是否存在证据冲突: {conflict.get('evidence_conflict')}",
        *[f"- {item}" for item in (conflict.get("evidence_conflict_reasons") or ["无"])],
        "",
        "## 支持等级",
        *[f"- {k}: {v}" for k, v in levels.items()],
        "",
        "## 人工关注点",
        *[f"- [{item.get('category')}] {item.get('text')}" for item in payload["human_attention_items"]],
        "",
        "## 人工复核清单",
        *[f"- [{item.get('id')}] {item.get('text')}" for item in payload["human_review_checklist"]],
        "",
        "## 禁止交易信号声明",
        "- 正式交易信号: NO",
        "- 方向性操作建议: NO",
        "- 交易执行参数: NO",
        "- 自动交易动作: NO",
        f"- forbidden_actions: {', '.join(payload.get('forbidden_actions', []))}",
        "",
        "## 下一阶段",
        f"- {payload.get('next_stage')}",
    ]
    return "\n".join(lines) + "\n"


def _write_html(path: Path) -> None:
    ensure_parent(path).write_text(HTML, encoding="utf-8")


def _ensure_index_entry(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace("CNSV V1.4 主线看板", "CNSV V1.5 主线看板")
    text = text.replace("路径分布与 V1.4 观察级回测入口", "路径分布、观察级回测与 V1.5 人工决策辅助入口")
    if 'href="decision_support.html"' not in text:
        text = text.replace("</nav>", '<a href="decision_support.html">V1.5 人工决策辅助</a></nav>')
    path.write_text(text, encoding="utf-8")


HTML = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CNSV V1.5 人工决策辅助</title><style>:root{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Microsoft YaHei",sans-serif;--page:#f5f5f7;--surface:#fff;--line:#d2d2d7;--text:#1d1d1f;--muted:#6e6e73;--blue:#06c;--green:#0b8f45;--red:#d70015;--amber:#8a5a00;--shadow:0 18px 44px rgba(0,0,0,.06)}*{box-sizing:border-box}body{margin:0;background:var(--page);color:var(--text)}main{width:min(100%,1180px);margin:auto;padding:38px 24px 48px}header{text-align:center;padding:18px 0 28px}.eyebrow{color:var(--blue);font-size:13px;font-weight:700;letter-spacing:.08em;margin:0 0 8px}h1{font-size:18px;margin:0}.subtitle{color:var(--muted);font-size:13px;margin:12px auto 0;max-width:860px;line-height:1.45}nav{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:16px}nav a{border:1px solid var(--line);border-radius:999px;color:var(--blue);text-decoration:none;padding:6px 11px;font-size:12px;background:#fff}section{background:var(--surface);border-radius:20px;padding:22px 26px;margin:16px 0;box-shadow:var(--shadow);overflow:hidden}h2{font-size:14px;margin:0 0 14px}.chips{display:flex;flex-wrap:wrap;gap:8px}.chip{border:1px solid var(--line);border-radius:999px;background:#fff;padding:7px 11px;color:var(--muted);font-size:12px}.chip strong{color:var(--text);margin-left:6px}.ok{color:var(--green)!important;font-weight:700}.bad{color:var(--red)!important;font-weight:700}.warn{color:var(--amber)!important;font-weight:700}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.card{border:1px solid var(--line);border-radius:16px;padding:14px;background:#fbfbfd}.card .label{color:var(--muted);font-size:12px}.card .value{font-weight:700;font-size:13px;margin-top:8px}.list{display:grid;gap:8px}.item{border:1px solid var(--line);border-radius:14px;padding:11px 13px;background:#fbfbfd;font-size:12px;line-height:1.45}.footer{color:var(--muted);font-size:12px;text-align:center;padding:18px 0 4px}@media(max-width:720px){main{padding:22px 14px 36px}header{text-align:left}nav{justify-content:flex-start}section{border-radius:18px;padding:18px}.grid{grid-template-columns:1fr}}</style></head><body><main><header><p class="eyebrow">CNSV V1.5 HUMAN DECISION SUPPORT</p><h1>中国船舶人工决策辅助看板</h1><p class="subtitle">整合 V1.0-V1.4 数据、特征、基准分布、路径分布与观察级回测证据，供人工复核。页面不生成交易信号，不构成方向性操作建议。</p><nav><a href="index.html">主线看板</a><a href="backtest.html">V1.4 观察级回测</a><a href="data/latest_human_decision_support_report.json">JSON</a></nav></header><section><h2>阶段总览</h2><div id="overview" class="chips"></div></section><section><h2>上游证据可用性</h2><div id="availability" class="chips"></div></section><section><h2>当前状态摘要</h2><div id="state" class="grid"></div></section><section><h2>模型证据摘要</h2><div id="modelEvidence" class="list"></div></section><section><h2>路径机会观察</h2><div id="opportunity" class="grid"></div></section><section><h2>路径风险观察</h2><div id="risk" class="grid"></div></section><section><h2>模型一致性与证据冲突</h2><div id="consistency" class="list"></div></section><section><h2>人工关注点</h2><div id="attention" class="list"></div></section><section><h2>人工复核清单</h2><div id="checklist" class="list"></div></section><section><h2>禁止交易信号声明</h2><div id="guardrails" class="chips"></div></section><div id="footer" class="footer"></div></main><script>const fmt=v=>v===null||v===undefined?"N/A":typeof v==="number"?v.toFixed(4):v;const cls=v=>v==="PASS"?"ok":v==="FAIL"?"bad":v==="WARN"?"warn":"";const chip=(l,v,c=cls(v))=>`<span class="chip">${l}<strong class="${c}">${fmt(v)}</strong></span>`;const card=(l,v)=>`<div class="card"><div class="label">${l}</div><div class="value">${fmt(v)}</div></div>`;const item=v=>`<div class="item">${v}</div>`;fetch("data/latest_human_decision_support_report.json").then(r=>r.json()).then(d=>{const q=d.human_decision_support_quality||{},meta=d.meta||{},levels=d.support_levels||{},av=d.evidence_availability||{},st=d.current_state_summary||{};overview.innerHTML=[chip("版本",meta.version),chip("阶段",meta.stage),chip("质量",q.status),chip("证据强度",levels.evidence_strength),chip("风险关注",levels.risk_attention_level),chip("人工复核",levels.human_review_required),chip("交易信号",meta.is_trade_signal?"YES":"NO",meta.is_trade_signal?"bad":"ok")].join("");availability.innerHTML=[chip("全部可用",av.all_required_available),chip("可用数量",(av.available_reports||[]).length),chip("缺失数量",(av.missing_reports||[]).length)].concat((av.missing_reports||[]).map(x=>chip("缺失",x,"warn"))).join("");state.innerHTML=Object.entries(st).map(([k,v])=>card(k,v)).join("");const me=d.model_evidence_summary||{},obs=me.observation_backtest_summary||{},ms=me.model_support_summary||{};modelEvidence.innerHTML=[item(`V1.4质量：${fmt(obs.quality_status)}`),item(`standard样本：${fmt(obs.standard_sample_size)}`),item(`purged样本：${fmt(obs.purged_sample_size)}`),item(`leakage：${fmt(obs.leakage_status)}`),item(`baseline模型：${(ms.baseline_models||[]).join(", ")}`),item(`path模型：${(ms.path_models||[]).join(", ")}`),item(`P2定位：${fmt(ms.p2_role)}`)].join("");opportunity.innerHTML=Object.entries(d.path_opportunity_observation||{}).map(([k,v])=>card(k,v)).join("");risk.innerHTML=Object.entries(d.path_risk_observation||{}).map(([k,v])=>card(k,v)).join("");const c=d.model_consistency_summary||{},ec=d.evidence_conflict_summary||{};consistency.innerHTML=[item(`模型一致性：${fmt(c.model_consistency_level)}`),item(`P2定位：${fmt(c.p2_role)}`),item(`存在证据冲突：${fmt(ec.evidence_conflict)}`)].concat((c.model_disagreement_points||[]).map(item)).concat((ec.evidence_conflict_reasons||[]).map(item)).join("");attention.innerHTML=(d.human_attention_items||[]).map(x=>item(`[${x.category}] ${x.text}`)).join("");checklist.innerHTML=(d.human_review_checklist||[]).map(x=>item(`[${x.id}] ${x.text}`)).join("");guardrails.innerHTML=(d.forbidden_actions||[]).map(x=>chip("禁止",x,"bad")).concat([chip("下一阶段",d.next_stage)]).join("");footer.textContent=`generated_at: ${meta.generated_at}`}).catch(e=>overview.innerHTML=`<span class="bad">加载失败：${e}</span>`);</script></body></html>"""


if __name__ == "__main__":
    raise SystemExit(main())
