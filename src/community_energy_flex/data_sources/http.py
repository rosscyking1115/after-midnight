"""Shared HTTP helper for the data-source clients - one place for the GET
boilerplate (headers, timeout, JSON decode)."""

from __future__ import annotations

import json
from urllib.request import Request, urlopen

USER_AGENT = "after-midnight/0.1 (+https://github.com)"


def get_json(url: str, timeout: int = 20) -> dict:
    req = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:  # noqa: S310 - fixed https hosts
        return json.loads(resp.read().decode("utf-8"))
