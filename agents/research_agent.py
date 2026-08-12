"""Research agent: queries external databases for identified metadata."""

from __future__ import annotations

from typing import Any, Dict, List

from research.model_zoo_search import ModelZooSearch
from research.patent_search import PatentSearch
from research.reference_manager import ReferenceManager


class ResearchAgent:
    """Aggregate model-zoo, patent, and reference lookups for an identity/object."""

    def __init__(self, references: Optional[ReferenceManager] = None) -> None:
        self.zoo = ModelZooSearch()
        self.patents = PatentSearch()
        self.references = references or ReferenceManager()

    def investigate(self, query: str) -> Dict[str, Any]:
        return {
            "query": query,
            "models": [{"name": m.name, "source": m.source, "url": m.url}
                       for m in self.zoo.search(query)],
            "patents": [{"number": p.number, "title": p.title, "url": p.url}
                        for p in self.patents.search(query)],
            "references": [r.title for r in self.references.search(query)],
        }
