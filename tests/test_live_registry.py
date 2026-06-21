from cnsv.live.live_registry import build_live_manual_decision_registry, write_live_manual_decision_registry
def test_live_registry_contains_v2_outputs(tmp_path):
 r=build_live_manual_decision_registry(); assert r[0]["version"]=="2.0"; assert "latest_live_manual_decision_report.json" in r[0]["outputs"]; assert write_live_manual_decision_registry(tmp_path/"registry.json").exists()
