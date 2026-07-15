from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import brier_score_loss, roc_auc_score

MODEL_ID = "T1_HGB_ENSEMBLE_V1"
MODEL_VERSION = "2026-07-14"
MIN_TRAIN_ROWS = 500
VALIDATION_MAX_ROWS = 2200
REFIT_INTERVAL_DAYS = 40
HIGH_CONFIDENCE_THRESHOLD = 0.51

MONEYFLOW_COLUMNS = (
    "buy_lg_amount",
    "sell_lg_amount",
    "buy_elg_amount",
    "sell_elg_amount",
    "net_mf_amount",
)

FEATURE_COLUMNS = (
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
    "net_mf_ratio",
    "main_force_ratio",
    "net_mf_ratio_5",
    "net_mf_ratio_20",
    "main_force_ratio_5",
    "main_force_ratio_20",
    "weekday",
    "ret_sign",
    "flow_sign",
    "trend_5_20",
    "vol_regime",
)


@dataclass(frozen=True)
class ModelSpec:
    max_iter: int
    learning_rate: float
    max_leaf_nodes: int
    max_depth: int
    min_samples_leaf: int
    l2_regularization: float
    half_life: int | None = None


MODEL_SPECS = (
    ModelSpec(80, 0.04, 7, 2, 50, 4.0),
    ModelSpec(80, 0.04, 12, 3, 40, 4.0),
    ModelSpec(80, 0.04, 12, 3, 40, 4.0, half_life=1000),
    ModelSpec(70, 0.04, 12, 3, 70, 5.0),
)


def fit_next_day_model(reports: dict[str, Any]) -> dict[str, Any]:
    daily = reports.get("daily_price_history")
    moneyflow = reports.get("moneyflow_history")
    if moneyflow is None or not isinstance(moneyflow, pd.DataFrame) or moneyflow.empty:
        return unavailable_model("moneyflow_history_unavailable")
    daily_latest = _latest_input_date(daily)
    moneyflow_latest = _latest_input_date(moneyflow)
    if daily_latest and moneyflow_latest and daily_latest != moneyflow_latest:
        return unavailable_model(f"history_date_mismatch:daily={daily_latest},moneyflow={moneyflow_latest}")
    try:
        frame = build_feature_frame(daily, moneyflow)
    except (KeyError, TypeError, ValueError) as exc:
        return unavailable_model(f"invalid_history:{exc}")
    if frame.empty:
        return unavailable_model("daily_price_history_unavailable")

    labelled = frame[frame["target"].notna()].reset_index(drop=True)
    if len(labelled) < MIN_TRAIN_ROWS:
        return unavailable_model(f"insufficient_training_rows:{len(labelled)}")

    validation_start = max(MIN_TRAIN_ROWS, len(labelled) - VALIDATION_MAX_ROWS)
    validation_probabilities = np.full(len(labelled), np.nan, dtype=float)
    validation_dispersion = np.full(len(labelled), np.nan, dtype=float)
    for begin in range(validation_start, len(labelled), REFIT_INTERVAL_DAYS):
        end = min(begin + REFIT_INTERVAL_DAYS, len(labelled))
        probabilities, dispersion = _fit_predict_ensemble(
            labelled.iloc[:begin],
            labelled.iloc[begin:end],
        )
        validation_probabilities[begin:end] = probabilities
        validation_dispersion[begin:end] = dispersion

    validation_mask = np.isfinite(validation_probabilities)
    validation = labelled.loc[validation_mask].copy()
    raw_oos_probability = validation_probabilities[validation_mask]
    calibration_slope = _calibration_slope(raw_oos_probability, validation["target"].to_numpy(dtype=int))
    calibrated_oos_probability = _calibrate(raw_oos_probability, calibration_slope)

    latest = frame.iloc[[-1]]
    raw_probabilities, current_dispersion = _fit_predict_ensemble(labelled, latest)
    raw_prob_up = float(raw_probabilities[0])
    prob_up = float(_calibrate(np.array([raw_prob_up]), calibration_slope)[0])
    prob_down = 1.0 - prob_up
    predicted = "UP" if prob_up >= 0.5 else "DOWN"
    validation_summary = _validation_summary(
        validation,
        raw_oos_probability,
        calibrated_oos_probability,
        validation_dispersion[validation_mask],
    )
    return_distribution = _conditional_return_distribution(
        validation,
        calibrated_oos_probability,
        prob_up,
        labelled["target_return"].to_numpy(dtype=float),
    )
    training_start = str(labelled.iloc[0]["trade_date"])
    training_end = str(labelled.iloc[-1]["trade_date"])
    latest_trade_date = str(frame.iloc[-1]["trade_date"])
    return {
        "model_ready": True,
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
        "primary_model": "T+1 histogram-gradient-boosting ensemble",
        "predicted_direction": predicted,
        "prob_up_1d": prob_up,
        "prob_down_1d": prob_down,
        "prob_flat_1d": 0.0,
        "direction_confidence": max(prob_up, prob_down),
        "raw_prob_up_1d": raw_prob_up,
        "calibration_slope": calibration_slope,
        "ensemble_dispersion": float(current_dispersion[0]),
        "fallback_used": False,
        "fallback_reason": None,
        "latest_data_trade_date": latest_trade_date,
        "training": {
            "start_date": training_start,
            "end_date": training_end,
            "sample_size": int(len(labelled)),
            "feature_count": len(FEATURE_COLUMNS),
            "ensemble_size": len(MODEL_SPECS),
            "refit_interval_days": REFIT_INTERVAL_DAYS,
            "target": "next_trading_day_close_direction",
        },
        "validation": validation_summary,
        "model_return_distribution": return_distribution,
        "inputs": {
            "daily_rows": int(len(frame)),
            "moneyflow_available": moneyflow is not None and hasattr(moneyflow, "empty") and not moneyflow.empty,
            "feature_columns": list(FEATURE_COLUMNS),
        },
    }


def unavailable_model(reason: str) -> dict[str, Any]:
    return {
        "model_ready": False,
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
        "primary_model": "T+1 histogram-gradient-boosting ensemble",
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
        "training": {},
        "validation": {},
        "model_return_distribution": {},
        "inputs": {},
    }


def build_feature_frame(daily: Any, moneyflow: Any = None) -> pd.DataFrame:
    if daily is None or not isinstance(daily, pd.DataFrame) or daily.empty:
        return pd.DataFrame()
    required = {"trade_date", "open", "high", "low", "close", "pre_close", "vol", "amount"}
    missing = sorted(required.difference(daily.columns))
    if missing:
        raise KeyError(",".join(missing))

    frame = daily.copy()
    frame["trade_date"] = frame["trade_date"].map(_date_text)
    frame = frame.dropna(subset=["trade_date"]).sort_values("trade_date").drop_duplicates("trade_date", keep="last")
    numeric_daily = ("open", "high", "low", "close", "pre_close", "vol", "amount", "pct_chg")
    for column in numeric_daily:
        if column not in frame:
            frame[column] = np.nan
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    flow = _normalise_moneyflow(moneyflow)
    if not flow.empty:
        frame = frame.merge(flow, on="trade_date", how="left")
    for column in MONEYFLOW_COLUMNS:
        if column not in frame:
            frame[column] = np.nan

    close = frame["close"].replace(0, np.nan)
    pre_close = frame["pre_close"].replace(0, np.nan)
    open_price = frame["open"].replace(0, np.nan)
    ret_1 = frame["pct_chg"] / 100.0
    ret_1 = ret_1.where(ret_1.notna(), close / pre_close - 1.0).clip(-0.25, 0.25)
    log_return = np.log1p(ret_1.clip(lower=-0.95))
    frame["ret_1"] = ret_1
    for window in (2, 5, 20):
        frame[f"ret_{window}"] = np.expm1(log_return.rolling(window).sum()).clip(-0.6, 0.6)
    frame["gap"] = (frame["open"] / pre_close - 1.0).clip(-0.2, 0.2)
    frame["intraday"] = (frame["close"] / open_price - 1.0).clip(-0.2, 0.2)
    frame["range"] = ((frame["high"] - frame["low"]) / pre_close).clip(0.0, 0.3)
    frame["close_position"] = (frame["close"] - frame["low"]) / (frame["high"] - frame["low"]).replace(0, np.nan)

    delta = ret_1
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    frame["rsi_14"] = gain / (gain + loss).replace(0, np.nan)
    for window in (5, 20):
        frame[f"volatility_{window}"] = ret_1.rolling(window).std().clip(0.0, 0.2)
    for window in (5, 20, 60):
        frame[f"close_ma_{window}"] = (close / close.rolling(window).mean() - 1.0).clip(-0.5, 0.5)
    frame["volume_ratio_20"] = (frame["vol"] / frame["vol"].rolling(20).mean()).clip(0.0, 8.0)

    amount = frame["amount"].replace(0, np.nan)
    main_force = frame["buy_lg_amount"] + frame["buy_elg_amount"] - frame["sell_lg_amount"] - frame["sell_elg_amount"]
    frame["net_mf_ratio"] = (frame["net_mf_amount"] / amount).clip(-1.0, 1.0)
    frame["main_force_ratio"] = (main_force / amount).clip(-1.0, 1.0)
    for window in (5, 20):
        rolling_amount = amount.rolling(window).sum().replace(0, np.nan)
        frame[f"net_mf_ratio_{window}"] = (frame["net_mf_amount"].rolling(window).sum() / rolling_amount).clip(-1.0, 1.0)
        frame[f"main_force_ratio_{window}"] = (main_force.rolling(window).sum() / rolling_amount).clip(-1.0, 1.0)

    parsed_dates = pd.to_datetime(frame["trade_date"], errors="coerce")
    frame["weekday"] = parsed_dates.dt.weekday
    frame["ret_sign"] = np.sign(frame["ret_1"])
    frame["flow_sign"] = np.sign(frame["net_mf_ratio"])
    frame["trend_5_20"] = frame["close_ma_5"] - frame["close_ma_20"]
    frame["vol_regime"] = (frame["volatility_5"] / frame["volatility_20"].replace(0, np.nan)).clip(0.0, 5.0)

    frame["target_return"] = ret_1.shift(-1)
    frame["target"] = np.where(
        frame["target_return"] > 0,
        1.0,
        np.where(frame["target_return"] < 0, 0.0, np.nan),
    )
    frame = frame.replace([np.inf, -np.inf], np.nan)
    frame = frame.iloc[60:].reset_index(drop=True)
    return frame[["trade_date", "target", "target_return", *FEATURE_COLUMNS]]


def _normalise_moneyflow(moneyflow: Any) -> pd.DataFrame:
    if moneyflow is None or not isinstance(moneyflow, pd.DataFrame) or moneyflow.empty or "trade_date" not in moneyflow:
        return pd.DataFrame()
    flow = moneyflow.copy()
    flow["trade_date"] = flow["trade_date"].map(_date_text)
    flow = flow.dropna(subset=["trade_date"]).sort_values("trade_date").drop_duplicates("trade_date", keep="last")
    for column in MONEYFLOW_COLUMNS:
        if column not in flow:
            flow[column] = np.nan
        flow[column] = pd.to_numeric(flow[column], errors="coerce")
    return flow[["trade_date", *MONEYFLOW_COLUMNS]]


def _fit_predict_ensemble(train: pd.DataFrame, test: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    x_train = train.loc[:, FEATURE_COLUMNS]
    y_train = train["target"].astype(int)
    x_test = test.loc[:, FEATURE_COLUMNS]
    if y_train.nunique() < 2:
        base = float(y_train.mean())
        return np.full(len(test), base), np.zeros(len(test))
    predictions: list[np.ndarray] = []
    for spec in MODEL_SPECS:
        model = HistGradientBoostingClassifier(
            max_iter=spec.max_iter,
            learning_rate=spec.learning_rate,
            max_leaf_nodes=spec.max_leaf_nodes,
            max_depth=spec.max_depth,
            min_samples_leaf=spec.min_samples_leaf,
            l2_regularization=spec.l2_regularization,
            random_state=42,
        )
        if spec.half_life:
            age = np.arange(len(train) - 1, -1, -1, dtype=float)
            weights = np.exp(-math.log(2.0) * age / spec.half_life)
            model.fit(x_train, y_train, sample_weight=weights)
        else:
            model.fit(x_train, y_train)
        predictions.append(model.predict_proba(x_test)[:, 1])
    matrix = np.vstack(predictions)
    return matrix.mean(axis=0), matrix.std(axis=0)


def _calibration_slope(probabilities: np.ndarray, target: np.ndarray) -> float:
    if len(probabilities) < 30:
        return 0.5
    centered = probabilities - 0.5
    denominator = float(np.dot(centered, centered))
    if denominator <= 1e-12:
        return 0.5
    slope = float(np.dot(centered, target - 0.5) / denominator)
    return min(1.0, max(0.05, slope))


def _calibrate(probabilities: np.ndarray, slope: float) -> np.ndarray:
    return np.clip(0.5 + slope * (probabilities - 0.5), 0.05, 0.95)


def _validation_summary(
    validation: pd.DataFrame,
    raw_probability: np.ndarray,
    calibrated_probability: np.ndarray,
    dispersion: np.ndarray,
) -> dict[str, Any]:
    if validation.empty:
        return {}
    target = validation["target"].to_numpy(dtype=int)
    predicted = (calibrated_probability >= 0.5).astype(int)
    correct = predicted == target
    accuracy = float(correct.mean())
    ci_low, ci_high = _wilson_interval(int(correct.sum()), len(correct))
    high_confidence = (calibrated_probability >= HIGH_CONFIDENCE_THRESHOLD) | (
        calibrated_probability <= 1.0 - HIGH_CONFIDENCE_THRESHOLD
    )
    high_count = int(high_confidence.sum())
    high_accuracy = float(correct[high_confidence].mean()) if high_count else None
    try:
        auc = float(roc_auc_score(target, calibrated_probability))
    except ValueError:
        auc = None
    return {
        "model": MODEL_ID,
        "horizon": "1D",
        "method": "expanding_walk_forward",
        "sample_size": int(len(validation)),
        "start_date": str(validation.iloc[0]["trade_date"]),
        "end_date": str(validation.iloc[-1]["trade_date"]),
        "directional_accuracy": accuracy,
        "accuracy_ci_95_low": ci_low,
        "accuracy_ci_95_high": ci_high,
        "brier_raw": float(brier_score_loss(target, raw_probability)),
        "brier_calibrated": float(brier_score_loss(target, calibrated_probability)),
        "roc_auc": auc,
        "actual_up_rate": float(target.mean()),
        "high_confidence_threshold": HIGH_CONFIDENCE_THRESHOLD,
        "high_confidence_sample_size": high_count,
        "high_confidence_coverage": float(high_confidence.mean()),
        "high_confidence_accuracy": high_accuracy,
        "mean_ensemble_dispersion": float(np.nanmean(dispersion)),
        "refit_interval_days": REFIT_INTERVAL_DAYS,
        "leakage_guard": "every validation prediction is fitted only on earlier trade dates",
    }


def _conditional_return_distribution(
    validation: pd.DataFrame,
    probability: np.ndarray,
    current_probability: float,
    fallback_returns: np.ndarray,
) -> dict[str, Any]:
    returns = validation["target_return"].to_numpy(dtype=float) if not validation.empty else np.array([], dtype=float)
    finite = np.isfinite(returns) & np.isfinite(probability)
    returns = returns[finite]
    comparable_probability = probability[finite]
    current_up = current_probability >= 0.5
    same_direction = (comparable_probability >= 0.5) == current_up
    candidates = np.flatnonzero(same_direction)
    if len(candidates) >= 120:
        nearest = candidates[np.argsort(np.abs(comparable_probability[candidates] - current_probability))[:300]]
        selected = returns[nearest]
        method = "walk_forward_nearest_probability_same_direction"
    else:
        selected = np.asarray(fallback_returns, dtype=float)
        selected = selected[np.isfinite(selected)]
        method = "historical_1d_empirical_fallback"
    if len(selected) == 0:
        selected = np.array([-0.01, 0.0, 0.01], dtype=float)
        method = "neutral_distribution_fallback"

    bins = {
        "gt_5pct": float(np.mean(selected > 0.05)),
        "plus_2_to_5pct": float(np.mean((selected > 0.02) & (selected <= 0.05))),
        "zero_to_plus_2pct": float(np.mean((selected >= 0.0) & (selected <= 0.02))),
        "zero_to_minus_2pct": float(np.mean((selected < 0.0) & (selected >= -0.02))),
        "minus_2_to_5pct": float(np.mean((selected < -0.02) & (selected >= -0.05))),
        "lt_minus_5pct": float(np.mean(selected < -0.05)),
    }
    total = sum(bins.values()) or 1.0
    bins = {key: value / total for key, value in bins.items()}
    return {
        "return_bins_1d": bins,
        "expected_return_1d": float(np.mean(selected)),
        "median_return_1d": float(np.median(selected)),
        "p10_return_1d": float(np.quantile(selected, 0.10)),
        "p90_return_1d": float(np.quantile(selected, 0.90)),
        "distribution_source": f"{MODEL_ID}:{method}",
        "sample_size": int(len(selected)),
    }


def _wilson_interval(successes: int, sample_size: int) -> tuple[float, float]:
    if sample_size <= 0:
        return 0.0, 0.0
    z = 1.959963984540054
    rate = successes / sample_size
    denominator = 1.0 + z * z / sample_size
    centre = (rate + z * z / (2.0 * sample_size)) / denominator
    margin = z * math.sqrt((rate * (1.0 - rate) + z * z / (4.0 * sample_size)) / sample_size) / denominator
    return max(0.0, centre - margin), min(1.0, centre + margin)


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


def _latest_input_date(frame: Any) -> str | None:
    if frame is None or not isinstance(frame, pd.DataFrame) or frame.empty or "trade_date" not in frame:
        return None
    dates = [_date_text(value) for value in frame["trade_date"]]
    return max((value for value in dates if value), default=None)
