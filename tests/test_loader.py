import pytest

from cnsv.data import loader
from cnsv.utils.errors import DownstreamGateError


def source_config():
    return {
        "cnsvdata": {"raw_base_url": "https://example.invalid"},
        "required_remote_files": {
            "downstream_ready": "ready.json",
            "data_manifest": "manifest.json",
            "trade_calendar": "calendar.parquet",
            "daily": "daily.parquet",
            "one_min": "one_min.parquet",
            "five_min": "five.parquet",
            "fifteen_min": "fifteen.parquet",
            "thirty_min": "thirty.parquet",
            "sixty_min": "sixty.parquet",
            "moneyflow": "moneyflow.parquet",
            "corporate_actions": "corp.parquet",
            "structural_breaks": "breaks.parquet",
        },
    }


def test_ready_false_does_not_read_parquet(monkeypatch):
    calls = []
    monkeypatch.setattr(loader, "load_downstream_ready", lambda cfg: {"ready": False, "status": "FAIL", "allowed_usage": {}})
    monkeypatch.setattr(loader, "fetch_parquet", lambda url: calls.append(url))
    with pytest.raises(DownstreamGateError):
        loader.load_all_core_data(source_config())
    assert calls == []


def test_ready_true_reads_parquet_after_gate(monkeypatch):
    calls = []
    ready = {
        "ready": True,
        "status": "PASS",
        "allowed_usage": {
            "can_develop_cnsv_main_program": True,
            "can_run_daily_ingest": True,
            "can_run_backtest": True,
            "can_use_moneyflow_as_strong_factor": True,
            "can_generate_formal_signal": False,
        },
    }
    monkeypatch.setattr(loader, "load_downstream_ready", lambda cfg: ready)
    monkeypatch.setattr(loader, "load_data_manifest", lambda cfg: {"snapshot_id": "s1"})
    monkeypatch.setattr(loader, "fetch_parquet", lambda url: calls.append(url) or "df")
    bundle = loader.load_all_core_data(source_config())
    assert calls
    assert bundle["daily"] == "df"
