from __future__ import annotations

from pathlib import Path

from cnsv.report.feature_report_html import HTML, write_feature_report_html


def write_report_html(path: str | Path) -> Path:
    return write_feature_report_html(path)
