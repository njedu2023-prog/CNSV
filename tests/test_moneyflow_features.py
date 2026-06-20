import pandas as pd

from cnsv.features.moneyflow_features import build_moneyflow_features


def test_moneyflow_core_calculations():
    moneyflow = pd.DataFrame(
        {
            "trade_date": [f"2026-06-{day:02d}" for day in range(1, 12)],
            "buy_sm_amount": [10] * 11,
            "sell_sm_amount": [5] * 11,
            "buy_md_amount": [20] * 11,
            "sell_md_amount": [10] * 11,
            "buy_lg_amount": [30] * 11,
            "sell_lg_amount": [10] * 11,
            "buy_elg_amount": [40] * 11,
            "sell_elg_amount": [20] * 11,
            "net_mf_amount": [-100, 100, 100, -100, 100, 100, 100, 100, 100, 100, 100],
        }
    )
    daily = pd.DataFrame({"trade_date": ["2026-06-11"], "amount": [1000]})
    price_volume = {"ret_1d": -0.01, "volume_ratio_5d": 1.2}
    features = build_moneyflow_features(moneyflow, {"can_use_moneyflow_as_strong_factor": True}, "2026-06-11", daily, price_volume)

    assert features["small_order_net"] == 5
    assert features["main_force_net"] == 40
    assert features["net_mf_ratio"] == 0.1
    assert features["flow_strength_score"] == 90
    assert -100 <= features["flow_strength_score"] <= 100
    assert features["price_flow_divergence"] is True
    assert features["volume_flow_confirm"] == "inflow_confirmed"
    assert features["positive_flow_days_10d"] == 9
