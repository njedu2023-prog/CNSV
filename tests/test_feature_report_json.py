from cnsv.features.feature_registry import build_feature_registry
from cnsv.report.feature_report_json import build_feature_report_payload


def test_feature_report_json_structure_complete():
    payload = build_feature_report_payload(
        {"status": "PASS", "can_generate_formal_signal": False},
        {"latest_trade_date": "2026-06-18", "files": []},
        {"price_volume": {}, "minute_structure": {}, "moneyflow": {}, "trend": {}, "volatility": {}},
        {"status": "PASS", "failed_count": 0, "warn_count": 0, "checks": []},
        build_feature_registry(),
    )
    assert payload["meta"]["report_type"] == "feature_report"
    assert payload["allowed_actions"]["can_generate_formal_signal"] is False
    assert "formal_signal_generation" in payload["forbidden_actions"]
    assert {"price_volume", "minute_structure", "moneyflow", "trend", "volatility"}.issubset(payload["features"])
