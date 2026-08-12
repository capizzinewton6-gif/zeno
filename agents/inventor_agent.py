"""Inventor agent: turns ideas into inventions."""

from __future__ import annotations

from ai_core.ai_engine import AIEngine
from invention import IdeaGenerator, ConceptDeveloper, FeasibilityAnalyzer
from invention.problem_finder import ProblemFinder
from invention.improvement_engine import ImprovementEngine


class InventorAgent:
    def __init__(self, engine: AIEngine | None = None):
        self.engine = engine or AIEngine()
        self.idea_gen = IdeaGenerator(self.engine.primary)
        self.concept_dev = ConceptDeveloper(self.engine.primary)
        self.feasibility = FeasibilityAnalyzer(self.engine.primary)
        self.problem_finder = ProblemFinder(self.engine.primary)
        self.improvement = ImprovementEngine(self.engine.primary)

    def invent(self, idea: str) -> str:
        return self.engine.reason(
            f"Turn this idea into a complete invention concept with novelty, "
            f"feasibility, and implementation path: {idea}",
            system="You are a world-class inventor.")

    def improve(self, existing: str) -> str:
        return self.improvement.improve(existing)

    def find_problems(self, domain: str) -> str:
        return self.problem_finder.find(domain)

    def evaluate(self, concept: str) -> str:
        return self.feasibility.analyze(concept)
