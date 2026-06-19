from __future__ import annotations

from pathlib import Path

from cnsv.utils.io import ensure_parent

HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CNSV Data Status</title>
  <style>
    :root { color-scheme: light; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    body { margin: 0; background: #f5f7fa; color: #18212f; }
    main { max-width: 1120px; margin: 0 auto; padding: 28px 18px 42px; }
    h1 { font-size: 28px; margin: 0 0 18px; letter-spacing: 0; }
    h2 { font-size: 18px; margin: 0 0 12px; }
    section { background: #fff; border: 1px solid #d8dee8; border-radius: 8px; padding: 16px; margin: 14px 0; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 10px; }
    .metric { border: 1px solid #e3e7ee; border-radius: 6px; padding: 10px; background: #fbfcfe; }
    .label { color: #5f6b7a; font-size: 12px; }
    .value { font-size: 18px; font-weight: 650; margin-top: 4px; overflow-wrap: anywhere; }
    pre { white-space: pre-wrap; background: #101828; color: #eef4ff; border-radius: 8px; padding: 12px; overflow: auto; }
  </style>
</head>
<body>
<main>
  <h1>CNSV Data Status</h1>
  <section><h2>Gate</h2><div id="gate" class="grid"></div></section>
  <section><h2>Loaded Data</h2><div id="loaded" class="grid"></div></section>
  <section><h2>Features</h2><pre id="features">Loading...</pre></section>
  <section><h2>Forbidden Actions</h2><pre id="forbidden">Loading...</pre></section>
</main>
<script>
function metric(label, value) {
  return `<div class="metric"><div class="label">${label}</div><div class="value">${value ?? ""}</div></div>`;
}
fetch("data/latest_data_report.json")
  .then(r => r.json())
  .then(data => {
    const gate = data.cnsvdata_gate || {};
    const loaded = data.loaded_data_summary || {};
    document.getElementById("gate").innerHTML = [
      metric("ready", gate.ready),
      metric("status", gate.status),
      metric("can_continue", gate.can_continue),
      metric("formal_signal", false),
      metric("latest_trade_date", (data.data_manifest || {}).latest_trade_date)
    ].join("");
    document.getElementById("loaded").innerHTML = [
      metric("daily_rows", loaded.daily_rows),
      metric("one_min_rows", loaded.one_min_rows),
      metric("moneyflow_rows", loaded.moneyflow_rows)
    ].join("");
    document.getElementById("features").textContent = JSON.stringify(data.features || {}, null, 2);
    document.getElementById("forbidden").textContent = JSON.stringify(data.forbidden_actions || [], null, 2);
  })
  .catch(err => {
    document.getElementById("features").textContent = `Failed to load data/latest_data_report.json: ${err}`;
  });
</script>
</body>
</html>
"""


def write_report_html(path: str | Path) -> Path:
    target = ensure_parent(path)
    target.write_text(HTML, encoding="utf-8")
    return target
