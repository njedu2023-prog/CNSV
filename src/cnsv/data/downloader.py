from __future__ import annotations

import io
import time
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import pandas as pd
import requests

DEFAULT_TIMEOUT = 30
DEFAULT_ATTEMPTS = 3
NO_CACHE_HEADERS = {
    "Cache-Control": "no-cache, no-store, max-age=0",
    "Pragma": "no-cache",
    "User-Agent": "CNSV-data-fetch/1.0",
}


def _get(url: str, timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
    last_error: requests.RequestException | None = None
    for attempt in range(1, DEFAULT_ATTEMPTS + 1):
        try:
            response = requests.get(
                _cache_busted_url(url),
                timeout=timeout,
                headers=NO_CACHE_HEADERS,
            )
            response.raise_for_status()
            return response
        except requests.RequestException as exc:
            last_error = exc
            if attempt < DEFAULT_ATTEMPTS:
                time.sleep(2 ** (attempt - 1))
    raise RuntimeError(
        f"failed to fetch URL {url} after {DEFAULT_ATTEMPTS} attempts: {last_error}"
    ) from last_error


def _cache_busted_url(url: str) -> str:
    parts = urlsplit(url)
    if parts.hostname not in {"raw.githubusercontent.com", "githubusercontent.com"}:
        return url
    query = parse_qsl(parts.query, keep_blank_values=True)
    query.append(("cnsv_cache_bust", str(time.time_ns())))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def fetch_text(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    return _get(url, timeout=timeout).text


def fetch_json(url: str, timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    try:
        payload = _get(url, timeout=timeout).json()
    except ValueError as exc:
        raise RuntimeError(f"failed to decode JSON from URL {url}: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"JSON URL {url} did not return an object")
    return payload


def fetch_parquet(url: str, timeout: int = DEFAULT_TIMEOUT) -> pd.DataFrame:
    response = _get(url, timeout=timeout)
    try:
        return pd.read_parquet(io.BytesIO(response.content))
    except Exception as exc:
        raise RuntimeError(f"failed to read parquet from URL {url}: {exc}") from exc
