"""Search NASA/ADS for astrophysics and planetary literature."""

from __future__ import annotations

from urllib.parse import quote

from agents.literature_agent import LiteratureAgent


class AdsSearch(LiteratureAgent):
    """NASA ADS search (offline fallback via LiteratureAgent)."""

    @staticmethod
    def url_for(query: str) -> str:
        return f"https://ui.adsabs.harvard.edu/search/q={quote(query)}"

    def search(self, query: str, max_results: int = 5):
        refs = LiteratureAgent.search(self, query).references[:max_results]
        return refs
