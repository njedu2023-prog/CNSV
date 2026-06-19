from __future__ import annotations

import pandas as pd


def latest_trade_date(calendar: pd.DataFrame) -> str:
    if calendar.empty:
        return ""
    column = "trade_date" if "trade_date" in calendar.columns else calendar.columns[0]
    return str(calendar[column].max())
