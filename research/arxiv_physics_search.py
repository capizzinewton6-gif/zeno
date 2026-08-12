"""Search arXiv physics subcategories (hep-th, quant-ph, astro-ph, cond-mat)."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

from agents.literature_agent import LiteratureAgent


ARXIV_CATEGORIES = {
    "hep-th": "High Energy Physics - Theory",
    "hep-ph": "High Energy Physics - Phenomenology",
    "hep-ex": "High Energy Physics - Experiment",
    "hep-lat": "Lattice High Energy Physics",
    "quant-ph": "Quantum Physics",
    "astro-ph": "Astrophysics",
    "astro-ph.CO": "Cosmology and Nongalactic Astrophysics",
    "astro-ph.HE": "High Energy Astrophysical Phenomena",
    "cond-mat": "Condensed Matter",
    "gr-qc": "General Relativity and Quantum Cosmology",
    "nucl-th": "Nuclear Theory",
    "physics": "Physics (other)",
}


@dataclass
class ArxivResult:
    query: str
    category: str
    references: list[dict]
    online: bool


class ArxivPhysicsSearch(LiteratureAgent):
    """arXiv search (offline-fallback through LiteratureAgent)."""

    @staticmethod
    def url_for(query: str, category: str | None = None) -> str:
        q = quote(query)
        if category:
            return f"https://arxiv.org/list/{category}/recent"
        return f"https://arxiv.org/a/?searchtype=all&query={q}"

    def search(self, query: str, category: str | None = None, max_results: int = 5) -> ArxivResult:
        refs = LiteratureAgent.search(self, query).references[:max_results]
        cat = category or "physics"
        return ArxivResult(query=query, category=cat, references=refs, online=self.online)

    @staticmethod
    def categories() -> dict[str, str]:
        return dict(ARXIV_CATEGORIES)
