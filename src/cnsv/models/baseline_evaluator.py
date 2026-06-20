from __future__ import annotations

import math
from typing import Any

from cnsv.models.baseline_schema import FORBIDDEN_FIELD_TOKENS, HORIZONS


def _walk_keys(value: Any, prefix: str = "") -> list[str]:
    if isinstance(value, dict):
        keys: list[str] = []
        for key, inner in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            keys.append(path)
            keys.extend(_walk_keys(inner, path))
        return keys
    if isinstance(value, list):
        keys = []
        for index, inner in enumerate(value):
            keys.extend(_walk_keys(inner, f"{prefix}[{index}]"))
        return keys
    return []


def _walk_values(value: Any) -> list[Any]:
    if isinstance(value, dict):
        out: list[Any] = []
        for inner in value.values():
            out.extend(_walk_values(inner))
        return out
    if isinstance(value, list):
        out = []
        for inner in value:
            out.extend(_walk_values(inner))
        return out
    return [value]


def evaluate_baseline_models(models: dict[str, Any], horizons: tuple[int, ...] = HORIZONS) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    gating_warnings: list[str] = []
    non_gating_warnings: list[str] = []
    fallback_notes: list[dict[str, Any]] = []

    def add(name: str, status: str, detail: str, category: str = "gating") -> None:
        check = {"name": name, "status": status, "detail": detail, "category": category}
        checks.append(check)
        if status == "WARN":
            if category == "non_gating":
                non_gating_warnings.append(detail)
            else:
                gating_warnings.append(detail)

    expected_models = {"B0_random_walk", "B1_historical_distribution", "B2_state_grouped_distribution", "B3_volatility_adjusted"}
    missing_models = sorted(expected_models - set(models))
    add("required_models_present", "FAIL" if missing_models else "PASS", f"missing models: {missing_models}" if missing_models else "all baseline models present")

    forbidden = [key for key in _walk_keys(models) if any(token in key.lower() for token in FORBIDDEN_FIELD_TOKENS)]
    add("no_trade_signal_fields", "FAIL" if forbidden else "PASS", f"forbidden fields: {forbidden}" if forbidden else "no forbidden field names")

    bad_numbers = [value for value in _walk_values(models) if isinstance(value, float) and not math.isfinite(value)]
    add("finite_numbers", "FAIL" if bad_numbers else "PASS", "all numeric values are finite" if not bad_numbers else "nan or inf detected")

    for model_id, model in models.items():
        model_horizons = model.get("horizons", {})
        for horizon in horizons:
            key = f"{horizon}D"
            row = model_horizons.get(key)
            if not row:
                add(f"{model_id}.{key}.present", "FAIL", f"{model_id} missing {key}")
                continue
            add(f"{model_id}.{key}.present", "PASS", f"{model_id} {key} present")
            returns = [row.get(name) for name in ("p10_return", "p50_return", "p90_return")]
            if all(value is not None for value in returns):
                ordered = returns[0] <= returns[1] <= returns[2]
                add(f"{model_id}.{key}.quantiles", "PASS" if ordered else "FAIL", "quantile order ok" if ordered else "quantile order broken")
            full_returns = [row.get(name) for name in ("p05_return", "p10_return", "p25_return", "p50_return", "p75_return", "p90_return", "p95_return")]
            if all(value is not None for value in full_returns):
                full_ordered = all(left <= right for left, right in zip(full_returns, full_returns[1:]))
                add(
                    f"{model_id}.{key}.full_quantiles",
                    "PASS" if full_ordered else "FAIL",
                    "full quantile order ok" if full_ordered else "full quantile order broken",
                )
            prices = [row.get(name) for name in ("expected_price", "p10_price", "p50_price", "p90_price") if row.get(name) is not None]
            bad_price = [price for price in prices if price <= 0]
            add(f"{model_id}.{key}.prices", "PASS" if not bad_price else "FAIL", "prices positive" if not bad_price else "non-positive price detected")
            sample_size = row.get("sample_size", row.get("state_sample_size"))
            if isinstance(sample_size, int) and sample_size < 30:
                if row.get("fallback_used") is True:
                    reason = row.get("fallback_reason") or "state_sample_size_below_threshold"
                    note = {
                        "model": model_id,
                        "horizon": key,
                        "state_key": row.get("state_key") or model.get("state_key"),
                        "reason": reason,
                        "state_sample_size": sample_size,
                        "state_coverage": model.get("state_coverage", {}),
                        "fallback_method": row.get("fallback_method") or "B1_historical_distribution",
                        "gating": False,
                        "non_blocking": True,
                        "is_trade_signal": False,
                        "next_coverage_action": row.get("next_coverage_action")
                        or "extend historical state coverage for trend_state, volatility_state, and flow_strength_basic",
                    }
                    fallback_notes.append(note)
                    message = f"{model_id} {key} state sample below threshold; transparent fallback to B1, non-gating"
                    add(f"{model_id}.{key}.controlled_fallback", "PASS", message, category="non_gating")
                    non_gating_warnings.append(message)
                elif model_id != "B2_state_grouped_distribution":
                    add(f"{model_id}.{key}.sample_size", "WARN", "sample size below 30")

    failed_count = sum(1 for check in checks if check["status"] == "FAIL")
    gating_warning_count = len(gating_warnings)
    non_gating_warning_count = len(non_gating_warnings)
    status = "FAIL" if failed_count else "WARN" if gating_warning_count else "PASS"
    return {
        "status": status,
        "failed_count": failed_count,
        "warn_count": gating_warning_count,
        "blocking_error_count": failed_count,
        "gating_warning_count": gating_warning_count,
        "non_gating_warning_count": non_gating_warning_count,
        "fallback_count": len(fallback_notes),
        "checks": checks,
        "warnings": gating_warnings,
        "gating_warnings": gating_warnings,
        "non_gating_warnings": non_gating_warnings,
        "fallback_notes": fallback_notes,
    }
