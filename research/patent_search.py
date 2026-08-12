"""Search biotech and gene sequence patents."""
from __future__ import annotations

import urllib.parse
import urllib.request


PATENT_SEARCH_URLS = {
    "google_patents": "https://patents.google.com/?q={query}",
    "uspto": "https://patentscope.wipo.int/search/en/search.jsf?query={query}",
}


class PatentSearch:
    @staticmethod
    def google_patents_url(query: str) -> str:
        return PATENT_SEARCH_URLS["google_patents"].format(
            query=urllib.parse.quote(query))

    @staticmethod
    def search_summary(query: str, max_results: int = 10) -> dict:
        """Return a link and guidance; full patent parsing requires a scraper/API."""
        return {
            "query": query,
            "google_patents_url": PatentSearch.google_patents_url(query),
            "note": ("Patent full-text retrieval requires a dedicated patent API "
                     "(e.g. Google Patents Public Datasets, EPO OPS). The URL above "
                     "opens a browser search; configure an API key for automated retrieval."),
            "max_results": max_results,
        }

    @staticmethod
    def classify_patent_type(title: str) -> str:
        t = title.lower()
        if "crispr" in t or "cas9" in t or "guide rna" in t:
            return "gene editing"
        if "primer" in t or "pcr" in t:
            return "amplification"
        if "antibody" in t or "immuno" in t:
            return "immunotherapy"
        if "vector" in t or "plasmid" in t:
            return "vector construction"
        if "promoter" in t or "expression" in t:
            return "expression system"
        return "general biotech"
