"""Search MathSciNet and zbMATH databases.

These databases require institutional subscriptions and have no public API.
This module performs a best-effort lookup via the public HTML search pages and
parses the results. When network access is unavailable (or the request fails),
it returns an empty result list so callers can degrade gracefully.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from typing import Any

USER_AGENT = "MathematicsAI/0.1 (research; contact: local)"

# Known public search endpoints (HTML scraping, best-effort)
MATHSCINET_URL = "https://mathscinet.ams.org/mathscinet/search/publications"
ZBMATH_URL = "https://zbmath.org/"


def search_mathscinet(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    """Best-effort MathSciNet search (requires subscription; may return [])."""
    return _search(MATHSCINET_URL, {"req": query}, max_results)


def search_zbmath(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    """Best-effort zbMATH search via the public HTML interface."""
    return _search(ZBMATH_URL, {"q": query}, max_results)


def _search(base_url: str, params: dict[str, str], max_results: int) -> list[dict[str, Any]]:
    try:
        qs = urllib.parse.urlencode(params)
        url = f"{base_url}?{qs}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:  # network unavailable or blocked
        return [{"error": f"search unavailable: {e}", "available": False}]
    return _parse_html(html, max_results)


def _parse_html(html: str, max_results: int) -> list[dict[str, Any]]:
    """Extract title snippets from search-result HTML."""
    results: list[dict[str, Any]] = []
    for title in re.findall(r"<a[^>]*class=\"[^\"]*title[^\"]*\"[^>]*>(.*?)</a>", html, re.DOTALL)[:max_results]:
        clean = re.sub(r"<[^>]+>", "", title).strip()
        if clean:
            results.append({"title": clean})
    return results


def search_all(query: str, max_results: int = 5) -> dict[str, list[dict[str, Any]]]:
    """Run MathSciNet + zbMATH searches and return both result sets."""
    return {
        "mathscinet": search_mathscinet(query, max_results),
        "zbmath": search_zbmath(query, max_results),
    }


__all__ = ["search_mathscinet", "search_zbmath", "search_all"]
