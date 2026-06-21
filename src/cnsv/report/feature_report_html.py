from __future__ import annotations

from pathlib import Path

from cnsv.utils.io import ensure_parent

HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CNSV V3.0 主线决策网站</title>
  <style>
    :root{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Microsoft YaHei",sans-serif;color:#1d1d1f;background:#f5f5f7;--line:#d2d2d7;--muted:#6e6e73;--blue:#06c;--surface:#fff;--shadow:0 18px 42px rgba(0,0,0,.07)}
    *{box-sizing:border-box}body{margin:0;background:#f5f5f7;-webkit-font-smoothing:antialiased}.topbar{position:fixed;top:0;left:0;right:0;z-index:20;background:rgba(0,0,0,.88);backdrop-filter:saturate(180%) blur(18px);border-bottom:1px solid rgba(255,255,255,.16)}.nav{display:flex;gap:2px;overflow-x:auto;white-space:nowrap;justify-content:center;padding:10px 18px}.nav a{color:#fff;text-decoration:none;font-size:12px;line-height:1.2;padding:4px 10px;border-radius:999px;opacity:.78}.nav a:hover,.nav a.active{color:#fff;opacity:1}.nav a.active{font-weight:600;background:rgba(255,255,255,.12)}.shell{width:min(1280px,100%);margin:0 auto;padding:58px 20px 18px}.frame-card{background:var(--surface);border-radius:22px;box-shadow:var(--shadow);overflow:hidden;border:1px solid rgba(0,0,0,.04)}.frame-head{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 16px;border-bottom:1px solid #e8e8ed;color:var(--muted);font-size:12px}.frame-title{color:#1d1d1f;font-weight:600}iframe{display:block;width:100%;height:calc(100vh - 110px);min-height:680px;border:0;background:#fff}.note{color:var(--muted);font-size:12px;text-align:center;margin-top:10px}@media(max-width:760px){.nav{justify-content:flex-start}.shell{padding:54px 10px 14px}.frame-card{border-radius:16px}iframe{height:calc(100vh - 104px);min-height:600px}}
  </style>
</head>
<body>
  <div class="topbar">
    <nav class="nav" aria-label="CNSV 全量菜单">
      <a href="trading.html" class="active">V3.0 交易决策</a>
      <a href="data/latest_data_report.json">数据状态</a>
      <a href="data/latest_feature_report.json">核心特征</a>
      <a href="baseline.html">V1.2 基准模型</a>
      <a href="validation.html">V1.2.2 验证</a>
      <a href="path.html">V1.3 路径分布</a>
      <a href="backtest.html">V1.4 观察级回测</a>
      <a href="decision_support.html">V1.5 人工决策辅助</a>
      <a href="risk.html">V1.6 风控解释</a>
      <a href="live.html">V2.0 实盘人工决策</a>
    </nav>
  </div>
  <main class="shell">
    <section class="frame-card">
      <div class="frame-head"><span class="frame-title" id="frameTitle">V3.0 交易决策</span><span>当前页打开</span></div>
      <iframe id="contentFrame" title="CNSV 内容页" src="trading.html"></iframe>
    </section>
    <p class="note">若浏览器缓存旧页面，请刷新或在 URL 后追加 ?v=site-20260621c。</p>
  </main>
  <script>
    const links=[...document.querySelectorAll('.nav a')];
    const frame=document.getElementById('contentFrame');
    const title=document.getElementById('frameTitle');
    links.forEach(link=>link.addEventListener('click',event=>{event.preventDefault();links.forEach(a=>a.classList.toggle('active',a===link));title.textContent=link.textContent.trim();frame.src=link.getAttribute('href');history.replaceState(null,'','#'+encodeURIComponent(link.getAttribute('href')));}));
    const initial=decodeURIComponent(location.hash.slice(1)||'trading.html');
    const selected=links.find(a=>a.getAttribute('href')===initial);
    if(selected){selected.click();}
  </script>
</body>
</html>
"""


def write_feature_report_html(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(HTML, encoding="utf-8")
    return target
