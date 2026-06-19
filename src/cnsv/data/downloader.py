from __future__ import annotations

import io
from typing import Any

import pandas as pd
import requests

DEFAULT_TIMEOUT = 30


def _get(url: str, timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.RequestException as exc:
        raise RuntimeError(f"failed to fetch URL {url}: {exc}") from exc


def fetch_text(url: str) -> str:
    return _get(url).text


def fetch_json(url: str) -> dict[str, Any]:
    try:
        payload = _get(url).json()
    except ValueError as exc:
        raise RuntimeError(f"failed to decode JSON from URL {url}: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"JSON URL {url} did not return an object")
    return payload


def fetch_parquet(url: str) -> pd.DataFrame:
    response = _get(url)
    try:
        return pd.read_parquet(io.BytesIO(response.content))
    except Exception as exc:
        raise RuntimeError(f"failed to read parquet from URL {url}: {exc}") from exc
