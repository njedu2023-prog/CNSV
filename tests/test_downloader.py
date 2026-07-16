import requests

from cnsv.data import downloader


class _Response:
    text = "ok"

    def raise_for_status(self):
        return None


def test_raw_github_fetch_bypasses_cache_and_retries(monkeypatch):
    calls = []
    monkeypatch.setattr(downloader.time, "sleep", lambda value: None)

    def get(url, timeout, headers):
        calls.append((url, timeout, headers))
        if len(calls) < 3:
            raise requests.ConnectionError("temporary")
        return _Response()

    monkeypatch.setattr(downloader.requests, "get", get)

    assert downloader.fetch_text("https://raw.githubusercontent.com/acme/repo/main/data.json") == "ok"
    assert len(calls) == 3
    assert all("cnsv_cache_bust=" in url for url, _, _ in calls)
    assert all(headers["Cache-Control"].startswith("no-cache") for _, _, headers in calls)


def test_non_github_url_is_not_rewritten(monkeypatch):
    calls = []

    def get(url, timeout, headers):
        calls.append(url)
        return _Response()

    monkeypatch.setattr(downloader.requests, "get", get)

    downloader.fetch_text("https://example.com/data.json")

    assert calls == ["https://example.com/data.json"]
