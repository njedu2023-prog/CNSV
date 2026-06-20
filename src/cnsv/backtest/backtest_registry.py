from __future__ import annotations

import json
from pathlib import Path

from cnsv.backtest import BACKTEST_STAGE, BACKTEST_VERSION
from cnsv.models.baseline_schema import HORIZONS
from cnsv.path import PATH_MODEL_IDS
from cnsv.utils.io import ensure_parent


def build_observation_backtest_registry() -> list[dict[str, object]]:
    return [
        {
            "registry_type": "observation_backtest",
            "version": BACKTEST_VERSION,
            "stage": BACKTEST_STAGE,
            "models": list(PATH_MODEL_IDS),
            "horizons": list(HORIZONS),
            "backtest_type": "observation_only",
            "is_trade_signal": False,
            "forbidden": ["formal_signal_generation", "auto_order", "broker_api"],
        }
    ]


def write_observation_backtest_registry(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(build_observation_backtest_registry(), ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return target
