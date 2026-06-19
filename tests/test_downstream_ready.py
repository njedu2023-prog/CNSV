from cnsv.data.downstream_ready import evaluate_downstream_gate


def payload(ready=True, status="PASS", **usage):
    allowed_usage = {
        "can_develop_cnsv_main_program": True,
        "can_run_daily_ingest": True,
        "can_run_backtest": True,
        "can_use_moneyflow_as_strong_factor": True,
        "can_generate_formal_signal": False,
    }
    allowed_usage.update(usage)
    return {"ready": ready, "status": status, "allowed_usage": allowed_usage}


def test_ready_false_blocks():
    gate = evaluate_downstream_gate(payload(ready=False))
    assert gate["can_continue"] is False
    assert "ready is false" in gate["blocking_reason"]


def test_fail_status_blocks():
    gate = evaluate_downstream_gate(payload(status="FAIL"))
    assert gate["can_continue"] is False
    assert gate["status"] == "FAIL"


def test_warn_status_degrades_but_continues():
    gate = evaluate_downstream_gate(payload(status="WARN"))
    assert gate["can_continue"] is True
    assert gate["warnings"]


def test_pass_status_continues():
    gate = evaluate_downstream_gate(payload(status="PASS"))
    assert gate["can_continue"] is True


def test_formal_signal_false_is_preserved():
    gate = evaluate_downstream_gate(payload(can_generate_formal_signal=False))
    assert gate["can_generate_formal_signal"] is False
    assert any("formal signal" in item for item in gate["warnings"])
