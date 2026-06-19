from cnsv.data.data_manifest import validate_manifest


def test_manifest_missing_snapshot_id_fails():
    result = validate_manifest({"generated_at": "now", "latest_trade_date": "2026-06-19", "files": []})
    assert result["status"] == "FAIL"


def test_manifest_missing_files_fails():
    result = validate_manifest({"snapshot_id": "s1", "generated_at": "now", "latest_trade_date": "2026-06-19"})
    assert result["status"] == "FAIL"


def test_manifest_normal_passes():
    result = validate_manifest(
        {
            "snapshot_id": "s1",
            "generated_at": "now",
            "latest_trade_date": "2026-06-19",
            "files": [{"path": "data/processed/cnsv_daily.parquet", "sha256": "abc", "rows": 3}],
        }
    )
    assert result["status"] == "PASS"
