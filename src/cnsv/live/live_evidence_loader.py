from __future__ import annotations
import json
from pathlib import Path
from typing import Any
REQUIRED_LIVE_REPORTS={"data_report":"latest_data_report.json","feature_report":"latest_feature_report.json","baseline_model_report":"latest_baseline_model_report.json","baseline_validation_report":"latest_baseline_validation_report.json","path_distribution_report":"latest_path_distribution_report.json","path_validation_report":"latest_path_validation_report.json","observation_backtest_report":"latest_observation_backtest_report.json","human_decision_support_report":"latest_human_decision_support_report.json","risk_explanation_report":"latest_risk_explanation_report.json"}
QUALITY_KEYS={"data_report":"validation","feature_report":"feature_quality","baseline_model_report":"baseline_quality","baseline_validation_report":"baseline_validation_quality","path_distribution_report":"path_quality","path_validation_report":"path_validation_quality","observation_backtest_report":"observation_backtest_quality","human_decision_support_report":"human_decision_support_quality","risk_explanation_report":"risk_explanation_quality"}
def load_live_evidence(root:str|Path)->dict[str,Any]:
 data_dir=Path(root)/"docs"/"data"; reports={}; av={"all_required_available":True,"available_reports":[],"missing_reports":[],"failed_quality_gates":[],"warning_quality_gates":[],"stale_evidence":[],"reports":{}}; dates={}
 for key,fn in REQUIRED_LIVE_REPORTS.items():
  path=data_dir/fn
  if not path.exists():
   av["all_required_available"]=False; av["missing_reports"].append(key); av["reports"][key]={"available":False,"path":str(path),"reason":"missing_report"}; reports[key]=None; continue
  try: report=json.loads(path.read_text(encoding="utf-8"))
  except json.JSONDecodeError as exc:
   av["all_required_available"]=False; av["missing_reports"].append(key); av["reports"][key]={"available":False,"path":str(path),"reason":f"invalid_json: {exc}"}; reports[key]=None; continue
  reports[key]=report; status=quality_status(report,QUALITY_KEYS[key]); tdate=latest_trade_date(report)
  if tdate!="N/A": dates[key]=tdate
  if status=="FAIL": av["failed_quality_gates"].append({"report":key,"quality_key":QUALITY_KEYS[key],"path":str(path)})
  elif status=="WARN": av["warning_quality_gates"].append({"report":key,"quality_key":QUALITY_KEYS[key],"path":str(path)})
  av["available_reports"].append(key); av["reports"][key]={"available":True,"path":str(path),"quality_status":status,"latest_trade_date":tdate}
 if len(set(dates.values()))>1: av["stale_evidence"].append({"reason":"latest_trade_date_mismatch","dates":dates})
 av["all_required_available"]=av["all_required_available"] and not av["missing_reports"]
 return {"reports":reports,"live_decision_evidence_availability":av}
def quality_status(report:dict[str,Any]|None,key:str)->str:
 if not isinstance(report,dict): return "MISSING"
 if key=="validation": return str((report.get("validation") or report.get("data_quality") or {}).get("status") or "N/A")
 return str((report.get(key) or {}).get("status") or "N/A")
def latest_trade_date(report:dict[str,Any]|None)->str:
 if not isinstance(report,dict): return "N/A"
 meta=report.get("meta") or {}; manifest=report.get("data_manifest") or {}; overview=report.get("live_state_overview") or {}
 return str(meta.get("latest_trade_date") or manifest.get("latest_trade_date") or overview.get("latest_trade_date") or "N/A")
