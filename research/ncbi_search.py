"""Entrez API integration for GenBank, PubMed, and GEO.

Uses Biopython's Entrez module when available and an API key is configured.
Falls back to informative offline guidance when no network/key is present.
"""
from __future__ import annotations

import json
from pathlib import Path

try:
    from Bio import Entrez  # type: ignore
    _HAS_ENTREZ = True
except Exception:
    _HAS_ENTREZ = False


class NCBISearch:
    def __init__(self, email: str = "biology-ai@example.com", api_key: str = ""):
        self.email = email
        self.api_key = api_key
        if _HAS_ENTREZ:
            Entrez.email = email
            if api_key:
                Entrez.api_key = api_key
        self.available = _HAS_ENTREZ and bool(api_key)

    def search_pubmed(self, query: str, max_results: int = 10) -> dict:
        if not self.available:
            return _offline("PubMed search", query, max_results)
        try:
            handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
            result = Entrez.read(handle)
            handle.close()
            return {"db": "pubmed", "query": query,
                    "ids": list(result.get("IdList", [])),
                    "count": int(result.get("Count", 0))}
        except Exception as e:
            return {"db": "pubmed", "query": query, "error": str(e)}

    def fetch_genbank(self, accession: str) -> dict:
        if not self.available:
            return _offline("GenBank fetch", accession, 1)
        try:
            handle = Entrez.efetch(db="nuccore", id=accession, rettype="gb", retmode="text")
            text = handle.read()
            handle.close()
            return {"accession": accession, "format": "genbank", "length": len(text)}
        except Exception as e:
            return {"accession": accession, "error": str(e)}

    def search_geo(self, query: str, max_results: int = 10) -> dict:
        if not self.available:
            return _offline("GEO search", query, max_results)
        try:
            handle = Entrez.esearch(db="gds", term=query, retmax=max_results)
            result = Entrez.read(handle)
            handle.close()
            return {"db": "GEO", "query": query,
                    "ids": list(result.get("IdList", []))}
        except Exception as e:
            return {"db": "GEO", "query": query, "error": str(e)}

    @staticmethod
    def status() -> dict:
        return {"biopython_entrez": _HAS_ENTREZ,
                "note": "Set api_keys.json ncbi_api_key to enable live queries."}


def _offline(operation, query, n):
    return {"operation": operation, "query": query,
            "status": "offline",
            "note": "No NCBI API key configured. Configure config/api_keys.json "
                    "with ncbi_email and ncbi_api_key to enable live Entrez queries."}
