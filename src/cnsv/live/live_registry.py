from __future__ import annotations
import json
from pathlib import Path
from cnsv.live import LIVE_STAGE, LIVE_VERSION
from cnsv.live.live_evidence_loader import REQUIRED_LIVE_REPORTS
from cnsv.models.baseline_schema import FORBIDDEN_ACTIONS
from cnsv.utils.io import ensure_parent
def build_live_manual_decision_registry()->list[dict[str,object]]:
 return [{"registry_type":"live_manual_decision","version":LIVE_VERSION,"stage":LIVE_STAGE,"inputs":list(REQUIRED_LIVE_REPORTS.values()),"outputs":["latest_live_manual_decision_report.json","live_manual_decision_registry.json","latest_live_manual_decision_report.md","live.html","manual_logs"],"is_trade_signal":False,"auto_order_enabled":False,"broker_api_enabled":False,"formal_signal_enabled":False,"forbidden":FORBIDDEN_ACTIONS,"next_stage":"V2.0 acceptance and daily manual operation"}]
def write_live_manual_decision_registry(path:str|Path)->Path:
 target=ensure_parent(path); target.write_text(json.dumps(build_live_manual_decision_registry(),ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8"); return target
