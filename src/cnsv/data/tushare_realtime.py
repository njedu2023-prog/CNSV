from __future__ import annotations

import os
import time
from datetime import datetime
from typing import Any, Callable
from zoneinfo import ZoneInfo

import pandas as pd
import requests

BEIJING_TIMEZONE = ZoneInfo("Asia/Shanghai")
TUSHARE_API_URL = "https://api.tushare.pro"
TUSHARE_REALTIME_API = "rt_min_daily"
TARGET_TS_CODE = "600150.SH"
MARKET_OPEN = "09:30:00"
MORNING_CLOSE = "11:30:00"
AFTERNOON_OPEN = "13:00:00"
MARKET_CLOSE = "15:00:00"
REALTIME_FETCH_ATTEMPTS = 3
MAX_REALTIME_TRADING_MINUTE_LAG = 5
MIN_REALTIME_COVERAGE = 0.95
MIN_EARLY_SESSION_COVERAGE = 0.80

REALTIME_MINUTE_COLUMNS = (
    "ts_code",
    "trade_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "vol",
    "amount",
    "source",
    "fetched_at",
)


def market_phase(now: datetime) -> str:
    current = now.astimezone(BEIJING_TIMEZONE).strftime("%H:%M:%S")
    if current < MARKET_OPEN:
        return "preopen"
    if current <= MORNING_CLOSE:
        return "morning"
    if current < AFTERNOON_OPEN:
        return "lunch_break"
    if current <= MARKET_CLOSE:
        return "afternoon"
    return "postclose"


def fetch_realtime_minutes(
    *,
    token: str | None = None,
    now: datetime | None = None,
    post: Callable[..., Any] | None = None,
    timeout: int = 25,
) -> pd.DataFrame:
    current = (now or datetime.now(BEIJING_TIMEZONE)).astimezone(BEIJING_TIMEZONE)
    if market_phase(current) == "preopen":
        return _empty_minutes()

    api_token = (token or os.getenv("TUSHARE_TOKEN", "")).strip()
    if not api_token:
        raise RuntimeError("TUSHARE_TOKEN is not configured for CNSV realtime prediction")

    sender = post or requests.post
    payload = _request_realtime_payload(api_token, sender, timeout)
    data = payload.get("data") or {}
    fields = data.get("fields") or []
    items = data.get("items") or []
    if not fields or not items:
        return _empty_minutes()
    frame = pd.DataFrame(items, columns=fields)
    return _normalize_realtime_minutes(frame, current)


def probe_realtime_connection(
    *,
    token: str | None = None,
    post: Callable[..., Any] | None = None,
    timeout: int = 25,
) -> dict[str, Any]:
    api_token = (token or os.getenv("TUSHARE_TOKEN", "")).strip()
    if not api_token:
        raise RuntimeError("TUSHARE_TOKEN is not configured for CNSV realtime prediction")

    payload = _request_realtime_payload(api_token, post or requests.post, timeout)
    data = payload.get("data") or {}
    if not isinstance(data, dict):
        raise RuntimeError("Tushare realtime response data is not a JSON object")
    fields = data.get("fields") or []
    items = data.get("items") or []
    if not isinstance(fields, list) or not isinstance(items, list):
        raise RuntimeError("Tushare realtime response fields or items is invalid")
    return {
        "status": "PASS",
        "data_source": "Tushare direct realtime",
        "data_endpoint": TUSHARE_REALTIME_API,
        "returned_rows": len(items),
    }


def _request_realtime_payload(
    api_token: str,
    sender: Callable[..., Any],
    timeout: int,
) -> dict[str, Any]:
    payload: Any = None
    last_error: Exception | None = None
    for attempt in range(1, REALTIME_FETCH_ATTEMPTS + 1):
        try:
            response = sender(
                TUSHARE_API_URL,
                json={
                    "api_name": TUSHARE_REALTIME_API,
                    "token": api_token,
                    "params": {"ts_code": TARGET_TS_CODE, "freq": "1MIN"},
                    "fields": "",
                },
                timeout=timeout,
            )
            response.raise_for_status()
            payload = response.json()
            break
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            if attempt < REALTIME_FETCH_ATTEMPTS:
                time.sleep(2 ** (attempt - 1))
    if payload is None:
        raise RuntimeError(
            f"Tushare {TUSHARE_REALTIME_API} request failed after "
            f"{REALTIME_FETCH_ATTEMPTS} attempts: {last_error}"
        ) from last_error
    if not isinstance(payload, dict):
        raise RuntimeError("Tushare realtime response is not a JSON object")
    if payload.get("code") not in (0, None):
        message = str(payload.get("msg") or "unknown error").strip()
        raise RuntimeError(f"Tushare {TUSHARE_REALTIME_API} failed: code={payload.get('code')} msg={message}")
    return payload


def build_realtime_ready(
    minutes: pd.DataFrame,
    *,
    now: datetime | None = None,
    trade_calendar: pd.DataFrame | None = None,
) -> dict[str, Any]:
    current = (now or datetime.now(BEIJING_TIMEZONE)).astimezone(BEIJING_TIMEZONE)
    current_date = current.date().isoformat()
    phase = market_phase(current)
    trading_day, calendar_reason = _trading_day_state(trade_calendar, current_date)
    frame = minutes.copy() if isinstance(minutes, pd.DataFrame) else _empty_minutes()
    if not frame.empty and "trade_time" in frame:
        parsed = pd.to_datetime(frame["trade_time"], errors="coerce")
        cutoff = min(
            current.replace(tzinfo=None),
            current.replace(hour=15, minute=0, second=0, microsecond=0, tzinfo=None),
        )
        frame = frame[
            (parsed.dt.strftime("%Y-%m-%d") == current_date)
            & (parsed <= cutoff)
        ].copy()
        frame = frame.sort_values("trade_time")

    expected_times = _expected_minute_times(current_date)
    expected_last = _expected_last_minute(current, expected_times)
    expected_rows = [item for item in expected_times if expected_last and item <= expected_last]
    observed_times = (
        set(pd.to_datetime(frame["trade_time"], errors="coerce").dropna())
        if "trade_time" in frame else set()
    )
    observed_expected = [item for item in expected_rows if item in observed_times]
    coverage_ratio = len(observed_expected) / len(expected_rows) if expected_rows else None
    latest = frame.tail(1) if "trade_time" in frame else frame.iloc[0:0]
    last_trade_time = str(latest.iloc[0]["trade_time"]) if not latest.empty else ""
    trading_minute_lag = _trading_minute_lag(expected_rows, last_trade_time)
    quality_errors = _minute_quality_errors(frame)
    required_coverage = (
        MIN_EARLY_SESSION_COVERAGE if len(expected_rows) < 20 else MIN_REALTIME_COVERAGE
    )
    stale = trading_minute_lag is None or trading_minute_lag > MAX_REALTIME_TRADING_MINUTE_LAG
    incomplete = coverage_ratio is None or coverage_ratio < required_coverage

    if trading_day is None:
        status = "FAIL"
        blocking_reason = calendar_reason
    elif not trading_day:
        status = "SKIP"
        blocking_reason = "non_trading_day"
    elif phase == "preopen":
        status = "SKIP"
        blocking_reason = "preopen_no_continuous_auction_minute"
    elif latest.empty:
        status = "FAIL"
        blocking_reason = "tushare_realtime_minutes_unavailable"
    elif quality_errors:
        status = "FAIL"
        blocking_reason = "tushare_realtime_quality_failed:" + ",".join(quality_errors)
    elif stale:
        status = "FAIL"
        blocking_reason = "tushare_realtime_minutes_stale"
    elif incomplete:
        status = "FAIL"
        blocking_reason = "tushare_realtime_minutes_incomplete"
    else:
        status = "PASS"
        blocking_reason = None
    ready = status == "PASS"

    parsed_latest = pd.to_datetime(last_trade_time, errors="coerce")
    lag_minutes = None
    if pd.notna(parsed_latest):
        lag_minutes = max(
            0.0,
            (current.replace(tzinfo=None) - parsed_latest.to_pydatetime()).total_seconds() / 60.0,
        )
    return {
        "line": "cnsv_direct_tushare_realtime_20m",
        "status": status,
        "ready": ready,
        "can_predict_intraday": ready,
        "market_phase": phase,
        "trade_date": current_date if not latest.empty else "",
        "expected_trade_date": current_date if trading_day else "",
        "asof_time": last_trade_time[-8:] if last_trade_time else "",
        "last_valid_trade_time": last_trade_time,
        "asof_price": (
            float(latest.iloc[0]["close"])
            if not latest.empty and "close" in latest else None
        ),
        "minute_rows_today": int(len(frame)),
        "lag_minutes": round(lag_minutes, 2) if lag_minutes is not None else None,
        "expected_asof_time": expected_last.strftime("%H:%M:%S") if expected_last else "",
        "expected_minute_rows": int(len(expected_rows)),
        "observed_expected_minute_rows": int(len(observed_expected)),
        "coverage_ratio": round(coverage_ratio, 4) if coverage_ratio is not None else None,
        "required_coverage_ratio": required_coverage if expected_rows else None,
        "trading_minute_lag": trading_minute_lag,
        "max_trading_minute_lag": MAX_REALTIME_TRADING_MINUTE_LAG,
        "calendar_status": "PASS" if trading_day is not None else "FAIL",
        "calendar_reason": calendar_reason,
        "quality_errors": quality_errors,
        "refresh_interval_minutes": 20,
        "data_source": "Tushare direct realtime",
        "data_endpoint": TUSHARE_REALTIME_API,
        "prediction_target": "next_trading_day_close_vs_current_trade_day_close",
        "future_data_guard": "current-day features use only trade_time <= reported asof_time",
        "schedule_window_beijing": "09:15-11:30,13:02-15:10; final 20:04",
        "blocking_reason": blocking_reason,
        "created_at": current.strftime("%Y-%m-%d %H:%M:%S"),
    }


def merge_intraday_history(history: pd.DataFrame, current: pd.DataFrame) -> pd.DataFrame:
    frames = [frame.copy() for frame in (history, current) if isinstance(frame, pd.DataFrame) and not frame.empty]
    if not frames:
        return pd.DataFrame()
    merged = pd.concat(frames, ignore_index=True, sort=False)
    if "trade_time" not in merged:
        raise KeyError("trade_time")
    merged["trade_time"] = pd.to_datetime(merged["trade_time"], errors="coerce")
    merged = merged.dropna(subset=["trade_time"]).sort_values("trade_time")
    merged = merged.drop_duplicates("trade_time", keep="last")
    merged["trade_time"] = merged["trade_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return merged.reset_index(drop=True)


def _normalize_realtime_minutes(frame: pd.DataFrame, current: datetime) -> pd.DataFrame:
    renamed = frame.rename(columns={"code": "ts_code", "time": "trade_time", "vol": "volume"}).copy()
    required = {"trade_time", "open", "high", "low", "close"}
    missing = sorted(required.difference(renamed.columns))
    if missing:
        raise RuntimeError(f"Tushare realtime response missing fields: {','.join(missing)}")
    if "ts_code" not in renamed:
        renamed["ts_code"] = TARGET_TS_CODE
    renamed["ts_code"] = renamed["ts_code"].astype(str).str.upper()
    invalid_symbols = sorted(set(renamed.loc[renamed["ts_code"] != TARGET_TS_CODE, "ts_code"]))
    if invalid_symbols:
        raise RuntimeError(
            "Tushare realtime response contains unexpected symbols: " + ",".join(invalid_symbols)
        )
    renamed["trade_time"] = pd.to_datetime(renamed["trade_time"], errors="coerce")
    if renamed["trade_time"].isna().any():
        raise RuntimeError("Tushare realtime response contains invalid trade_time")
    current_date = current.date().isoformat()
    cutoff = min(current.replace(tzinfo=None), current.replace(hour=15, minute=0, second=0, microsecond=0, tzinfo=None))
    clock = renamed["trade_time"].dt.strftime("%H:%M:%S")
    in_session = (
        ((clock >= MARKET_OPEN) & (clock <= MORNING_CLOSE))
        | ((clock >= AFTERNOON_OPEN) & (clock <= MARKET_CLOSE))
    )
    renamed = renamed[
        (renamed["trade_time"].dt.strftime("%Y-%m-%d") == current_date)
        & (renamed["trade_time"] <= cutoff)
        & in_session
    ].copy()
    for column in ("open", "high", "low", "close", "volume", "amount"):
        if column not in renamed:
            renamed[column] = 0.0
        renamed[column] = pd.to_numeric(renamed[column], errors="coerce")
    quality_errors = _minute_quality_errors(renamed)
    if quality_errors:
        raise RuntimeError("Tushare realtime response quality failed: " + ",".join(quality_errors))
    renamed["vol"] = renamed["volume"]
    renamed["source"] = f"tushare.{TUSHARE_REALTIME_API}"
    renamed["fetched_at"] = current.strftime("%Y-%m-%d %H:%M:%S")
    renamed = renamed.sort_values("trade_time").drop_duplicates("trade_time", keep="last")
    renamed["trade_time"] = renamed["trade_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return renamed.loc[:, REALTIME_MINUTE_COLUMNS].reset_index(drop=True)


def _trading_day_state(
    calendar: pd.DataFrame | None, current_date: str
) -> tuple[bool | None, str | None]:
    if not isinstance(calendar, pd.DataFrame) or calendar.empty:
        return None, "trade_calendar_unavailable"
    column = "cal_date" if "cal_date" in calendar else "trade_date" if "trade_date" in calendar else None
    if not column or "is_open" not in calendar:
        return None, "trade_calendar_schema_invalid"
    dates = calendar[column].astype(str).str[:10].str.replace("-", "", regex=False)
    target = current_date.replace("-", "")
    matches = calendar[dates == target]
    if matches.empty:
        return None, "trade_calendar_missing_current_date"
    is_open = pd.to_numeric(matches["is_open"], errors="coerce")
    if is_open.isna().all():
        return None, "trade_calendar_is_open_invalid"
    return bool((is_open == 1).any()), None


def _expected_minute_times(current_date: str) -> list[pd.Timestamp]:
    morning = pd.date_range(f"{current_date} 09:30:00", f"{current_date} 11:30:00", freq="1min")
    afternoon = pd.date_range(f"{current_date} 13:01:00", f"{current_date} 15:00:00", freq="1min")
    return [*morning, *afternoon]


def _expected_last_minute(current: datetime, expected: list[pd.Timestamp]) -> pd.Timestamp | None:
    if market_phase(current) == "preopen" or not expected:
        return None
    naive = pd.Timestamp(current.replace(tzinfo=None, second=0, microsecond=0))
    eligible = [item for item in expected if item <= naive]
    return eligible[-1] if eligible else None


def _trading_minute_lag(expected_rows: list[pd.Timestamp], last_trade_time: str) -> int | None:
    if not expected_rows or not last_trade_time:
        return None
    latest = pd.to_datetime(last_trade_time, errors="coerce")
    if pd.isna(latest):
        return None
    observed_index = -1
    for index, item in enumerate(expected_rows):
        if item <= latest:
            observed_index = index
    return max(0, len(expected_rows) - 1 - observed_index)


def _minute_quality_errors(frame: pd.DataFrame) -> list[str]:
    if frame.empty:
        return []
    required = ("trade_time", "open", "high", "low", "close", "volume", "amount")
    missing = [column for column in required if column not in frame]
    if missing:
        return ["missing_" + "_".join(missing)]
    numeric = frame.loc[:, ("open", "high", "low", "close", "volume", "amount")].apply(
        pd.to_numeric, errors="coerce"
    )
    errors: list[str] = []
    if numeric.isna().any().any():
        errors.append("non_numeric_values")
    prices = numeric.loc[:, ("open", "high", "low", "close")]
    if (prices <= 0).any().any():
        errors.append("non_positive_price")
    invalid_ohlc = (
        (numeric["low"] > numeric[["open", "close"]].min(axis=1))
        | (numeric["high"] < numeric[["open", "close"]].max(axis=1))
        | (numeric["low"] > numeric["high"])
    )
    if invalid_ohlc.any():
        errors.append("invalid_ohlc")
    if (numeric[["volume", "amount"]] < 0).any().any():
        errors.append("negative_volume_or_amount")
    if "ts_code" in frame and (frame["ts_code"].astype(str).str.upper() != TARGET_TS_CODE).any():
        errors.append("unexpected_symbol")
    if pd.to_datetime(frame["trade_time"], errors="coerce").isna().any():
        errors.append("invalid_trade_time")
    return errors


def _empty_minutes() -> pd.DataFrame:
    return pd.DataFrame(columns=REALTIME_MINUTE_COLUMNS)
