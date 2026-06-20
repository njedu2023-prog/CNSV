from test_walk_forward_validation import _bundle

from cnsv.validation.baseline_validation import run_baseline_validation


def test_baseline_validation_report_keeps_non_trade_boundary():
    bundle = _bundle()
    payload = run_baseline_validation(bundle, bundle["gate"])
    assert payload["meta"]["version"] == "1.2.2"
    assert payload["meta"]["is_trade_signal"] is False
    assert payload["validation_quality"]["status"] in {"PASS", "WARN"}
    assert "formal_signal_generation" in payload["forbidden_actions"]
    assert "B2_state_grouped_distribution" in payload["model_metrics"]["standard_walk_forward_metrics"]
