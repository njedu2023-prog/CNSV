from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from cnsv.utils.io import ensure_parent

LIVE_STATS_START_DATE = "2026-06-21"
VERIFIABLE_DIRECTIONS = {"UP", "DOWN", "FLAT"}


def default_live_registry_entry(payload: dict[str, Any], signal_date: str | None = None) -> dict[str, Any]:
    timeline = payload.get("decision_timeline") or {}
    signal_day = signal_date or timeline.get("signal_date") or _today()
    verify_day = timeline.get("verify_date") or _plus_one_day(signal_day)
    market = payload.get("market_snapshot") or {}
    data_trade_date = timeline.get("data_trade_date") or market.get("latest_trade_date")
    return {
        "trade_date": timeline.get("prediction_date") or signal_day,
        "data_trade_date": data_trade_date,
        "signal_date": signal_day,
        "verify_date": verify_day,
        "predicted_direction": predicted_direction(payload),
        "actual_direction": None,
        "is_correct": None,
        "close_t": market.get("latest_close"),
        "close_t1": None,
        "return_1d": None,
    }


def update_live_stats_registry(payload: dict[str, Any], path: str | Path, reports: dict[str, Any]) -> list[dict[str, Any]]:
    target = Path(path)
    registry = load_live_stats_registry(target)
    registry = _backfill_verified_archive_entries(registry, target, reports)
    registry = [_try_verify_entry(item, reports) for item in registry]

    signal_date = (payload.get("decision_timeline") or {}).get("signal_date") or _today()
    current_direction = predicted_direction(payload)
    if signal_date >= LIVE_STATS_START_DATE and current_direction in VERIFIABLE_DIRECTIONS and _has_base_close(payload):
        replacement = default_live_registry_entry(payload, signal_date)
        found = False
        updated: list[dict[str, Any]] = []
        for item in registry:
            if item.get("signal_date") == signal_date:
                found = True
                updated.append(item if item.get("is_correct") is not None else {**item, **replacement})
            else:
                updated.append(item)
        registry = updated
        if not found:
            registry.append(replacement)

    registry = [
        item
        for item in registry
        if str(item.get("signal_date", "")) >= LIVE_STATS_START_DATE
        and item.get("predicted_direction") in VERIFIABLE_DIRECTIONS
        and item.get("close_t") is not None
        and _has_auditable_base_date(item)
    ]
    registry.sort(key=lambda item: str(item.get("signal_date", "")))
    write_live_stats_registry(registry, target)
    return registry


def _backfill_verified_archive_entries(
    registry: list[dict[str, Any]], target: Path, reports: dict[str, Any]
) -> list[dict[str, Any]]:
    latest_date, _ = _latest_close(reports)
    archive_dir = _archive_dir_for_registry(target)
    if not latest_date or not archive_dir.exists():
        return registry

    existing_signal_dates = {str(item.get("signal_date", "")) for item in registry}
    out = list(registry)
    for archive_path in sorted(archive_dir.glob("*_trading_decision_report.md")):
        entry = _archived_markdown_entry(archive_path, latest_date)
        if not entry:
            continue
        signal_date = str(entry.get("signal_date", ""))
        if signal_date in existing_signal_dates:
            continue
        existing_signal_dates.add(signal_date)
        out.append(entry)
    return out


def load_live_stats_registry(path: str | Path) -> list[dict[str, Any]]:
    target = Path(path)
    if not target.exists():
        return []
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def write_live_stats_registry(registry: list[dict[str, Any]], path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(registry, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return target


def build_model_performance(historical_validation: dict[str, Any], registry: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    standard = ((historical_validation.get("baseline_directional_accuracy") or {}).get("standard") or {})
    historical_accuracy = standard.get("directional_accuracy")
    verified = [
        item
        for item in (registry or [])
        if str(item.get("signal_date", "")) >= LIVE_STATS_START_DATE and item.get("is_correct") is not None
    ]
    correct_count = sum(1 for item in verified if item.get("is_correct") is True)
    wrong_count = sum(1 for item in verified if item.get("is_correct") is False)
    sample_count = correct_count + wrong_count
    return {
        "historical_stats": {
            "name": "历史统计线",
            "direction_accuracy": historical_accuracy,
            "sample_count": standard.get("sample_size"),
            "description": "包含历史验证样本、walk-forward、purged walk-forward 等历史统计结果。",
        },
        "live_stats": {
            "name": "实盘统计线",
            "start_date": LIVE_STATS_START_DATE,
            "direction_accuracy": (correct_count / sample_count) if sample_count else None,
            "correct_count": correct_count,
            "wrong_count": wrong_count,
            "sample_count": sample_count,
            "description": "从 2026-06-21 起，只统计 V3.0 正式运行后的真实方向命中情况。",
        },
    }


def predicted_direction(payload: dict[str, Any]) -> str | None:
    signal = ((payload.get("decision") or {}).get("signal") or "").upper()
    if signal in {"BUY", "STRONG_BUY"}:
        return "UP"
    if signal in {"SELL", "STRONG_SELL", "REDUCE"}:
        return "DOWN"
    if signal in {"HOLD", "WATCH"}:
        return "FLAT"
    return None


def _try_verify_entry(item: dict[str, Any], reports: dict[str, Any]) -> dict[str, Any]:
    if item.get("is_correct") is not None:
        return item
    verify_date = item.get("verify_date")
    latest_date, latest_close = _latest_close(reports)
    if not verify_date or verify_date != latest_date or latest_close is None:
        return item
    close_t = item.get("close_t")
    if close_t is None:
        return item
    ret = (float(latest_close) / float(close_t)) - 1.0
    actual = "UP" if ret > 0 else "DOWN" if ret < 0 else "FLAT"
    out = dict(item)
    out["close_t1"] = float(latest_close)
    out["return_1d"] = ret
    out["actual_direction"] = actual
    out["is_correct"] = actual == item.get("predicted_direction")
    return out


def _latest_close(reports: dict[str, Any]) -> tuple[str | None, float | None]:
    feature_report = reports.get("feature_report") or {}
    features = feature_report.get("features") or {}
    price_volume = features.get("price_volume") or {}
    date_value = (
        price_volume.get("latest_trade_date")
        or (feature_report.get("meta") or {}).get("latest_trade_date")
        or ((reports.get("data_report") or {}).get("data_manifest") or {}).get("latest_trade_date")
    )
    close_value = price_volume.get("latest_close")
    try:
        close = float(close_value)
    except (TypeError, ValueError):
        close = None
    return date_value, close


def _has_base_close(payload: dict[str, Any]) -> bool:
    market = payload.get("market_snapshot") or {}
    try:
        float(market.get("latest_close"))
    except (TypeError, ValueError):
        return False
    return True


def _has_auditable_base_date(item: dict[str, Any]) -> bool:
    if item.get("is_correct") is not None:
        return True
    return bool(item.get("data_trade_date"))


def _archive_dir_for_registry(target: Path) -> Path:
    try:
        root = target.parent.parent.parent
    except IndexError:
        return Path("reports/archive")
    return root / "reports/archive"


def _archived_markdown_entry(path: Path, latest_date: str) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    signal_date = _md_value(text, "信号生成日")
    prediction_date = _md_value(text, "预测日")
    verify_date = prediction_date or _md_value(text, "验证日")
    if not signal_date or signal_date < LIVE_STATS_START_DATE or verify_date != latest_date:
        return None

    signal = _md_value(text, "信号")
    close_t = _parse_float(_md_value(text, "收盘价"))
    direction = predicted_direction({"decision": {"signal": (signal or "").split("/")[0].strip()}})
    if direction not in VERIFIABLE_DIRECTIONS or close_t is None:
        return None
    return {
        "trade_date": prediction_date or signal_date,
        "data_trade_date": _md_value(text, "数据交易日") or _md_value(text, "交易日"),
        "signal_date": signal_date,
        "verify_date": verify_date,
        "predicted_direction": direction,
        "actual_direction": None,
        "is_correct": None,
        "close_t": close_t,
        "close_t1": None,
        "return_1d": None,
        "source": "reports_archive",
    }


def _md_value(text: str, label: str) -> str | None:
    prefix = f"- {label}:"
    for line in text.splitlines():
        if line.startswith(prefix):
            value = line[len(prefix) :].strip()
            return value or None
    return None


def _parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value.replace(",", "").replace("%", ""))
    except ValueError:
        return None


def _today() -> str:
    return date.today().isoformat()


def _plus_one_day(value: str) -> str:
    try:
        day = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return value
    return (day + timedelta(days=1)).isoformat()
