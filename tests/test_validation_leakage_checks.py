import pandas as pd

from cnsv.validation.leakage_checks import check_training_window, contains_forbidden_validation_key


def test_training_window_rejects_future_rows():
    frame = pd.DataFrame({"trade_date": ["2026-01-01", "2026-01-03"]})
    check = check_training_window("2026-01-02", [frame])
    assert check["status"] == "FAIL"


def test_forbidden_validation_keys_do_not_flag_required_guardrail_values():
    payload = {"meta": {"is_trade_signal": False}, "forbidden_actions": ["formal_signal_generation"]}
    assert contains_forbidden_validation_key(payload) is False
    assert contains_forbidden_validation_key({"buy_signal": True}) is True
