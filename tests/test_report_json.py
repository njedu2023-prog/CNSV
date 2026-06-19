from cnsv.report.report_json import build_report_payload


def test_report_json_contains_required_sections():
    payload = build_report_payload({"ready": True, "status": "PASS", "can_continue": True})
    assert "meta" in payload
    assert "cnsvdata_gate" in payload
    assert "validation" in payload
    assert "features" in payload
    assert "forbidden_actions" in payload
    assert "formal_signal_generation" in payload["forbidden_actions"]
    assert payload["allowed_actions"]["can_generate_formal_signal"] is False
