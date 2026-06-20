from __future__ import annotations

from typing import Any

from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS
from cnsv.path import PATH_MODEL_IDS


FORBIDDEN_BACKTEST_KEYS = {
    "buy_signal",
    "sell_signal",
    "target_position",
    "target_shares",
    "stop_loss",
    "take_profit",
    "formal_signal",
    "target_price",
    "trade_recommendation",
}


def evaluate_observation_backtest(payload: dict[str, Any]) -> dict[str, Any]:
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

    scope = payload.get("backtest_scope", {})
    metrics = payload.get("model_backtest_metrics", {}).get("standard_walk_forward", {})
    purged = payload.get("model_backtest_metrics", {}).get("purged_walk_forward", {})
    leakage = payload.get("observation_backtest_leakage_checks", {})
    add("is_trade_signal_false", payload.get("meta", {}).get("is_trade_signal") is False, "observation backtest is not a trade signal")
    add("no_forbidden_trade_fields", not _contains_forbidden_key(payload), "no buy/sell/position/target fields")
    add("forbidden_actions_present", set(FORBIDDEN_ACTIONS).issubset(set(payload.get("forbidden_actions", []))), "formal_signal_generation, auto_order, broker_api required")
    add("leakage_checks_pass", leakage.get("status") == "PASS", f"leakage={leakage.get('status')}")
    add("standard_samples_present", (scope.get("standard_sample_size") or 0) > 0, f"standard_sample_size={scope.get('standard_sample_size')}")
    add("purged_samples_present", (scope.get("purged_sample_size") or 0) > 0, f"purged_sample_size={scope.get('purged_sample_size')}")
    for model_id in PATH_MODEL_IDS:
        add(f"{model_id}.standard_present", model_id in metrics, f"{model_id} standard metrics")
        add(f"{model_id}.purged_present", model_id in purged, f"{model_id} purged metrics")
        for horizon in ("5D", "10D", "20D"):
            row = metrics.get(model_id, {}).get(horizon, {})
            add(f"{model_id}.{horizon}.sample_size", (row.get("sample_size") or 0) > 0, f"sample_size={row.get('sample_size')}")
            add(f"{model_id}.{horizon}.probabilities", _probabilities_valid(row), "probabilities and rates in [0,1]")
            add(f"{model_id}.{horizon}.finite", _finite(row), "no NaN/inf")
    buckets = payload.get("observation_bucket_metrics", {})
    add("touch_probability_groups", bool(buckets.get("touch_probability_groups")), "touch probability buckets exist")
    add("drawdown_risk_groups", bool(buckets.get("drawdown_risk_groups")), "drawdown risk buckets exist")
    add("upside_path_groups", bool(buckets.get("upside_path_groups")), "upside path buckets exist")
    add("model_comparison", bool(payload.get("model_comparison")), "P0/P1/P2 comparison exists")
    add("condition_quality", bool(payload.get("observation_condition_quality")), "condition quality exists", warning=True)
    status = "FAIL" if failed else "WARN" if warn else "PASS"
    return {"status": status, "failed_count": failed, "warn_count": warn, "blocking_error_count": failed, "checks": checks}


def _contains_forbidden_key(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(k) in FORBIDDEN_BACKTEST_KEYS or _contains_forbidden_key(v) for k, v in value.items())
    if isinstance(value, list):
        return any(_contains_forbidden_key(v) for v in value)
    return False


def _probabilities_valid(row: dict[str, Any]) -> bool:
    for key, value in row.items():
        if value is not None and ("rate" in key or "coverage" in key or "brier" in key):
            f = float(value)
            if f < 0 or f > 1:
                return False
    return True


def _finite(value: Any) -> bool:
    if isinstance(value, dict):
        return all(_finite(v) for v in value.values())
    if isinstance(value, list):
        return all(_finite(v) for v in value)
    if isinstance(value, float):
        return value == value and value not in (float("inf"), float("-inf"))
    return True
