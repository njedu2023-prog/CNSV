from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd

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
    minutes = pd.DataFrame({
        "trade_time": ["2026-07-17 14:20:00"],
        "close": [33.25],
    })
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
