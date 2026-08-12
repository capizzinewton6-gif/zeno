"""Main physical intelligence and reasoning orchestrator.

The PhysicsAgent is the top-level entry point the UI calls. It decomposes a problem
through the ai_core engine, dispatches domain work to specialized agents, runs
verification, and returns a structured answer that the UI can render.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from ai_core.ai_engine import ENGINE, AIResponse
from agents.theory_agent import TheoryAgent
from agents.hypothesis_agent import HypothesisAgent
from agents.compute_agent import ComputeAgent
from agents.literature_agent import LiteratureAgent
from agents.experimental_agent import ExperimentalAgent


@dataclass
class PhysicsAnswer:
    problem: str
    response: AIResponse
    theory: Any = None
    hypothesis: Any = None
    computation: Any = None
    literature: Any = None
    experimental: Any = None

    def render(self) -> str:
        lines = [self.response.trace.as_text(), "", "=== Verification ===", self.response.safety.summary()]
        if self.computation is not None:
            lines += ["", "=== Computation ===", str(self.computation)]
        return "\n".join(lines)


class PhysicsAgent:
    """The autonomous orchestrator."""

    def __init__(self):
        self.engine = ENGINE
        self.theory = TheoryAgent()
        self.hypothesis = HypothesisAgent()
        self.compute = ComputeAgent()
        self.literature = LiteratureAgent()
        self.experimental = ExperimentalAgent()

    def solve(self, problem: str, **kwargs) -> PhysicsAnswer:
        resp = self.engine.run(problem)
        return PhysicsAnswer(problem=problem, response=resp)

    def think(self, problem: str):
        return self.engine.think(problem)

    def explain(self, concept: str) -> str:
        """Plain-language explanation routed to the relevant domain agent."""
        return self.theory.explain(concept)

    def simulate(self, name: str, **params):
        """Dispatch a simulation by name; results render on the UI."""
        return self.compute.run_simulation(name, **params)

    def verify(self, **values) -> str:
        rep = self.engine.safety.full_check(**values)
        return rep.summary()


PHYSICS_AGENT = PhysicsAgent()
