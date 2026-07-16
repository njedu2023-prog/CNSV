from __future__ import annotations

import os
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
    if not isinstance(payload, dict):
        raise RuntimeError("Tushare realtime response is not a JSON object")
    if payload.get("code") not in (0, None):
        message = str(payload.get("msg") or "unknown error").strip()
        raise RuntimeError(f"Tushare {TUSHARE_REALTIME_API} failed: code={payload.get('code')} msg={message}")

    data = payload.get("data") or {}
    fields = data.get("fields") or []
    items = data.get("items") or []
    if not fields or not items:
        return _empty_minutes()
    frame = pd.DataFrame(items, columns=fields)
    return _normalize_realtime_minutes(frame, current)


def build_realtime_ready(
    minutes: pd.DataFrame,
    *,
    now: datetime | None = None,
    trade_calendar: pd.DataFrame | None = None,
) -> dict[str, Any]:
    current = (now or datetime.now(BEIJING_TIMEZONE)).astimezone(BEIJING_TIMEZONE)
    current_date = current.date().isoformat()
    phase = market_phase(current)
    trading_day = _is_trading_day(trade_calendar, current_date)
    frame = minutes.copy() if isinstance(minutes, pd.DataFrame) else _empty_minutes()
    if not frame.empty:
        parsed = pd.to_datetime(frame["trade_time"], errors="coerce")
        frame = frame[parsed.dt.strftime("%Y-%m-%d") == current_date].copy()
        frame = frame.sort_values("trade_time")

    latest = frame.tail(1)
    last_trade_time = str(latest.iloc[0]["trade_time"]) if not latest.empty else ""
    ready = bool(trading_day and phase != "preopen" and not latest.empty)
    if not trading_day:
        status = "SKIP"
        blocking_reason = "non_trading_day"
    elif phase == "preopen":
        status = "SKIP"
        blocking_reason = "preopen_no_continuous_auction_minute"
    elif latest.empty:
        status = "FAIL"
        blocking_reason = "tushare_realtime_minutes_unavailable"
    else:
        status = "PASS"
        blocking_reason = None

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
        "asof_price": float(latest.iloc[0]["close"]) if not latest.empty else None,
        "minute_rows_today": int(len(frame)),
        "lag_minutes": round(lag_minutes, 2) if lag_minutes is not None else None,
        "refresh_interval_minutes": 20,
        "data_source": "Tushare direct realtime",
        "data_endpoint": TUSHARE_REALTIME_API,
        "prediction_target": "next_trading_day_close_vs_current_trade_day_close",
        "future_data_guard": "current-day features use only trade_time <= reported asof_time",
        "schedule_window_beijing": "09:15-11:30,13:00-15:10; final 20:04",
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
    renamed["ts_code"] = renamed.get("ts_code", TARGET_TS_CODE)
    renamed["trade_time"] = pd.to_datetime(renamed["trade_time"], errors="coerce")
    renamed = renamed.dropna(subset=["trade_time"]).copy()
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
    renamed["vol"] = renamed["volume"]
    renamed["source"] = f"tushare.{TUSHARE_REALTIME_API}"
    renamed["fetched_at"] = current.strftime("%Y-%m-%d %H:%M:%S")
    renamed = renamed.sort_values("trade_time").drop_duplicates("trade_time", keep="last")
    renamed["trade_time"] = renamed["trade_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return renamed.loc[:, REALTIME_MINUTE_COLUMNS].reset_index(drop=True)


def _is_trading_day(calendar: pd.DataFrame | None, current_date: str) -> bool:
    if isinstance(calendar, pd.DataFrame) and not calendar.empty:
        column = "cal_date" if "cal_date" in calendar else "trade_date" if "trade_date" in calendar else None
        if column:
            dates = calendar[column].astype(str).str[:10].str.replace("-", "", regex=False)
            target = current_date.replace("-", "")
            matches = calendar[dates == target]
            if not matches.empty:
                if "is_open" not in matches:
                    return True
                return bool((pd.to_numeric(matches["is_open"], errors="coerce") == 1).any())
    return pd.Timestamp(current_date).weekday() < 5


def _empty_minutes() -> pd.DataFrame:
    return pd.DataFrame(columns=REALTIME_MINUTE_COLUMNS)
