from __future__ import annotations

import math
from typing import Any

import pandas as pd


CORE_FEATURES = {
    "price_volume": ("latest_close", "latest_amount", "ret_1d"),
    "minute_structure": ("latest_intraday_close", "intraday_range_pct"),
    "moneyflow": ("net_mf_amount", "main_force_net", "flow_strength_score"),
    "trend": ("trend_state",),
    "volatility": ("volatility_state",),
}


def _latest_date(df: pd.DataFrame) -> str:
    if "trade_date" in df.columns and not df.empty:
        return str(df["trade_date"].max())
    return ""


def _flatten(prefix: str, value: Any) -> list[tuple[str, Any]]:
    if isinstance(value, dict):
        items: list[tuple[str, Any]] = []
        for key, inner in value.items():
            items.extend(_flatten(f"{prefix}.{key}" if prefix else str(key), inner))
        return items
    if isinstance(value, list):
        return [(f"{prefix}[{index}]", item) for index, item in enumerate(value)]
    return [(prefix, value)]


def _is_nan(value: Any) -> bool:
    return isinstance(value, float) and math.isnan(value)


def _is_inf(value: Any) -> bool:
    return isinstance(value, float) and math.isinf(value)


def check_feature_quality(features: dict[str, Any], data_bundle: dict[str, Any], gate: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, str]] = []

    def add(name: str, status: str, detail: str) -> None:
        checks.append({"name": name, "status": status, "detail": detail})

    for category in ("price_volume", "minute_structure", "moneyflow", "trend", "volatility"):
        value = features.get(category)
        add(f"{category}_non_empty", "PASS" if isinstance(value, dict) and bool(value) else "FAIL", f"{category} features must not be empty")

    for category, fields in CORE_FEATURES.items():
        category_features = features.get(category) or {}
        for field in fields:
            status = "PASS" if category_features.get(field) not in (None, "") else "FAIL"
            add(f"{category}.{field}", status, f"{category}.{field} is required")

    for name, value in _flatten("", features):
        if _is_inf(value):
            add(f"finite:{name}", "FAIL", f"{name} is infinite")
        elif _is_nan(value):
            add(f"finite:{name}", "FAIL", f"{name} is NaN")
        elif value is None and any(name.startswith(prefix) for prefix in ("price_volume.", "minute_structure.", "moneyflow.", "trend.", "volatility.")):
            add(f"nullable:{name}", "WARN", f"{name} is null")

    if not gate.get("can_use_moneyflow_as_strong_factor", False):
        add("moneyflow_strong_factor_gate", "WARN", "moneyflow is not allowed as strong factor by CNSVdata gate")
    else:
        add("moneyflow_strong_factor_gate", "PASS", "moneyflow can be used as strong factor")

    for key, minimum in (("daily", 60), ("one_min", 60), ("moneyflow", 10)):
        df = data_bundle.get(key)
        ok = isinstance(df, pd.DataFrame) and len(df) >= minimum
        add(f"{key}_row_count", "PASS" if ok else "FAIL", f"{key} rows must be >= {minimum}")

    daily = data_bundle.get("daily")
    one_min = data_bundle.get("one_min")
    moneyflow = data_bundle.get("moneyflow")
    daily_date = _latest_date(daily) if isinstance(daily, pd.DataFrame) else ""
    minute_date = _latest_date(one_min) if isinstance(one_min, pd.DataFrame) else ""
    moneyflow_date = _latest_date(moneyflow) if isinstance(moneyflow, pd.DataFrame) else ""
    if daily_date and minute_date:
        add("latest_trade_date_daily_vs_1min", "PASS" if daily_date == minute_date else "WARN", f"daily={daily_date}, one_min={minute_date}")
    if daily_date and moneyflow_date:
        add("latest_trade_date_daily_vs_moneyflow", "PASS" if daily_date == moneyflow_date else "WARN", f"daily={daily_date}, moneyflow={moneyflow_date}")

    failed_count = sum(1 for check in checks if check["status"] == "FAIL")
    warn_count = sum(1 for check in checks if check["status"] == "WARN")
    status = "FAIL" if failed_count else "WARN" if warn_count else "PASS"
    return {"status": status, "failed_count": failed_count, "warn_count": warn_count, "checks": checks}
