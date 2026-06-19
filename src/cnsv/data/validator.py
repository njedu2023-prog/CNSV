from __future__ import annotations

from typing import Any

import pandas as pd


def _latest_date(df: pd.DataFrame) -> str:
    for column in ("trade_date", "date"):
        if column in df.columns and not df.empty:
            return str(df[column].max())
    return ""


def validate_loaded_data(bundle: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(name: str, status: str, detail: str) -> None:
        checks.append({"name": name, "status": status, "detail": detail})

    daily = bundle.get("daily")
    one_min = bundle.get("one_min")
    moneyflow = bundle.get("moneyflow")

    add("daily_non_empty", "PASS" if isinstance(daily, pd.DataFrame) and not daily.empty else "FAIL", "daily must not be empty")
    add("one_min_non_empty", "PASS" if isinstance(one_min, pd.DataFrame) and not one_min.empty else "FAIL", "1min must not be empty")
    add("moneyflow_non_empty", "PASS" if isinstance(moneyflow, pd.DataFrame) and not moneyflow.empty else "FAIL", "moneyflow must not be empty")

    for name, df, fields in (
        ("daily", daily, {"trade_date", "close"}),
        ("one_min", one_min, {"trade_date", "close"}),
        ("moneyflow", moneyflow, {"trade_date"}),
    ):
        missing = fields - set(getattr(df, "columns", []))
        add(f"{name}_core_fields", "PASS" if not missing else "FAIL", f"missing fields: {sorted(missing)}")

    daily_date = _latest_date(daily) if isinstance(daily, pd.DataFrame) else ""
    minute_date = _latest_date(one_min) if isinstance(one_min, pd.DataFrame) else ""
    moneyflow_date = _latest_date(moneyflow) if isinstance(moneyflow, pd.DataFrame) else ""
    if daily_date and minute_date:
        add("latest_trade_date_daily_vs_1min", "PASS" if daily_date == minute_date else "WARN", f"daily={daily_date}, one_min={minute_date}")
    if daily_date and moneyflow_date:
        add("latest_trade_date_daily_vs_moneyflow", "PASS" if daily_date == moneyflow_date else "WARN", f"daily={daily_date}, moneyflow={moneyflow_date}")

    if isinstance(daily, pd.DataFrame) and isinstance(one_min, pd.DataFrame) and not daily.empty and not one_min.empty and "close" in daily and "close" in one_min:
        daily_close = float(daily.sort_values("trade_date").iloc[-1]["close"]) if "trade_date" in daily else float(daily.iloc[-1]["close"])
        minute_close = float(one_min.sort_values([c for c in ("trade_date", "datetime", "time") if c in one_min.columns]).iloc[-1]["close"])
        rel_diff = abs(daily_close - minute_close) / max(abs(daily_close), 1e-9)
        add("daily_close_vs_1min_latest_close", "PASS" if rel_diff <= 0.03 else "WARN", f"relative diff={rel_diff:.4f}")

    failed_count = sum(1 for check in checks if check["status"] == "FAIL")
    warn_count = sum(1 for check in checks if check["status"] == "WARN")
    status = "FAIL" if failed_count else "WARN" if warn_count else "PASS"
    return {"status": status, "failed_count": failed_count, "warn_count": warn_count, "checks": checks}
