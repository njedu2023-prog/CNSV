from cnsv.risk.risk_scenarios import build_risk_scenario_cards


def test_risk_scenario_cards_include_required_and_exclude_trade_cards():
    cards = build_risk_scenario_cards({"risk_evidence_availability": {"missing_reports": []}, "path_distribution_risk_explanation": {}, "evidence_conflict_risk_explanation": {}, "p2_auxiliary_risk_explanation": {}, "data_risk_explanation": {}})
    ids = {card["scenario_id"] for card in cards}
    assert {"downside_touch_risk_card", "max_drawdown_risk_card", "model_conflict_risk_card", "p2_instability_risk_card"}.issubset(ids)
    assert not {"buy_card", "sell_card", "stop_loss_card", "take_profit_card", "position_card"} & ids
