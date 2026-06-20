from cnsv.cli.run_human_decision_support import _contains_forbidden_key, _ensure_index_entry


def test_ensure_decision_support_entry(tmp_path):
    path = tmp_path / "index.html"
    path.write_text("<title>CNSV V1.4 主线看板</title><nav></nav>", encoding="utf-8")

    _ensure_index_entry(path)
    text = path.read_text(encoding="utf-8")

    assert "CNSV V1.5 主线看板" in text
    assert 'href="decision_support.html"' in text


def test_forbidden_trade_field_detection():
    assert _contains_forbidden_key({"buy_signal": True}) is True
    assert _contains_forbidden_key({"support_levels": {"evidence_strength": "moderate"}}) is False
