from cnsv.trading.evidence_loader import load_trading_evidence
from cnsv.trading.fusion import build_trading_decision_payload
from cnsv.trading.report import build_trading_html
from cnsv.utils.io import repo_root


def test_trading_html_is_chinese_dashboard():
    html = build_trading_html(build_trading_decision_payload(load_trading_evidence(repo_root())))

    assert "CNSV V3.0 交易决策系统" in html
    assert "今日决策" in html
    assert "建议仓位" in html
    assert "风险调整 EV" in html
    assert "模型表现追踪" in html
    assert "历史统计线" in html
    assert "实盘统计线" in html
    assert "暂无样本" in html
    assert "实盘统计线样本仍然较少" not in html
    assert "不自动下单" in html
