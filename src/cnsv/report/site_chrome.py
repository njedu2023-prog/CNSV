from __future__ import annotations

import re


GLOBAL_NAV_ITEMS = [
    ("trading.html", "交易决策", "trading"),
    ("index.html#coverage", "数据状态", "index"),
    ("index.html#priceVolumeCards", "核心特征", "index"),
    ("baseline.html", "基准模型", "baseline"),
    ("validation.html", "基准验证", "validation"),
    ("path.html", "路径分布", "path"),
    ("backtest.html", "观察回测", "backtest"),
    ("decision_support.html", "人工辅助", "decision_support"),
    ("risk.html", "风控解释", "risk"),
    ("live.html", "人工确认", "live"),
]

PAGE_EYEBROWS = {
    "index": "CNSV V3.0 交易决策系统",
    "baseline": "CNSV V3.0 交易决策系统",
    "validation": "CNSV V3.0 交易决策系统",
    "path": "CNSV V3.0 交易决策系统",
    "backtest": "CNSV V3.0 交易决策系统",
    "decision_support": "CNSV V3.0 交易决策系统",
    "risk": "CNSV V3.0 交易决策系统",
    "live": "CNSV V3.0 交易决策系统",
    "trading": "CNSV V3.0 交易决策系统",
}

GLOBAL_HEADER_HTML = """
  <header class="site-hero">
    <p class="eyebrow">CNSV V3.0 交易决策系统</p>
    <h1>中国船舶 600150.SH</h1>
  </header>
"""


GLOBAL_CHROME_CSS = """
    body { padding-top: 48px; }
    .topbar {
      position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
      background: rgba(0,0,0,.88); backdrop-filter: saturate(180%) blur(18px);
      border-bottom: 1px solid rgba(255,255,255,.16);
    }
    .topnav {
      display: flex; justify-content: center; gap: 2px; flex-wrap: nowrap;
      overflow-x: auto; white-space: nowrap; padding: 9px 18px;
      -webkit-overflow-scrolling: touch;
    }
    .topnav a {
      border: 0; border-radius: 999px; background: transparent; color: #fff;
      text-decoration: none; padding: 4px 10px; font-size: 12px;
      line-height: 1.2; white-space: nowrap; opacity: .78;
    }
    .topnav a:hover,
    .topnav a.active { color: #fff; opacity: 1; }
    .topnav a.active { font-weight: 600; background: rgba(255,255,255,.12); }
    .global-nav { display: none !important; }
    header nav { display: none !important; }
    main { padding-top: 26px !important; }
    header, .site-hero { text-align: center !important; padding: 16px 0 20px !important; }
    header .eyebrow,
    .site-hero .eyebrow,
    .hero .eyebrow {
      color: #d70015 !important; font-size: 12px !important; font-weight: 700 !important;
      letter-spacing: .08em !important; margin: 0 0 5px !important;
    }
    h1 { font-size: 30px !important; letter-spacing: 0 !important; margin: 5px 0 8px !important; }
    h2 { font-size: 14px !important; letter-spacing: 0 !important; }
    header .subtitle { display: none !important; }
    .metric { padding: 10px 12px !important; }
    .value { font-size: 13px !important; line-height: 1.26 !important; }
    .label, .chip, table { font-size: 12px !important; }
    section { margin: 12px 0 !important; padding: 18px 22px !important; }
    @media (max-width: 760px) {
      body { padding-top: 50px; }
      .topnav { justify-content: flex-start; }
      main { padding-left: 14px !important; padding-right: 14px !important; }
      h1 { font-size: 24px !important; }
      section { padding: 16px !important; }
    }
"""


def site_nav(active: str) -> str:
    links = []
    for href, label, key in GLOBAL_NAV_ITEMS:
        cls = ' class="active"' if key == active else ""
        links.append(f'<a href="{href}"{cls}>{label}</a>')
    return f'<div class="topbar"><nav class="topnav" aria-label="CNSV 全量菜单">{"".join(links)}</nav></div>'


def _normalize_header(html: str, active: str) -> str:
    del active
    if re.search(r"<header\b", html, flags=re.S):
        return re.sub(r"<header\b[^>]*>.*?</header>", GLOBAL_HEADER_HTML, html, count=1, flags=re.S)
    return re.sub(r"<main\b[^>]*>", lambda match: f"{match.group(0)}\n{GLOBAL_HEADER_HTML}", html, count=1, flags=re.S)


def apply_site_chrome(html: str, active: str) -> str:
    html = re.sub(
        r"<title>.*?</title>",
        "<title>CNSV V3.0 交易决策系统</title>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(r"\s*<nav class=\"global-nav\">.*?</nav>", "", html, flags=re.S)
    html = re.sub(r"\s*<div class=\"topbar\">.*?</div>", "", html, flags=re.S)
    html = re.sub(r"(<body\b[^>]*>)", rf"\1\n{site_nav(active)}", html, count=1, flags=re.S)
    if ".topbar {" not in html or ".site-hero" not in html:
        html = html.replace("</style>", f"{GLOBAL_CHROME_CSS}\n  </style>", 1)
    return _normalize_header(html, active)
