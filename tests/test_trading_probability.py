from cnsv.trading.evidence_loader import load_trading_evidence
from cnsv.trading.probability import compute_next_day_probability
from cnsv.utils.io import repo_root


def test_trading_probability_outputs_valid_probabilities():
    reports = load_trading_evidence(repo_root())["reports"]
    probability = compute_next_day_probability(reports)

    assert 0 <= probability["prob_up_1d"] <= 1
    assert 0 <= probability["prob_down_1d"] <= 1
    assert 0 <= probability["prob_flat_1d"] <= 1
    assert probability["prob_up_1d"] + probability["prob_down_1d"] == 1.0
    assert probability["prob_flat_1d"] == 0.0
    assert probability["primary_model"]
    assert probability["model_id"] == "T1_HGB_ENSEMBLE_V1"
    assert "5D" not in probability["primary_model"]
