"""Research agent: searches mathematical literature and OEIS.

Uses the research modules (arXiv, OEIS). When offline or unprovisioned, the
OEIS search falls back to a small built-in sequence lookup so the agent still
returns useful results.
"""

from __future__ import annotations

from typing import Any

from mathematics_ai.agents.base import BaseAgent, AgentResult
from mathematics_ai.research.oeis_search import oeis_lookup, oeis_search_offline
from mathematics_ai.research.arxiv_math_search import arxiv_search


class ResearchAgent(BaseAgent):
    """Searches OEIS and arXiv for relevant mathematical context."""

    name = "research_agent"

    def search_sequence(self, sequence: list[int]) -> AgentResult:
        steps = []
        result = oeis_lookup(sequence)
        steps.append({"source": "oeis", "result": result})
        return self.result(result, steps, source="oeis")

    def search_arxiv(self, query: str, max_results: int = 5) -> AgentResult:
        steps = []
        results = arxiv_search(query, max_results=max_results)
        steps.append({"source": "arxiv", "query": query, "count": len(results)})
        return self.result(results, steps, source="arxiv")

    def research(self, topic: str, sequence: list[int] | None = None) -> AgentResult:
        steps = []
        out: dict[str, Any] = {}
        if sequence is not None:
            out["oeis"] = oeis_lookup(sequence)
            steps.append({"oeis": out["oeis"]})
        out["arxiv"] = arxiv_search(topic, max_results=3)
        steps.append({"arxiv": out["arxiv"]})
        return self.result(out, steps, topic=topic)
