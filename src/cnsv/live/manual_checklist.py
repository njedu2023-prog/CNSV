from __future__ import annotations
from typing import Any
REQUIRED_MANUAL_CHECKS=[("check_data_freshness","确认数据新鲜度与最新交易日。"),("check_latest_trade_date","确认所有上游报告 latest_trade_date 一致。"),("check_path_downside","复核路径下穿概率与尾部路径风险。"),("check_drawdown_exposure","复核最大回撤分布与当前波动状态。"),("check_model_conflict","复核 B/P 模型之间的证据分歧。"),("check_p2_fallback","确认 P2 仅为辅助层并复核 fallback 风险。"),("check_evidence_conflict","复核证据冲突原因。"),("check_risk_level","确认总体风险等级与主要风险来源。"),("check_manual_notes","填写人工复核备注。"),("confirm_no_auto_order","确认系统不执行自动交易动作。")]
def build_manual_review_checklist(risk_report:dict[str,Any]|None)->list[dict[str,Any]]:
 items=[{"id":i,"text":t,"required":True,"status":"pending"} for i,t in REQUIRED_MANUAL_CHECKS]; known={x["id"] for x in items}
 for r in (risk_report or {}).get("risk_review_checklist") or []:
  item_id=str(r.get("id") or "")
  if item_id and item_id not in known: items.append({"id":item_id,"text":r.get("text",item_id),"required":True,"status":"pending"}); known.add(item_id)
 return items
