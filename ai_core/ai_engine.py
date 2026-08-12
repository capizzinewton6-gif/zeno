"""Core physics AI orchestrator.

Wires together reasoning, planning, context, knowledge, and safety. This is the
'brain' that the agent layer calls into. It is pure-Python and deterministic so the
whole application runs without any external LLM API; the optional Gemini engines are
invoked through the ``agents`` layer when API credentials are configured.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Optional

from .reasoning_engine import ReasoningEngine, ReasoningTrace
from .planning_engine import PlanningEngine, Pipeline
from .context_manager import ContextManager, SystemContext
from .knowledge_engine import KnowledgeEngine
from .safety_layer import SafetyLayer, SafetyReport


_HERE = os.path.dirname(os.path.abspath(__file__))


@dataclass
class AIResponse:
    trace: ReasoningTrace
    pipeline: Optional[Pipeline]
    safety: SafetyReport
    result: Any = None
    notes: str = ""

    def summary(self) -> str:
        lines = [self.trace.as_text(), "", "--- Safety ---", self.safety.summary()]
        if self.result is not None:
            lines += ["", "--- Result ---", str(self.result)]
        if self.notes:
            lines += ["", "--- Notes ---", self.notes]
        return "\n".join(lines)


class AIEngine:
    """The orchestrating intelligence of Physics AI."""

    def __init__(self):
        self.reasoning = ReasoningEngine()
        self.planning = PlanningEngine()
        self.context = ContextManager()
        self.knowledge = KnowledgeEngine()
        self.safety = SafetyLayer()
        self.system_prompt = self._load_prompt()

    @staticmethod
    def _load_prompt() -> str:
        path = os.path.join(_HERE, "prompt.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def load_system(self, name: str, regime: str = "classical", dofs: list[str] | None = None,
                    parameters: dict[str, float] | None = None) -> SystemContext:
        ctx = SystemContext(name=name, regime=regime, degrees_of_freedom=dofs or [],
                            parameters=parameters or {})
        self.context.push(ctx)
        return ctx

    def think(self, problem: str) -> ReasoningTrace:
        """Decompose a problem into structured reasoning steps."""
        trace = self.reasoning.decompose(problem)
        return trace

    def plan(self, steps: list[tuple[str, Any]]) -> Pipeline:
        return self.planning.standard_solver(steps)

    def related_fields(self, field: str) -> list[str]:
        return self.knowledge.related_fields(field)

    def run(self, problem: str, solver_steps: list[tuple[str, Any]] | None = None,
            safety_values: dict[str, Any] | None = None) -> AIResponse:
        trace = self.think(problem)
        pipe = self.plan(solver_steps) if solver_steps else None
        result = pipe.run(verbose=False) if pipe else None
        safety = self.safety.full_check(**(safety_values or {}))
        return AIResponse(trace=trace, pipeline=pipe, safety=safety, result=result)


ENGINE = AIEngine()
