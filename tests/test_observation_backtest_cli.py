from cnsv.cli.run_observation_backtest import _ensure_backtest_entry


def test_ensure_backtest_entry(tmp_path):
    path = tmp_path / "index.html"
    path.write_text("<nav></nav>", encoding="utf-8")
    _ensure_backtest_entry(path)
    assert 'href="backtest.html"' in path.read_text(encoding="utf-8")
