from cnsv.trading.evidence_loader import load_trading_evidence
from cnsv.trading.fusion import build_trading_decision_payload
from cnsv.trading.report import build_trading_html
from cnsv.utils.io import repo_root


def test_trading_html_is_chinese_dashboard():
    html = build_trading_html(build_trading_decision_payload(load_trading_evidence(repo_root())))
    nav = html.split('<nav class="topnav"', 1)[1].split("</nav>", 1)[0]

    assert "CNSV V3.0 交易决策系统" in html
    assert "今日决策" in html
    assert "信号生成日" in html
    assert "预测日" in html
    assert "数据交易日" in html
    assert 'aria-label="交易决策日期表"' in html
    assert "收盘数据日" in html
    assert "最新收盘价" in html
    assert "收盘涨跌幅" in html
    assert 'aria-label="收盘数据表"' in html
    assert "43.13 亿" in html
    assert ".eyebrow{color:var(--red)" in html
    assert 'aria-label="概率判断表"' in html
    assert "5D / 10D / 20D 价格预测分布" in html
    assert "5D 预测分布" in html
    assert "10D 预测分布" in html
    assert "20D 预测分布" in html
    assert 'aria-label="5D 价格预测分布表"' in html
    assert 'aria-label="10D 价格预测分布表"' in html
    assert 'aria-label="20D 价格预测分布表"' in html
    assert html.index("今日决策") < html.index("5D / 10D / 20D 价格预测分布") < html.index("概率判断")
    assert "交易决策" in nav
    assert "V3.0 交易决策" not in nav
    assert "V1.2" not in nav
    assert "V1.3" not in nav
    assert "V2.0" not in nav
    assert "data/latest_data_report.json" not in nav
    assert "人工执行量化交易决策参考。不自动下单，不连接券商接口。" not in html
    assert "主线看板" not in html
    assert "V2.0 人工决策" not in html
    assert "原始 JSON" not in html
    assert "建议仓位" in html
    assert "风险调整 EV" in html
    assert "模型表现追踪" in html
    assert "历史统计线" in html
    assert "实盘统计线" in html
    assert "暂无样本" in html
    assert "实盘统计线样本仍然较少" not in html
    assert "自动下单" in html
