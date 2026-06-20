from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cnsv.models.baseline_schema import HORIZONS
from cnsv.utils.io import ensure_parent


def build_baseline_registry() -> list[dict[str, Any]]:
    common = {
        "horizons": list(HORIZONS),
        "is_trade_signal": False,
        "stage": "V1.2_baseline_model",
    }
    return [
        {
            **common,
            "model_id": "B0_random_walk",
            "model_name": "随机游走基准",
            "description": "以当前收盘价为中位路径，使用近期波动率估计 5D/10D/20D 终端收益分布。",
            "input_data": ["daily.close"],
            "input_features": ["volatility_estimate"],
            "output_fields": ["expected_return", "expected_price", "p10_return", "p50_return", "p90_return"],
        },
        {
            **common,
            "model_id": "B1_historical_distribution",
            "model_name": "历史分布基准",
            "description": "使用全样本历史 h 日终端收益经验分布。",
            "input_data": ["daily.close"],
            "input_features": [],
            "output_fields": ["mean_return", "median_return", "positive_prob", "p05_return", "p95_return"],
        },
        {
            **common,
            "model_id": "B2_state_grouped_distribution",
            "model_name": "状态分组历史分布",
            "description": "按趋势、波动率、资金流状态分组；样本不足时透明回退到 B1。",
            "input_data": ["daily.close"],
            "input_features": ["trend_state", "volatility_state", "flow_strength_basic"],
            "output_fields": ["state_key", "state_sample_size", "fallback_used", "p10_return", "p90_return"],
        },
        {
            **common,
            "model_id": "B3_volatility_adjusted",
            "model_name": "波动率调整历史分布",
            "description": "在 B1 历史分布基础上按当前 20D 实现波动率调整分布宽度。",
            "input_data": ["daily.close"],
            "input_features": ["realized_vol_20d"],
            "output_fields": ["volatility_scale", "adjusted_std", "p10_return", "p90_return"],
        },
    ]


def write_baseline_registry(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(json.dumps(build_baseline_registry(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target

