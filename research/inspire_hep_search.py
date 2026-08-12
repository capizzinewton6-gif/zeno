"""Search INSPIRE-HEP database for high-energy physics literature."""

from __future__ import annotations

from urllib.parse import quote

from agents.literature_agent import LiteratureAgent


class InspireHepSearch(LiteratureAgent):
    """INSPIRE-HEP search (offline fallback via LiteratureAgent)."""

    @staticmethod
    def url_for(query: str) -> str:
        return f"https://inspirehep.net/api/literature?q={quote(query)}"

    def search(self, query: str, max_results: int = 5):
        return LiteratureAgent.search(self, query).references[:max_results]
