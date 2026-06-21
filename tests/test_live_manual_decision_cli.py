import json
from cnsv.cli.run_live_manual_decision import main
from cnsv.utils.io import repo_root
def test_live_manual_decision_cli_generates_outputs():
 assert main()==0; root=repo_root(); rp=root/"docs/data/latest_live_manual_decision_report.json"; assert rp.exists(); assert (root/"docs/data/live_manual_decision_registry.json").exists(); assert (root/"reports/latest_live_manual_decision_report.md").exists(); assert (root/"docs/live.html").exists(); assert (root/"reports/manual_logs").exists(); assert 'href="live.html"' in (root/"docs/index.html").read_text(encoding="utf-8"); p=json.loads(rp.read_text(encoding="utf-8")); assert p["meta"]["version"]=="2.0"; assert p["meta"]["is_trade_signal"] is False; assert p["auto_order_enabled"] is False; assert p["broker_api_enabled"] is False; assert p["formal_signal_enabled"] is False; assert p["live_manual_decision_quality"]["status"] in {"PASS","WARN"}
