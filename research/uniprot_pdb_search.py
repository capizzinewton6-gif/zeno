"""Search protein sequence and structure databases (UniProt, PDB)."""
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request

UNIPROT_SEARCH_URL = "https://rest.uniprot.org/uniprotkb/search"
PDB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"


class UniProtPDBSearch:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def search_uniprot(self, query: str, max_results: int = 10) -> dict:
        params = urllib.parse.urlencode({
            "query": query, "format": "json", "size": max_results,
        })
        url = f"{UNIPROT_SEARCH_URL}?{params}"
        try:
            with urllib.request.urlopen(url, timeout=self.timeout) as r:
                data = json.loads(r.read().decode())
            return {"query": query, "n_results": data.get("results", []),
                    "count": len(data.get("results", []))}
        except (urllib.error.URLError, OSError) as e:
            return {"query": query, "status": "offline",
                    "error": str(e),
                    "note": "UniProt query requires network access."}

    def search_pdb(self, query: str, max_results: int = 10) -> dict:
        body = json.dumps({
            "query": {"type": "terminal", "service": "full_text",
                      "parameters": {"value": query}},
            "return_type": "entry", "request_options": {"results_content_type": ["experimental"],
                                                        "paginate": {"start": 0, "rows": max_results}},
        }).encode()
        req = urllib.request.Request(PDB_SEARCH_URL, data=body,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                data = json.loads(r.read().decode())
            return {"query": query, "n_results": data.get("total_count", 0),
                    "pdb_ids": [r.get("identifier") for r in data.get("result_set", [])]}
        except (urllib.error.URLError, OSError) as e:
            return {"query": query, "status": "offline", "error": str(e),
                    "note": "PDB query requires network access."}

    @staticmethod
    def status() -> dict:
        return {"note": "UniProt/PDB queries use public REST APIs; network access required."}
