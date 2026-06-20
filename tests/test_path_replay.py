from __future__ import annotations

import pandas as pd
import pytest

from cnsv.path.path_replay import build_path_samples, max_drawdown


def test_build_path_samples_returns_t_plus_paths() -> None:
    daily = pd.DataFrame(
        {
            "trade_date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
            "close": [10.0, 11.0, 12.0, 13.0],
            "high": [10.2, 11.5, 12.5, 13.5],
            "low": [9.8, 10.5, 11.5, 12.5],
        }
    )
    samples, meta = build_path_samples(daily, horizon=2, latest_close=20.0)
    assert len(samples) == 2
    assert meta["dropped_count"] == 0
    assert samples[0]["close_return_path"] == pytest.approx([0.1, 0.2])
    assert samples[0]["close_price_path"] == pytest.approx([22.0, 24.0])


def test_max_drawdown_uses_path_running_high() -> None:
    assert round(max_drawdown([0.1, -0.1, 0.05]) or 0, 4) == -0.1818
