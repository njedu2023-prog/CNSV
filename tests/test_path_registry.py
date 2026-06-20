from __future__ import annotations

from cnsv.path.path_distribution import build_path_registry


def test_path_registry_contains_three_models() -> None:
    registry = build_path_registry()
    assert [row["model_id"] for row in registry] == [
        "P0_historical_path_replay",
        "P1_volatility_adjusted_path",
        "P2_state_conditional_path",
    ]
    assert all(row["is_trade_signal"] is False for row in registry)
