"""Search arXiv math categories (math.AG, math.NT, math.PR, ...).

Queries the arXiv Atom API when network is available; returns structured
metadata. Falls back to an empty list (with a note) when offline.
"""

from __future__ import annotations

import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

ARXIV_API = "http://export.arxiv.org/api/query"

ARXIV_CATEGORIES = [
    "math.AG", "math.AT", "math.AP", "math.CT", "math.CA", "math.CO",
    "math.AC", "math.CV", "math.DG", "math.DS", "math.FA", "math.GM",
    "math.GN", "math.GT", "math.GR", "math.HO", "math.IT", "math.KT",
    "math.LO", "math.MP", "math.MG", "math.NT", "math.NA", "math.OA",
    "math.OC", "math.PR", "math.QA", "math.RT", "math.RA", "math.SP",
    "math.ST", "math.SG",
]

NS = {"a": "http://www.w3.org/2005/Atom"}


def arxiv_search(query: str, max_results: int = 5, category: str | None = None) -> list[dict[str, Any]]:
    """Search arXiv. Returns a list of {title, authors, abstract, url, id}."""
    q = query
    if category:
        q = f"cat:{category} AND all:{query}"
    url = ARXIV_API + "?search_query=" + urllib.parse.quote(q) + f"&max_results={max_results}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mathematics-AI/0.1"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml = resp.read().decode("utf-8")
        return _parse_arxiv_xml(xml)
    except Exception as exc:
        return [{"error": f"arXiv search unavailable: {exc}"}]


def _parse_arxiv_xml(xml: str) -> list[dict[str, Any]]:
    root = ET.fromstring(xml)
    out = []
    for entry in root.findall("a:entry", NS):
        authors = [a.find("a:name", NS).text for a in entry.findall("a:author", NS) if a.find("a:name", NS) is not None]
        out.append({
            "id": entry.find("a:id", NS).text if entry.find("a:id", NS) is not None else "",
            "title": (entry.find("a:title", NS).text or "").strip() if entry.find("a:title", NS) is not None else "",
            "authors": authors,
            "abstract": (entry.find("a:summary", NS).text or "").strip() if entry.find("a:summary", NS) is not None else "",
            "published": entry.find("a:published", NS).text if entry.find("a:published", NS) is not None else "",
        })
    return out


__all__ = ["arxiv_search", "ARXIV_CATEGORIES"]
