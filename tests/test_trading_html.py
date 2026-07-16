# This test keeps the live trading page freshness contract covered by CI.

from cnsv.trading.evidence_loader import load_trading_evidence
from cnsv.trading.fusion import build_trading_decision_payload
from cnsv.trading.live_html import build_live_trading_html
from cnsv.utils.io import repo_root


def test_trading_html_is_chinese_dashboard():
    html = build_live_trading_html(build_trading_decision_payload(load_trading_evidence(repo_root())))
    nav = html.split('<nav class="topnav"', 1)[1].split("</nav>", 1)[0]

    assert "CNSV V3.0 交易决策系统" in html
    assert "今日有效决策" in html
    assert "data/latest_trading_decision_report.json" in html
    assert "Date.now()" in html
    assert 'cache: "no-store"' in html
    assert "function render(payload)" in html
    assert "数据交易日（T）" in html
    assert "决策适用日（T+1）" in html
    assert "验证日（T+1 收盘）" in html
    assert "生成时间（北京时间）" in html
    assert 'aria-label="交易决策日期表"' in html
    assert "收盘数据日" in html
    assert "最新收盘价" in html
    assert "收盘涨跌幅" in html
    assert 'aria-label="收盘数据表"' in html
    assert html.count('class="timeline-table pair-table"') == 2
    assert ".pair-table tr{display:grid;grid-template-columns:max-content minmax(0,1fr) max-content minmax(0,1fr)" in html
    assert '.pair-table th::after{content:"："}' in html
    assert ".pair-table td{padding-left:6px" in html
    assert "成交额" in html
    assert " 亿" in html
    assert ".eyebrow{color:var(--red)" in html
    assert 'aria-label="概率判断表"' in html
    assert "5D / 10D / 20D 价格预测分布" in html
    assert '${label} 预测分布' in html
    assert 'aria-label="${label} 价格预测分布表"' in html
    assert html.index("检查决策有效期") < html.index("5D / 10D / 20D 价格预测分布") < html.index("<section><h2>T+1 涨跌预测")
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
    assert "T+1 扩展窗口" in html
    assert "实盘统计线" in html
    assert "暂无样本" in html
    assert "实盘统计线样本仍然较少" not in html
    assert "自动下单" in html
    assert 'const BEIJING_TIMEZONE = "Asia/Shanghai"' in html
    assert "function freshnessState(payload" in html
    assert "上一交易日决策（已失效）" in html
    assert "STALE" in html
    assert "setInterval(loadLatest, REFRESH_INTERVAL_MS)" in html
    assert "visibilitychange" in html
    assert "每日 20:04 自动更新" in html
    assert 'document.getElementById("priceDistribution").innerHTML' in html
    assert 'document.getElementById("priceDistribution").outerHTML' not in html
    assert "2026-06-25T" not in html
    assert "最新收盘价</th><td>35." not in html


def test_trading_workflows_delegate_pages_to_single_refresh_workflow():
    root = repo_root()
    for path in [
        root / ".github/workflows/run_trading_decision.yml",
        root / ".github/workflows/run_mainline_daily.yml",
    ]:
        text = path.read_text(encoding="utf-8")
        assert "actions/upload-pages-artifact@v3" not in text
        assert "actions/deploy-pages@v4" not in text

    refresh = (root / ".github/workflows/deploy_pages_refresh.yml").read_text(encoding="utf-8")
    assert "pages: write" in refresh
    assert "id-token: write" in refresh
    assert "actions/upload-pages-artifact@v3" in refresh
    assert "actions/deploy-pages@v4" in refresh
    assert "cancel-in-progress: true" in refresh
    assert "Check whether reports changed" in refresh
