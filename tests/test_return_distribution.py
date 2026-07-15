from cnsv.trading.evidence_loader import load_trading_evidence
from cnsv.trading.probability import compute_next_day_probability
from cnsv.trading.return_distribution import compute_return_distribution
from cnsv.utils.io import repo_root


def test_return_distribution_bins_sum_to_one():
    reports = load_trading_evidence(repo_root())["reports"]
    distribution = compute_return_distribution(reports, compute_next_day_probability(reports))

    assert set(distribution["return_bins_1d"]) == {
        "gt_5pct",
        "plus_2_to_5pct",
        "zero_to_plus_2pct",
        "zero_to_minus_2pct",
        "minus_2_to_5pct",
        "lt_minus_5pct",
    }
    assert abs(sum(distribution["return_bins_1d"].values()) - 1.0) < 1e-9
    assert distribution["p10_return_1d"] <= distribution["p90_return_1d"]
    assert "scaled_to_1D" not in distribution["distribution_source"]
