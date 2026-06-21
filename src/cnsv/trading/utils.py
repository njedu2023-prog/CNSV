from __future__ import annotations

from collections.abc import Iterable
from math import erf, sqrt
from typing import Any


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def first_number(*values: Any, default: float = 0.0) -> float:
    for value in values:
        if value is not None:
            return safe_float(value, default)
    return default


def mean(values: Iterable[float], default: float = 0.0) -> float:
    clean = [v for v in values if v is not None]
    return sum(clean) / len(clean) if clean else default


def normal_cdf(x: float, mu: float, sigma: float) -> float:
    if sigma <= 0:
        return 1.0 if x >= mu else 0.0
    return 0.5 * (1.0 + erf((x - mu) / (sigma * sqrt(2.0))))


def pct(value: float, digits: int = 2) -> str:
    sign = "+" if value > 0 else ""
    return f"{sign}{value * 100:.{digits}f}%"


def probability_pct(value: float, digits: int = 2) -> str:
    return f"{value * 100:.{digits}f}%"


def get_path(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    node: Any = data
    for key in keys:
        if not isinstance(node, dict) or key not in node:
            return default
        node = node[key]
    return node
