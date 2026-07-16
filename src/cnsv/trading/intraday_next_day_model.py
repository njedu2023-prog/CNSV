from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import brier_score_loss, roc_auc_score

from cnsv.trading.next_day_model import build_feature_frame as build_daily_feature_frame

MODEL_ID = "T1_INTRADAY_20M_HGB_V3"
MODEL_VERSION = "2026-07-17"
MIN_TRAIN_ROWS = 500
TRAIN_WINDOW_ROWS = 2000
VALIDATION_DAYS = 60
HIGH_CONFIDENCE_THRESHOLD = 0.55

CHECKPOINT_TIMES = (
    "09:35:00", "09:55:00", "10:15:00", "10:35:00", "10:55:00", "11:15:00",
    "11:30:00", "13:00:00", "13:20:00", "13:40:00", "14:00:00", "14:20:00",
    "14:40:00", "15:00:00",
)

FLOW_SOURCE_COLUMNS = (
    "net_mf_ratio",
    "main_force_ratio",
    "net_mf_ratio_5",
    "net_mf_ratio_20",
    "main_force_ratio_5",
    "main_force_ratio_20",
)

PRICE_FEATURE_COLUMNS = (
    "ret_1",
    "ret_2",
    "ret_5",
    "ret_20",
    "gap",
    "intraday",
    "range",
    "close_position",
    "rsi_14",
    "volatility_5",
    "volatility_20",
    "close_ma_5",
    "close_ma_20",
    "close_ma_60",
    "volume_ratio_20",
    "weekday",
    "ret_sign",
    "trend_5_20",
    "vol_regime",
)

FEATURE_COLUMNS = (
    *PRICE_FEATURE_COLUMNS,
    *(f"{column}_lag1" for column in FLOW_SOURCE_COLUMNS),
    "flow_sign_lag1",
)


def fit_intraday_next_day_model(reports: dict[str, Any]) -> dict[str, Any]:
    ready = reports.get("intraday_realtime_ready")
    minutes = reports.get("intraday_minute_history")
    daily = reports.get("daily_price_history")
    moneyflow = reports.get("moneyflow_history")
    if not isinstance(ready, dict) or not ready.get("ready"):
        return unavailable_model("realtime_intraday_not_ready")
    if ready.get("can_predict_intraday") is False:
        return unavailable_model("realtime_intraday_prediction_not_allowed")
    if not isinstance(minutes, pd.DataFrame) or minutes.empty:
        return unavailable_model("intraday_minute_history_unavailable")
    if not isinstance(daily, pd.DataFrame) or daily.empty:
        return unavailable_model("daily_price_history_unavailable")
    if not isinstance(moneyflow, pd.DataFrame) or moneyflow.empty:
        return unavailable_model("moneyflow_history_unavailable")

    current_date = _date_text(ready.get("trade_date"))
    current_asof = _time_text(ready.get("asof_time"))
    if not current_date or not current_asof:
        return unavailable_model("realtime_trade_date_or_asof_missing")
    try:
        base = build_realtime_daily_feature_frame(daily, moneyflow)
        pseudo = build_intraday_feature_frame(
            minutes,
            daily,
            current_date=current_date,
            current_asof=current_asof,
            moneyflow_history=moneyflow,
        )
    except (KeyError, TypeError, ValueError) as exc:
        return unavailable_model(f"invalid_realtime_history:{exc}")
    if base.empty or pseudo.empty:
        return unavailable_model("realtime_feature_frame_empty")

    current = pseudo[
        (pseudo["trade_date"] == current_date) & (pseudo["asof_time"] == current_asof)
    ].tail(1)
    if current.empty:
        return unavailable_model("current_intraday_snapshot_missing")
    labelled = pseudo[pseudo["target"].notna()].sort_values("trade_date").reset_index(drop=True)
    validation_dates = sorted(labelled["trade_date"].unique())[-VALIDATION_DAYS:]
    validation_rows: list[dict[str, Any]] = []
    for validation_date in validation_dates:
        test = labelled[labelled["trade_date"] == validation_date].tail(1)
        train = _available_training_rows(base, validation_date)
        if len(train) < MIN_TRAIN_ROWS or test.empty:
            continue
        candidate = _fit_predict(train, test)
        baseline = np.full(len(test), float(train["target"].mean()))
        validation_rows.append({
            **test.iloc[0].to_dict(),
            "candidate_probability": float(candidate[0]),
            "baseline_probability": float(baseline[0]),
        })
    validation = pd.DataFrame(validation_rows)
    if len(validation) < min(30, VALIDATION_DAYS):
        return unavailable_model(f"walk_forward_validation_unavailable:{len(validation)}")

    target = validation["target"].astype(int).to_numpy()
    candidate_probability = validation["candidate_probability"].to_numpy(dtype=float)
    baseline_probability = validation["baseline_probability"].to_numpy(dtype=float)
    candidate_metrics = _metric_summary(target, candidate_probability)
    baseline_metrics = _metric_summary(target, baseline_probability)
    holdout_start = len(validation) // 2
    candidate_holdout = _metric_summary(target[holdout_start:], candidate_probability[holdout_start:])
    baseline_holdout = _metric_summary(target[holdout_start:], baseline_probability[holdout_start:])
    candidate_accepted = bool(
        candidate_metrics["directional_accuracy"] > baseline_metrics["directional_accuracy"]
        and candidate_metrics["brier"] < baseline_metrics["brier"]
        and candidate_holdout["directional_accuracy"] >= baseline_holdout["directional_accuracy"]
        and candidate_holdout["brier"] <= baseline_holdout["brier"]
    )

    final_train = _available_training_rows(base, current_date)
    if len(final_train) < MIN_TRAIN_ROWS:
        return unavailable_model(f"insufficient_training_rows:{len(final_train)}")
    candidate_prob_up = float(_fit_predict(final_train, current)[0])
    baseline_prob_up = float(final_train["target"].mean())
    prob_up = candidate_prob_up if candidate_accepted else baseline_prob_up
    prob_up = float(np.clip(prob_up, 0.05, 0.95))
    prob_down = 1.0 - prob_up
    active_probability = candidate_probability if candidate_accepted else baseline_probability
    active_metrics = candidate_metrics if candidate_accepted else baseline_metrics
    validation_summary = _validation_summary(
        validation,
        target,
        active_probability,
        active_metrics,
        candidate_metrics,
        baseline_metrics,
        candidate_accepted,
    )
    distribution = _return_distribution(validation, active_probability, prob_up, labelled)
    latest = current.iloc[0]
    return {
        "model_ready": True,
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
        "primary_model": (
            "20-minute pseudo-daily HGB using 2000 historical trading days"
            if candidate_accepted else "expanding historical next-day direction baseline"
        ),
        "predicted_direction": "UP" if prob_up >= 0.5 else "DOWN",
        "prob_up_1d": prob_up,
        "prob_down_1d": prob_down,
        "prob_flat_1d": 0.0,
        "direction_confidence": max(prob_up, prob_down),
        "raw_prob_up_1d": candidate_prob_up,
        "baseline_prob_up_1d": baseline_prob_up,
        "calibration_slope": 1.0,
        "ensemble_dispersion": abs(candidate_prob_up - baseline_prob_up),
        "fallback_used": not candidate_accepted,
        "fallback_reason": None if candidate_accepted else "walk_forward_candidate_did_not_beat_recent_baseline",
        "candidate_accepted": candidate_accepted,
        "latest_data_trade_date": str(latest["trade_date"]),
        "asof_time": str(latest["asof_time"]),
        "asof_price": float(latest["asof_price"]),
        "asof_amount": float(latest["asof_amount"]),
        "asof_pct_chg": float(latest["asof_pct_chg"]),
        "prediction_basis": "next_trading_day_close_vs_current_trade_day_close",
        "direction_label_anchor": "current_trade_day_official_close",
        "feature_price_anchor": "latest_valid_intraday_trade_at_checkpoint",
        "uses_intraday_snapshot": True,
        "refresh_interval_minutes": 20,
        "training": {
            "start_date": str(final_train.iloc[0]["trade_date"]),
            "end_date": str(final_train.iloc[-1]["trade_date"]),
            "sample_size": int(len(final_train)),
            "trading_day_count": int(final_train["trade_date"].nunique()),
            "feature_count": len(FEATURE_COLUMNS),
            "checkpoint_time": current_asof,
            "target": "next_trading_day_close_vs_current_trade_day_close",
            "current_day_moneyflow_policy": "T-1 lag only",
        },
        "validation": validation_summary,
        "model_return_distribution": distribution,
        "inputs": {
            "realtime_source": ready.get("data_source", "unknown"),
            "realtime_endpoint": ready.get("data_endpoint", "unknown"),
            "minute_rows": int(len(minutes)),
            "daily_rows": int(len(daily)),
            "moneyflow_rows": int(len(moneyflow)),
            "historical_intraday_days": int(pseudo["trade_date"].nunique()),
            "feature_columns": list(FEATURE_COLUMNS),
            "future_data_guard": (
                "each validation date uses only earlier labelled dates; current-day price features "
                "use minute bars no later than reported asof_time"
            ),
        },
    }


def unavailable_model(reason: str) -> dict[str, Any]:
    return {
        "model_ready": False,
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
        "primary_model": "20-minute pseudo-daily HGB next-day model",
        "predicted_direction": None,
        "prob_up_1d": 0.5,
        "prob_down_1d": 0.5,
        "prob_flat_1d": 0.0,
        "direction_confidence": 0.5,
        "raw_prob_up_1d": 0.5,
        "calibration_slope": 0.0,
        "ensemble_dispersion": None,
        "fallback_used": True,
        "fallback_reason": reason,
        "latest_data_trade_date": None,
        "prediction_basis": "next_trading_day_close_vs_current_trade_day_close",
        "direction_label_anchor": "current_trade_day_official_close",
        "feature_price_anchor": "latest_valid_intraday_trade_at_checkpoint",
        "uses_intraday_snapshot": False,
        "training": {},
        "validation": {},
        "model_return_distribution": {},
        "inputs": {},
    }


def build_realtime_daily_feature_frame(daily: pd.DataFrame, moneyflow: pd.DataFrame) -> pd.DataFrame:
    frame = build_daily_feature_frame(daily, moneyflow).copy()
    if frame.empty:
        return frame
    for column in FLOW_SOURCE_COLUMNS:
        frame[f"{column}_lag1"] = frame[column].shift(1)
    frame["flow_sign_lag1"] = frame["flow_sign"].shift(1)
    return frame.replace([np.inf, -np.inf], np.nan)


def build_intraday_feature_frame(
    minute_history: pd.DataFrame,
    daily_history: pd.DataFrame,
    current_date: str | None = None,
    current_asof: str | None = None,
    moneyflow_history: pd.DataFrame | None = None,
) -> pd.DataFrame:
    required_minutes = {"trade_time", "open", "high", "low", "close"}
    missing = sorted(required_minutes.difference(minute_history.columns))
    if missing:
        raise KeyError(",".join(missing))
    daily = _normalise_daily(daily_history)
    if daily.empty:
        raise ValueError("daily_history_empty")
    base = build_realtime_daily_feature_frame(daily, moneyflow_history)
    minute = minute_history.copy()
    minute["timestamp"] = pd.to_datetime(minute["trade_time"], errors="coerce")
    minute = minute.dropna(subset=["timestamp"]).copy()
    minute["trade_date"] = minute["timestamp"].dt.strftime("%Y-%m-%d")
    minute["clock"] = minute["timestamp"].dt.strftime("%H:%M:%S")
    minute = minute[
        ((minute["clock"] >= "09:30:00") & (minute["clock"] <= "11:30:00"))
        | ((minute["clock"] >= "13:00:00") & (minute["clock"] <= "15:00:00"))
    ].copy()
    for column in ("open", "high", "low", "close", "volume", "vol", "amount"):
        if column in minute:
            minute[column] = pd.to_numeric(minute[column], errors="coerce")
    if "volume" not in minute:
        minute["volume"] = minute.get("vol", 0.0)
    if "amount" not in minute:
        minute["amount"] = minute["close"] * minute["volume"]
    minute = minute.sort_values("timestamp").drop_duplicates(["trade_date", "timestamp"], keep="last")

    requested_asof = current_asof or _latest_asof(minute, current_date)
    if not requested_asof:
        return pd.DataFrame()
    close_map = daily.set_index("trade_date")["close"]
    dates = daily["trade_date"].tolist()
    next_date_map = {dates[index]: dates[index + 1] for index in range(len(dates) - 1)}
    rows: list[dict[str, Any]] = []
    for trade_date, day in minute.groupby("trade_date", sort=True):
        window = day[day["clock"] <= requested_asof].sort_values("timestamp")
        if window.empty or str(window.iloc[-1]["clock"]) < _minus_minutes(requested_asof, 5):
            continue
        previous = daily[daily["trade_date"] < trade_date]
        if len(previous) < 60:
            continue
        row = _pseudo_daily_feature_row(window, previous, base, trade_date, requested_asof)
        next_date = next_date_map.get(trade_date)
        current_close = close_map.get(trade_date)
        next_close = close_map.get(next_date) if next_date else None
        if pd.notna(current_close) and pd.notna(next_close) and float(current_close) != 0:
            target_return = float(next_close) / float(current_close) - 1.0
        else:
            target_return = np.nan
        row.update({
            "next_trade_date": next_date,
            "target_return": target_return,
            "target": 1.0 if target_return > 0 else 0.0 if target_return < 0 else np.nan,
        })
        rows.append(row)
    return pd.DataFrame(rows).replace([np.inf, -np.inf], np.nan)


def _pseudo_daily_feature_row(
    window: pd.DataFrame,
    previous: pd.DataFrame,
    base: pd.DataFrame,
    trade_date: str,
    asof_time: str,
) -> dict[str, Any]:
    current_open = float(pd.to_numeric(window.iloc[0]["open"], errors="coerce"))
    current_high = float(pd.to_numeric(window["high"], errors="coerce").max())
    current_low = float(pd.to_numeric(window["low"], errors="coerce").min())
    asof_price = float(pd.to_numeric(window.iloc[-1]["close"], errors="coerce"))
    previous_close = float(previous.iloc[-1]["close"])
    current_return = float(np.clip(asof_price / previous_close - 1.0, -0.25, 0.25))
    previous_returns = _daily_returns(previous)
    combined_returns = pd.concat([previous_returns, pd.Series([current_return])], ignore_index=True)
    log_returns = np.log1p(combined_returns.clip(lower=-0.95))

    row: dict[str, Any] = {
        "trade_date": trade_date,
        "asof_time": asof_time,
        "last_observed_time": str(window.iloc[-1]["clock"]),
        "asof_price": asof_price,
        # Tushare minute amount is yuan while the daily contract stores thousand yuan.
        "asof_amount": float(pd.to_numeric(window["amount"], errors="coerce").fillna(0.0).sum()) / 1000.0,
        "asof_pct_chg": current_return * 100.0,
        "ret_1": current_return,
        "gap": float(np.clip(current_open / previous_close - 1.0, -0.2, 0.2)),
        "intraday": float(np.clip(asof_price / current_open - 1.0, -0.2, 0.2)),
        "range": float(np.clip((current_high - current_low) / previous_close, 0.0, 0.3)),
        "close_position": (
            (asof_price - current_low) / (current_high - current_low)
            if current_high != current_low else 0.5
        ),
    }
    for window_size in (2, 5, 20):
        row[f"ret_{window_size}"] = float(
            np.clip(np.expm1(log_returns.tail(window_size).sum()), -0.6, 0.6)
        )
    gains = combined_returns.clip(lower=0).tail(14)
    losses = (-combined_returns.clip(upper=0)).tail(14)
    gain = float(gains.mean())
    loss = float(losses.mean())
    row["rsi_14"] = gain / (gain + loss) if gain + loss else 0.5
    for window_size in (5, 20):
        row[f"volatility_{window_size}"] = float(
            np.clip(combined_returns.tail(window_size).std(), 0.0, 0.2)
        )
    previous_closes = previous["close"].astype(float)
    for window_size in (5, 20, 60):
        closes = pd.concat([previous_closes.tail(window_size - 1), pd.Series([asof_price])], ignore_index=True)
        row[f"close_ma_{window_size}"] = float(
            np.clip(asof_price / closes.mean() - 1.0, -0.5, 0.5)
        )
    progress = max(_session_progress(asof_time), 0.05)
    current_volume = float(pd.to_numeric(window["volume"], errors="coerce").fillna(0.0).sum()) / 100.0
    full_day_volume_estimate = current_volume / progress
    volume_window = pd.concat(
        [previous["vol"].astype(float).tail(19), pd.Series([full_day_volume_estimate])],
        ignore_index=True,
    )
    row["volume_ratio_20"] = float(
        np.clip(full_day_volume_estimate / volume_window.mean(), 0.0, 8.0)
    ) if volume_window.mean() else np.nan
    row["weekday"] = pd.Timestamp(trade_date).weekday()
    row["ret_sign"] = float(np.sign(current_return))
    row["trend_5_20"] = row["close_ma_5"] - row["close_ma_20"]
    row["vol_regime"] = float(
        np.clip(row["volatility_5"] / row["volatility_20"], 0.0, 5.0)
    ) if row["volatility_20"] else np.nan

    previous_date = str(previous.iloc[-1]["trade_date"])
    previous_features = base[base["trade_date"] == previous_date].tail(1)
    for column in FLOW_SOURCE_COLUMNS:
        row[f"{column}_lag1"] = (
            float(previous_features.iloc[0][column])
            if not previous_features.empty and pd.notna(previous_features.iloc[0][column]) else np.nan
        )
    row["flow_sign_lag1"] = (
        float(previous_features.iloc[0]["flow_sign"])
        if not previous_features.empty and pd.notna(previous_features.iloc[0]["flow_sign"]) else np.nan
    )
    return row


def _normalise_daily(daily: pd.DataFrame) -> pd.DataFrame:
    required = {"trade_date", "open", "high", "low", "close", "pre_close", "vol", "amount"}
    missing = sorted(required.difference(daily.columns))
    if missing:
        raise KeyError("daily:" + ",".join(missing))
    frame = daily.copy()
    frame["trade_date"] = frame["trade_date"].map(_date_text)
    frame = frame.dropna(subset=["trade_date"]).sort_values("trade_date").drop_duplicates("trade_date", keep="last")
    for column in ("open", "high", "low", "close", "pre_close", "vol", "amount", "pct_chg"):
        if column not in frame:
            frame[column] = np.nan
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame.reset_index(drop=True)


def _daily_returns(frame: pd.DataFrame) -> pd.Series:
    returns = pd.to_numeric(frame.get("pct_chg"), errors="coerce") / 100.0
    fallback = frame["close"] / frame["pre_close"].replace(0.0, np.nan) - 1.0
    return returns.where(returns.notna(), fallback).clip(-0.25, 0.25).reset_index(drop=True)


def _available_training_rows(base: pd.DataFrame, prediction_date: str) -> pd.DataFrame:
    previous_dates = sorted(base.loc[base["trade_date"] < prediction_date, "trade_date"].unique())
    if not previous_dates:
        return pd.DataFrame(columns=base.columns)
    previous_date = previous_dates[-1]
    # Before T closes, the label attached to T-1 is not known. Excluding T-1 keeps every
    # intraday checkpoint on the same strict information set, including the close checkpoint.
    return base[(base["trade_date"] < previous_date) & base["target"].notna()].tail(TRAIN_WINDOW_ROWS)


def _fit_predict(train: pd.DataFrame, test: pd.DataFrame) -> np.ndarray:
    target = train["target"].astype(int)
    if target.nunique() < 2:
        return np.full(len(test), float(target.mean()))
    model = HistGradientBoostingClassifier(
        max_iter=80,
        learning_rate=0.03,
        max_leaf_nodes=7,
        max_depth=2,
        min_samples_leaf=50,
        l2_regularization=5.0,
        random_state=7,
    )
    model.fit(train.loc[:, FEATURE_COLUMNS], target)
    return np.clip(model.predict_proba(test.loc[:, FEATURE_COLUMNS])[:, 1], 0.05, 0.95)


def _metric_summary(target: np.ndarray, probability: np.ndarray) -> dict[str, float | None]:
    predicted = probability >= 0.5
    try:
        auc = float(roc_auc_score(target, probability))
    except ValueError:
        auc = None
    return {
        "sample_size": int(len(target)),
        "directional_accuracy": float(np.mean(predicted == target)),
        "brier": float(brier_score_loss(target, probability)),
        "roc_auc": auc,
    }


def _validation_summary(
    validation: pd.DataFrame,
    target: np.ndarray,
    probability: np.ndarray,
    active: dict[str, Any],
    candidate: dict[str, Any],
    baseline: dict[str, Any],
    accepted: bool,
) -> dict[str, Any]:
    correct = (probability >= 0.5) == target
    ci_low, ci_high = _wilson_interval(int(correct.sum()), len(correct))
    high = (probability >= HIGH_CONFIDENCE_THRESHOLD) | (probability <= 1.0 - HIGH_CONFIDENCE_THRESHOLD)
    split = len(validation) // 2
    candidate_probability = validation["candidate_probability"].to_numpy(dtype=float)
    baseline_probability = validation["baseline_probability"].to_numpy(dtype=float)
    return {
        "model": MODEL_ID,
        "horizon": "next_trading_day_close_vs_current_trade_day_close",
        "method": "strict_expanding_walk_forward_with_recent_holdout_gate",
        "sample_size": int(len(validation)),
        "trading_day_count": int(validation["trade_date"].nunique()),
        "start_date": str(validation["trade_date"].min()),
        "end_date": str(validation["trade_date"].max()),
        "checkpoint_time": str(validation.iloc[-1]["asof_time"]),
        "directional_accuracy": active["directional_accuracy"],
        "accuracy_ci_95_low": ci_low,
        "accuracy_ci_95_high": ci_high,
        "brier_raw": candidate["brier"],
        "brier_calibrated": active["brier"],
        "roc_auc": active["roc_auc"],
        "actual_up_rate": float(target.mean()),
        "high_confidence_threshold": HIGH_CONFIDENCE_THRESHOLD,
        "high_confidence_sample_size": int(high.sum()),
        "high_confidence_coverage": float(high.mean()),
        "high_confidence_accuracy": float(correct[high].mean()) if high.any() else None,
        "candidate_accepted": accepted,
        "candidate_directional_accuracy": candidate["directional_accuracy"],
        "candidate_brier": candidate["brier"],
        "baseline_directional_accuracy": baseline["directional_accuracy"],
        "baseline_brier": baseline["brier"],
        "development": _metric_summary(target[:split], candidate_probability[:split]),
        "recent_holdout": _metric_summary(target[split:], candidate_probability[split:]),
        "recent_holdout_baseline": _metric_summary(target[split:], baseline_probability[split:]),
        "refit_interval_days": 1,
        "leakage_guard": (
            "validation T uses labelled daily rows through T-2 and minute bars through the checkpoint only"
        ),
    }


def _return_distribution(
    validation: pd.DataFrame,
    probability: np.ndarray,
    current_probability: float,
    fallback: pd.DataFrame,
) -> dict[str, Any]:
    same_direction = (probability >= 0.5) == (current_probability >= 0.5)
    selected = validation.loc[same_direction, "target_return"].dropna().to_numpy(dtype=float)
    source = "walk_forward_same_direction"
    if len(selected) < 20:
        selected = fallback["target_return"].dropna().to_numpy(dtype=float)
        source = "historical_next_day_empirical_fallback"
    if len(selected) == 0:
        selected = np.array([-0.01, 0.0, 0.01])
        source = "neutral_fallback"
    bins = {
        "gt_5pct": float(np.mean(selected > 0.05)),
        "plus_2_to_5pct": float(np.mean((selected > 0.02) & (selected <= 0.05))),
        "zero_to_plus_2pct": float(np.mean((selected >= 0.0) & (selected <= 0.02))),
        "zero_to_minus_2pct": float(np.mean((selected < 0.0) & (selected >= -0.02))),
        "minus_2_to_5pct": float(np.mean((selected < -0.02) & (selected >= -0.05))),
        "lt_minus_5pct": float(np.mean(selected < -0.05)),
    }
    total = sum(bins.values()) or 1.0
    return {
        "return_bins_1d": {key: value / total for key, value in bins.items()},
        "expected_return_1d": float(np.mean(selected)),
        "median_return_1d": float(np.median(selected)),
        "p10_return_1d": float(np.quantile(selected, 0.10)),
        "p90_return_1d": float(np.quantile(selected, 0.90)),
        "distribution_source": f"{MODEL_ID}:{source}",
        "sample_size": int(len(selected)),
    }


def _latest_asof(minutes: pd.DataFrame, current_date: str | None) -> str:
    frame = minutes
    if current_date:
        current = frame[frame["trade_date"] == current_date]
        if not current.empty:
            frame = current
    return str(frame["clock"].max()) if not frame.empty else ""


def _session_progress(value: str) -> float:
    hour, minute, _ = [int(part) for part in value.split(":")]
    clock = hour * 60 + minute
    elapsed = clock - (9 * 60 + 30) if clock <= 11 * 60 + 30 else 120 + clock - 13 * 60
    return float(np.clip(elapsed / 240.0, 0.0, 1.0))


def _minus_minutes(value: str, minutes: int) -> str:
    hour, minute, second = [int(part) for part in value.split(":")]
    total = hour * 60 + minute - minutes
    return f"{total // 60:02d}:{total % 60:02d}:{second:02d}"


def _time_text(value: Any) -> str:
    text = str(value or "")
    return text[-8:] if len(text) >= 8 else ""


def _date_text(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = str(value)[:10]
    if len(text) == 8 and text.isdigit():
        return f"{text[:4]}-{text[4:6]}-{text[6:8]}"
    try:
        return pd.Timestamp(value).date().isoformat()
    except (TypeError, ValueError):
        return None


def _wilson_interval(successes: int, sample_size: int) -> tuple[float, float]:
    if sample_size <= 0:
        return 0.0, 0.0
    z = 1.959963984540054
    rate = successes / sample_size
    denominator = 1.0 + z * z / sample_size
    centre = (rate + z * z / (2.0 * sample_size)) / denominator
    margin = z * math.sqrt((rate * (1.0 - rate) + z * z / (4.0 * sample_size)) / sample_size) / denominator
    return max(0.0, centre - margin), min(1.0, centre + margin)
