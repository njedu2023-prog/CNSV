from cnsv.backtest.backtest_registry import build_observation_backtest_registry


def test_backtest_registry_is_observation_only():
    reg = build_observation_backtest_registry()[0]
    assert reg["version"] == "1.4"
    assert reg["backtest_type"] == "observation_only"
    assert reg["is_trade_signal"] is False
