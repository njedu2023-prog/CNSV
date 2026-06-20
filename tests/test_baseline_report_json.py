from cnsv.models.baseline_registry import build_baseline_registry
from cnsv.report.baseline_report_json import build_baseline_report_payload


def test_baseline_report_json_has_required_sections():
    payload = build_baseline_report_payload(
        {"status": "PASS", "ready": True},
        {"latest_trade_date": "2026-06-18", "files": []},
        {
            "price_volume": {"latest_close": 36.14},
            "trend": {"trend_state": "downtrend"},
            "volatility": {"volatility_state": "normal_vol"},
            "moneyflow": {"flow_strength_basic": "mixed", "can_use_as_strong_factor": True},
        },
        {"status": "PASS", "failed_count": 0, "warn_count": 0},
        {"models": {}, "baseline_quality": {"status": "PASS"}, "current_close": 36.14},
        build_baseline_registry(),
    )
    assert payload["meta"]["report_type"] == "baseline_model_report"
    assert payload["meta"]["is_trade_signal"] is False
    assert payload["meta"]["version"] == "1.2.1"
    assert payload["meta"]["stage"] == "V1.2.1_state_grouped_baseline_fix"
    assert "baseline_models" in payload
    assert payload["next_stage"] == "V1.2.2 baseline validation / walk-forward validation"
