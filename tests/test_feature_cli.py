import pandas as pd

from cnsv.cli import generate_feature_report


def test_generate_feature_report_cli_runs_with_mock_data(tmp_path, monkeypatch):
    dates = [f"2026-06-{day:02d}" for day in range(1, 61)]
    daily = pd.DataFrame(
        {
            "trade_date": dates,
            "open": range(60),
            "high": [value + 1 for value in range(60)],
            "low": [value - 1 for value in range(60)],
            "close": range(1, 61),
            "amount": [1000] * 60,
            "vol": [100] * 60,
        }
    )
    one_min = pd.DataFrame(
        {
            "trade_date": ["2026-06-30"] * 61,
            "time": range(61),
            "open": range(61),
            "high": [value + 1 for value in range(61)],
            "low": [value - 1 for value in range(61)],
            "close": range(1, 62),
            "amount": [100] * 61,
            "vol": [10] * 61,
        }
    )
    moneyflow = pd.DataFrame(
        {
            "trade_date": [f"2026-06-{day:02d}" for day in range(21, 31)],
            "buy_sm_amount": [10] * 10,
            "sell_sm_amount": [5] * 10,
            "buy_md_amount": [20] * 10,
            "sell_md_amount": [10] * 10,
            "buy_lg_amount": [30] * 10,
            "sell_lg_amount": [10] * 10,
            "buy_elg_amount": [40] * 10,
            "sell_elg_amount": [20] * 10,
            "net_mf_amount": [100] * 10,
        }
    )
    bundle = {
        "daily": daily,
        "one_min": one_min,
        "moneyflow": moneyflow,
        "gate": {"status": "PASS", "ready": True, "can_continue": True, "can_use_moneyflow_as_strong_factor": True},
        "data_manifest": {"latest_trade_date": "2026-06-30", "files": []},
    }
    monkeypatch.setattr(generate_feature_report, "load_default_config", lambda: {"data_source": {}})
    monkeypatch.setattr(generate_feature_report, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(generate_feature_report, "load_all_core_data", lambda source: bundle)

    assert generate_feature_report.main() == 0
    assert (tmp_path / "docs/data/latest_feature_report.json").exists()
    assert (tmp_path / "reports/latest_feature_report.md").exists()
    assert (tmp_path / "docs/data/feature_registry.json").exists()
