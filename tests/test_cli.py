from cnsv.cli import build_features, check_data, generate_data_report


def test_cli_modules_import_and_have_main():
    assert callable(check_data.main)
    assert callable(build_features.main)
    assert callable(generate_data_report.main)
