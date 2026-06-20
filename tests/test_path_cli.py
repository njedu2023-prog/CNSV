from __future__ import annotations

from pathlib import Path


def test_path_cli_modules_are_importable() -> None:
    import cnsv.cli.run_path_distribution as distribution
    import cnsv.cli.run_path_validation as validation

    assert callable(distribution.main)
    assert callable(validation.main)


def test_path_report_paths_are_documented() -> None:
    assert Path("docs/data/latest_path_distribution_report.json").as_posix().endswith(".json")
    assert Path("docs/path.html").as_posix().endswith(".html")
