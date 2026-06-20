from test_walk_forward_validation import _bundle

from cnsv.cli import run_baseline_validation


def test_run_baseline_validation_cli_runs_with_mock_data(tmp_path, monkeypatch):
    bundle = _bundle()
    monkeypatch.setattr(run_baseline_validation, "load_default_config", lambda: {"data_source": {}})
    monkeypatch.setattr(run_baseline_validation, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(run_baseline_validation, "load_all_core_data", lambda source: bundle)

    assert run_baseline_validation.main() == 0
    assert (tmp_path / "docs/data/latest_baseline_validation_report.json").exists()
    assert (tmp_path / "docs/data/baseline_validation_registry.json").exists()
    assert (tmp_path / "docs/validation.html").exists()
    assert (tmp_path / "docs/index.html").exists()
    assert (tmp_path / "reports/latest_baseline_validation_report.md").exists()
