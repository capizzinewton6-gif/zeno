"""Patent search — search chemical composition and process patents.

Provides a structure for patent queries. Live patent DB access requires an
API key (e.g., EPO OPS, USPTO PatentsView); falls back gracefully.
"""

import json
import logging
import urllib.parse
import urllib.request

logger = logging.getLogger(__name__)

PATENTSVIEW = "https://api.patentsview.org/patents/query"


class PatentSearch:
    """Query patent databases."""

    def search_uspto(self, query_text, limit=5):
        """Search USPTO PatentsView by keyword (network-dependent)."""
        body = {
            "q": {"_text": {"_all_words": query_text}},
            "f": ["patent_number", "patent_title", "patent_date", "assignee_organization"],
            "o": {"size": limit},
        }
        try:
            req = urllib.request.Request(
                PATENTSVIEW,
                data=json.dumps(body).encode(),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode())
            patents = data.get("patents", [])
            return {"source": "USPTO PatentsView", "query": query_text,
                    "results": patents, "mode": "live"}
        except Exception as exc:
            logger.warning("Patent search failed: %s", exc)
            return {"source": "USPTO PatentsView", "query": query_text,
                    "results": [], "mode": "offline", "error": str(exc)}

    def markush_template(self, core, substituents):
        """Generate a Markush structure description for a patent claim."""
        return {
            "claim_type": "Markush",
            "core": core,
            "substituents": substituents,
            "description": f"A compound of structure {core} wherein R is selected from {substituents}.",
        }
