from __future__ import annotations

import math
from typing import Any

from cnsv.models.baseline_schema import HORIZONS
from cnsv.path import PATH_MODEL_IDS

FORBIDDEN_OUTPUT_KEYS = ("buy_signal", "sell_signal", "target_position", "target_shares", "stop_loss", "take_profit", "formal_signal")
PROB_KEYS = (
    "positive_terminal_prob",
    "touch_up_3pct_prob",
    "touch_up_5pct_prob",
    "touch_up_8pct_prob",
    "touch_down_3pct_prob",
    "touch_down_5pct_prob",
    "touch_down_8pct_prob",
    "end_above_start_prob",
    "intraperiod_any_up_prob",
    "intraperiod_any_down_prob",
)


def evaluate_path_quality(models: dict[str, Any], latest_close: float | None, horizons: tuple[int, ...] = HORIZONS) -> dict[str, Any]:
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

    add("latest_close_positive", _finite_positive(latest_close), f"latest_close={latest_close}")
    add("no_forbidden_trade_fields", not contains_forbidden_path_key(models), "path payload must not contain trade action fields")
    for model_id in PATH_MODEL_IDS:
        model = models.get(model_id, {})
        add(f"{model_id}.present", bool(model), f"{model_id} present")
        for horizon in horizons:
            row = (model.get("horizons") or {}).get(f"{horizon}D", {})
            add(f"{model_id}.{horizon}D.present", bool(row), f"{model_id} {horizon}D present")
            if not row:
                continue
            add(f"{model_id}.{horizon}D.path_count", (row.get("path_count") or 0) > 0, f"path_count={row.get('path_count')}")
            add(f"{model_id}.{horizon}D.quantile_order", _quantile_order(row), "p10 <= p50 <= p90")
            add(f"{model_id}.{horizon}D.price_positive", _prices_positive(row), "price quantiles must be positive")
            add(f"{model_id}.{horizon}D.probabilities", _probabilities_valid(row), "probabilities must be in [0,1]")
            add(f"{model_id}.{horizon}D.fallback_reason", not row.get("fallback_used") or bool(row.get("fallback_reason")), f"fallback_used={row.get('fallback_used')}")
            if model_id == "P2_state_conditional_path":
                sample_size = row.get("state_sample_size") or row.get("path_count") or 0
                add(f"{model_id}.{horizon}D.state_sample_size", sample_size >= 30 or bool(row.get("fallback_used")), f"state_sample_size={sample_size}", warning=True)
                add(f"{model_id}.{horizon}D.fallback_transparent", sample_size >= 30 or row.get("source_model") == "P1_volatility_adjusted_path", f"source_model={row.get('source_model')}")
            if row.get("dropped_count"):
                add(f"{model_id}.{horizon}D.dropped_paths", False, f"dropped_count={row.get('dropped_count')}", warning=True)
            if row.get("volatility_scale_warnings"):
                add(f"{model_id}.{horizon}D.volatility_scale_warning", False, ",".join(row.get("volatility_scale_warnings") or []), warning=True)
            add(f"{model_id}.{horizon}D.finite_values", _finite_tree(row), "no NaN/inf")
    status = "FAIL" if failed else "WARN" if warn else "PASS"
    return {"status": status, "failed_count": failed, "warn_count": warn, "blocking_error_count": failed, "checks": checks}


def contains_forbidden_path_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, inner in value.items():
            lower = str(key).lower()
            if any(token == lower or token in lower for token in FORBIDDEN_OUTPUT_KEYS):
                return True
            if contains_forbidden_path_key(inner):
                return True
    if isinstance(value, list):
        return any(contains_forbidden_path_key(item) for item in value)
    return False


def _finite_positive(value: Any) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number) and number > 0


def _quantile_order(row: dict[str, Any]) -> bool:
    prefixes = ("terminal_return", "terminal_price", "max_up_return", "max_up_price", "max_down_return", "max_down_price", "max_drawdown")
    for prefix in prefixes:
        values = [row.get(f"{prefix}_p10"), row.get(f"{prefix}_p50"), row.get(f"{prefix}_p90")]
        if any(v is None for v in values):
            return False
        if not float(values[0]) <= float(values[1]) <= float(values[2]):
            return False
    return True


def _prices_positive(row: dict[str, Any]) -> bool:
    keys = [key for key in row if key.endswith("_price_p10") or key.endswith("_price_p50") or key.endswith("_price_p90")]
    return bool(keys) and all(_finite_positive(row.get(key)) for key in keys)


def _probabilities_valid(row: dict[str, Any]) -> bool:
    for key in PROB_KEYS:
        value = row.get(key)
        if value is None:
            return False
        try:
            number = float(value)
        except (TypeError, ValueError):
            return False
        if not math.isfinite(number) or not 0 <= number <= 1:
            return False
    return True


def _finite_tree(value: Any) -> bool:
    if isinstance(value, dict):
        return all(_finite_tree(inner) for inner in value.values())
    if isinstance(value, list):
        return all(_finite_tree(item) for item in value)
    if isinstance(value, float):
        return math.isfinite(value)
    return True
