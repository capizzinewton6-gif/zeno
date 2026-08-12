"""Research agent: researches technologies and materials."""

from __future__ import annotations

from ai_core.ai_engine import AIEngine
from research import WebSearch, PatentSearch, PaperReader, TechnologySearch, ReferenceManager


class ResearchAgent:
    def __init__(self, engine: AIEngine | None = None):
        self.engine = engine or AIEngine()
        self.web = WebSearch(self.engine.primary)
        self.patent = PatentSearch(self.engine.secondary, self.engine.primary)
        self.paper = PaperReader(self.engine.secondary, self.engine.primary)
        self.tech = TechnologySearch(self.engine.primary)
        self.references = ReferenceManager()

    def research(self, query: str) -> str:
        return self.web.research(query)

    def patent_search(self, concept: str) -> str:
        return self.patent.search(concept)

    def assess_novelty(self, concept: str, prior_art: str = "") -> str:
        return self.patent.novelty(concept, prior_art)

    def summarize_paper(self, text: str) -> str:
        return self.paper.summarize(text)

    def benchmark(self, options: list[str]) -> str:
        return self.tech.benchmark(options)
