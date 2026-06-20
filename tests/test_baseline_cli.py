import pandas as pd

from cnsv.cli import run_baseline_models


def test_run_baseline_models_cli_runs_with_mock_data(tmp_path, monkeypatch):
    daily = pd.DataFrame(
        {
            "trade_date": [f"2026-06-{(i % 28) + 1:02d}" for i in range(90)],
            "open": [20 + i * 0.1 for i in range(90)],
            "high": [20.5 + i * 0.1 for i in range(90)],
            "low": [19.5 + i * 0.1 for i in range(90)],
            "close": [20 + i * 0.1 for i in range(90)],
            "amount": [1000] * 90,
            "vol": [100] * 90,
        }
    )
    one_min = pd.DataFrame(
        {
            "trade_date": ["2026-06-18"] * 80,
            "time": range(80),
            "open": range(80),
            "high": [value + 1 for value in range(80)],
            "low": [value - 1 for value in range(80)],
            "close": range(1, 81),
            "amount": [100] * 80,
            "vol": [10] * 80,
        }
    )
    moneyflow = pd.DataFrame(
        {
            "trade_date": [f"2026-06-{(i % 28) + 1:02d}" for i in range(30)],
            "buy_sm_amount": [10] * 30,
            "sell_sm_amount": [5] * 30,
            "buy_md_amount": [20] * 30,
            "sell_md_amount": [10] * 30,
            "buy_lg_amount": [30] * 30,
            "sell_lg_amount": [10] * 30,
            "buy_elg_amount": [40] * 30,
            "sell_elg_amount": [20] * 30,
            "net_mf_amount": [100] * 30,
        }
    )
    bundle = {
        "daily": daily,
        "one_min": one_min,
        "moneyflow": moneyflow,
        "gate": {"status": "PASS", "ready": True, "can_continue": True, "can_use_moneyflow_as_strong_factor": True},
        "data_manifest": {"latest_trade_date": "2026-06-18", "files": []},
    }
    monkeypatch.setattr(run_baseline_models, "load_default_config", lambda: {"data_source": {}})
    monkeypatch.setattr(run_baseline_models, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(run_baseline_models, "load_all_core_data", lambda source: bundle)

    assert run_baseline_models.main() == 0
    assert (tmp_path / "docs/data/latest_baseline_model_report.json").exists()
    assert (tmp_path / "docs/data/baseline_registry.json").exists()
    assert (tmp_path / "docs/baseline.html").exists()
    assert (tmp_path / "docs/index.html").exists()
    assert (tmp_path / "reports/latest_baseline_model_report.md").exists()
