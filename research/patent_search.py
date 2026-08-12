"""Patent search: search patents on facial recognition and object tracking."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Patent:
    number: str
    title: str
    assignee: str
    abstract: str
    url: str = ""


class PatentSearch:
    """Query patent sources. Uses Google Patents public search as a fallback."""

    def search(self, query: str, limit: int = 5) -> List[Patent]:
        try:
            import requests
            url = "https://patents.google.com/xhr/query"
            params = {"q": query, "exp": "", "num": str(limit)}
            resp = requests.get(url, params=params, timeout=10,
                                headers={"User-Agent": "VisionAI/1.0"})
            if resp.status_code == 200 and resp.text:
                return self._parse(resp.text, limit)
        except Exception:
            pass
        return self._fallback(query)

    @staticmethod
    def _parse(text: str, limit: int) -> List[Patent]:
        # Google Patents returns JSON-ish; do a tolerant regex scan.
        import re
        out: List[Patent] = []
        for m in re.finditer(r'"publication_number"\s*:\s*"([^"]+)".*?"title"\s*:\s*"([^"]+)"',
                             text, re.DOTALL):
            out.append(Patent(number=m.group(1), title=m.group(2),
                              assignee="", abstract="",
                              url=f"https://patents.google.com/patent/{m.group(1)}"))
            if len(out) >= limit:
                break
        return out

    @staticmethod
    def _fallback(query: str) -> List[Patent]:
        return [Patent(number="N/A", title=f"Search '{query}' on Google Patents",
                       assignee="", abstract="",
                       url=f"https://patents.google.com/?q={query.replace(' ', '+')}")]
