from __future__ import annotations

import re


GLOBAL_NAV_ITEMS = [
    ("index.html#coverage", "数据状态", "index"),
    ("index.html#priceVolumeCards", "核心特征", "index"),
    ("baseline.html", "基准模型", "baseline"),
    ("validation.html", "基准验证", "validation"),
    ("path.html", "路径分布", "path"),
    ("backtest.html", "观察回测", "backtest"),
    ("decision_support.html", "人工辅助", "decision_support"),
    ("risk.html", "风控解释", "risk"),
    ("live.html", "人工确认", "live"),
    ("trading.html", "交易决策", "trading"),
]


GLOBAL_CHROME_CSS = """
    body { padding-top: 48px; }
    .global-nav {
      position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
      display: flex; justify-content: center; gap: 2px; flex-wrap: nowrap;
      overflow-x: auto; padding: 9px max(14px, env(safe-area-inset-left));
      background: rgba(251,251,253,.82); backdrop-filter: saturate(180%) blur(18px);
      border-bottom: 1px solid rgba(0,0,0,.08);
      -webkit-overflow-scrolling: touch;
    }
    .global-nav a {
      border: 0; border-radius: 0; background: transparent; color: #1d1d1f;
      text-decoration: none; padding: 4px 10px; font-size: 12px;
      line-height: 1.2; white-space: nowrap; opacity: .82;
    }
    .global-nav a:hover { color: #06c; opacity: 1; }
    .global-nav a.active { color: #06c; font-weight: 600; opacity: 1; }
    header nav:not(.global-nav) { display: none; }
    main { padding-top: 26px !important; }
    header { padding-top: 10px !important; padding-bottom: 18px !important; }
    section { margin: 12px 0 !important; padding: 18px 22px !important; }
    h1 { font-size: 20px !important; letter-spacing: 0 !important; }
    h2 { font-size: 14px !important; letter-spacing: 0 !important; }
    .subtitle { font-size: 13px !important; line-height: 1.42 !important; }
    .metric { padding: 10px 12px !important; }
    .value { font-size: 13px !important; line-height: 1.26 !important; }
    .label, .chip, table { font-size: 12px !important; }
    @media (max-width: 760px) {
      body { padding-top: 50px; }
      .global-nav { justify-content: flex-start; }
      main { padding-left: 14px !important; padding-right: 14px !important; }
      section { padding: 16px !important; }
    }
"""


def site_nav(active: str) -> str:
    links = []
    for href, label, key in GLOBAL_NAV_ITEMS:
        cls = ' class="active"' if key == active else ""
        links.append(f'<a href="{href}"{cls}>{label}</a>')
    return f'<nav class="global-nav">{"".join(links)}</nav>'


def apply_site_chrome(html: str, active: str) -> str:
    if "class=\"global-nav\"" not in html:
        html = html.replace("<body>", f"<body>\n{site_nav(active)}", 1)
        html = html.replace("<body><main>", f"<body>\n{site_nav(active)}\n<main>", 1)
    if ".global-nav" not in html:
        html = html.replace("</style>", f"{GLOBAL_CHROME_CSS}\n  </style>", 1)
    return re.sub(r"<header>\s*<nav\b.*?</nav>\s*</header>", lambda m: m.group(0), html, count=1, flags=re.S)
