from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import pytest
import requests

from cnsv.data.tushare_realtime import (
    build_realtime_ready,
    fetch_realtime_minutes,
    merge_intraday_history,
)

BEIJING = ZoneInfo("Asia/Shanghai")


class _Response:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def _calendar():
    return pd.DataFrame({"cal_date": ["20260717", "20260718"], "is_open": [1, 0]})


def _complete_minutes(end: str) -> pd.DataFrame:
    date = "2026-07-17"
    times = [
        *pd.date_range(f"{date} 09:30:00", f"{date} 11:30:00", freq="1min"),
        *pd.date_range(f"{date} 13:01:00", f"{date} {end}", freq="1min"),
    ]
    return pd.DataFrame({
        "ts_code": "600150.SH",
        "trade_time": [item.strftime("%Y-%m-%d %H:%M:%S") for item in times],
        "open": 33.0,
        "high": 33.3,
        "low": 32.9,
        "close": 33.25,
        "volume": 100.0,
        "amount": 3325.0,
    })


def test_preopen_checkpoint_does_not_call_tushare():
    def fail_post(*args, **kwargs):
        raise AssertionError("Tushare must not be called before continuous auction minute data exists")

    minutes = fetch_realtime_minutes(
        now=datetime(2026, 7, 17, 9, 15, tzinfo=BEIJING),
        post=fail_post,
    )
    ready = build_realtime_ready(
        minutes,
        now=datetime(2026, 7, 17, 9, 15, tzinfo=BEIJING),
        trade_calendar=_calendar(),
    )

    assert minutes.empty
    assert ready["status"] == "SKIP"
    assert ready["ready"] is False
    assert ready["can_predict_intraday"] is False
    assert ready["market_phase"] == "preopen"
    assert ready["blocking_reason"] == "preopen_no_continuous_auction_minute"


def test_realtime_fetch_uses_rt_min_daily_and_enforces_current_cutoff():
    captured = {}

    def post(url, json, timeout):
        captured.update({"url": url, "json": json, "timeout": timeout})
        fields = ["code", "freq", "time", "open", "close", "high", "low", "vol", "amount"]
        return _Response({
            "code": 0,
            "data": {
                "fields": fields,
                "items": [
                    ["600150.SH", "1MIN", "2026-07-16 15:00:00", 32.9, 33.0, 33.1, 32.8, 100, 3300],
                    ["600150.SH", "1MIN", "2026-07-17 09:30:00", 33.1, 33.2, 33.2, 33.1, 200, 6640],
                    ["600150.SH", "1MIN", "2026-07-17 09:35:00", 33.2, 33.3, 33.4, 33.2, 300, 9990],
                    ["600150.SH", "1MIN", "2026-07-17 09:36:00", 33.3, 33.5, 33.5, 33.3, 400, 13400],
                ],
            },
        })

    minutes = fetch_realtime_minutes(
        token="test-token",
        now=datetime(2026, 7, 17, 9, 35, tzinfo=BEIJING),
        post=post,
    )

    assert captured["json"]["api_name"] == "rt_min_daily"
    assert captured["json"]["params"] == {"ts_code": "600150.SH", "freq": "1MIN"}
    assert minutes["trade_time"].tolist() == [
        "2026-07-17 09:30:00",
        "2026-07-17 09:35:00",
    ]
    assert minutes.iloc[-1]["close"] == 33.3
    assert minutes.iloc[-1]["source"] == "tushare.rt_min_daily"


def test_realtime_ready_is_anchored_to_current_trade_day():
    minutes = _complete_minutes("14:20:00")
    ready = build_realtime_ready(
        minutes,
        now=datetime(2026, 7, 17, 14, 23, tzinfo=BEIJING),
        trade_calendar=_calendar(),
    )

    assert ready["status"] == "PASS"
    assert ready["ready"] is True
    assert ready["trade_date"] == "2026-07-17"
    assert ready["expected_trade_date"] == "2026-07-17"
    assert ready["asof_time"] == "14:20:00"
    assert ready["asof_price"] == 33.25
    assert ready["data_endpoint"] == "rt_min_daily"
    assert ready["coverage_ratio"] >= 0.95
    assert ready["trading_minute_lag"] == 3


def test_realtime_gate_fails_closed_without_trade_calendar():
    ready = build_realtime_ready(
        _complete_minutes("14:20:00"),
        now=datetime(2026, 7, 17, 14, 20, tzinfo=BEIJING),
        trade_calendar=None,
    )

    assert ready["status"] == "FAIL"
    assert ready["ready"] is False
    assert ready["blocking_reason"] == "trade_calendar_unavailable"


def test_same_day_but_stale_minutes_are_rejected():
    ready = build_realtime_ready(
        _complete_minutes("11:30:00"),
        now=datetime(2026, 7, 17, 14, 20, tzinfo=BEIJING),
        trade_calendar=_calendar(),
    )

    assert ready["status"] == "FAIL"
    assert ready["blocking_reason"] == "tushare_realtime_minutes_stale"
    assert ready["trading_minute_lag"] > ready["max_trading_minute_lag"]


def test_sparse_current_minutes_are_rejected_as_incomplete():
    minutes = _complete_minutes("14:20:00").tail(1)
    ready = build_realtime_ready(
        minutes,
        now=datetime(2026, 7, 17, 14, 20, tzinfo=BEIJING),
        trade_calendar=_calendar(),
    )

    assert ready["status"] == "FAIL"
    assert ready["blocking_reason"] == "tushare_realtime_minutes_incomplete"


def test_ready_gate_ignores_minutes_after_current_checkpoint():
    ready = build_realtime_ready(
        _complete_minutes("15:00:00"),
        now=datetime(2026, 7, 17, 9, 35, tzinfo=BEIJING),
        trade_calendar=_calendar(),
    )

    assert ready["status"] == "PASS"
    assert ready["asof_time"] == "09:35:00"
    assert ready["minute_rows_today"] == 6


def test_realtime_fetch_retries_transient_transport_failure(monkeypatch):
    calls = []
    monkeypatch.setattr("cnsv.data.tushare_realtime.time.sleep", lambda value: None)

    def post(*args, **kwargs):
        calls.append(1)
        if len(calls) < 3:
            raise requests.ConnectionError("temporary")
        return _Response({
            "code": 0,
            "data": {
                "fields": ["code", "time", "open", "close", "high", "low", "vol", "amount"],
                "items": [["600150.SH", "2026-07-17 09:35:00", 33.1, 33.2, 33.3, 33.0, 100, 3320]],
            },
        })

    result = fetch_realtime_minutes(
        token="test-token",
        now=datetime(2026, 7, 17, 9, 35, tzinfo=BEIJING),
        post=post,
    )

    assert len(calls) == 3
    assert len(result) == 1


def test_realtime_fetch_rejects_wrong_symbol():
    def post(*args, **kwargs):
        return _Response({
            "code": 0,
            "data": {
                "fields": ["code", "time", "open", "close", "high", "low", "vol", "amount"],
                "items": [["600151.SH", "2026-07-17 09:35:00", 33.1, 33.2, 33.3, 33.0, 100, 3320]],
            },
        })

    with pytest.raises(RuntimeError, match="unexpected symbols"):
        fetch_realtime_minutes(
            token="test-token",
            now=datetime(2026, 7, 17, 9, 35, tzinfo=BEIJING),
            post=post,
        )


def test_current_realtime_rows_replace_same_timestamp_in_history():
    history = pd.DataFrame({
        "trade_time": ["2026-07-16 15:00:00", "2026-07-17 09:35:00"],
        "close": [33.0, 33.1],
    })
    current = pd.DataFrame({
        "trade_time": ["2026-07-17 09:35:00"],
        "close": [33.3],
    })

    merged = merge_intraday_history(history, current)

    assert len(merged) == 2
    assert merged.iloc[-1]["close"] == 33.3
