"""Planning engine for proof strategies and symbolic computation pipelines."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mathematics_ai.ai_core.gemini_25_flash_engine import Gemini25FlashEngine
from mathematics_ai.ai_core.reasoning_engine import ReasoningEngine


@dataclass
class PlanStep:
    name: str
    tool: str
    args: dict[str, Any] = field(default_factory=dict)
    depends_on: list[int] = field(default_factory=list)
    result: Any = None


@dataclass
class ExecutionPlan:
    goal: str
    steps: list[PlanStep] = field(default_factory=list)

    def add(self, name: str, tool: str, **args: Any) -> int:
        idx = len(self.steps)
        self.steps.append(PlanStep(name=name, tool=tool, args=args))
        return idx

    def as_dict(self) -> dict[str, Any]:
        return {
            "goal": self.goal,
            "steps": [
                {"name": s.name, "tool": s.tool, "args": s.args}
                for s in self.steps
            ],
        }


# Domain -> ordered capability-module hints.
DOMAIN_TOOLS = {
    "algebra": ["mathematics.algebra", "calculations.symbolic_math"],
    "analysis": ["mathematics.analysis", "calculations.symbolic_math", "numerical_computing.root_finder"],
    "number_theory": ["mathematics.number_theory", "calculations.discrete_math"],
    "combinatorics": ["mathematics.combinatorics", "calculations.discrete_math"],
    "linear_algebra": ["mathematics.linear_algebra", "calculations.matrix_algebra"],
    "probability": ["mathematics.probability", "simulation.monte_carlo"],
    "geometry": ["mathematics.geometry", "tools.plot_generator"],
    "topology": ["mathematics.topology"],
    "logic": ["mathematics.logic"],
    "optimization": ["numerical_computing.optimization_solver", "mathematics.analysis"],
}


class PlanningEngine:
    """Builds an :class:`ExecutionPlan` for a mathematical goal."""

    def __init__(self, reasoning: ReasoningEngine | None = None, engine: Gemini25FlashEngine | None = None) -> None:
        self.engine = engine or Gemini25FlashEngine()
        self.reasoning = reasoning or ReasoningEngine(self.engine)

    def detect_domain(self, goal: str) -> str:
        lowered = goal.lower()
        scores = {}
        for domain, kws in {
            "number_theory": ["prime", "divisib", "modular", "congruen", "gcd", "integer sequence"],
            "algebra": ["group", "ring", "field", "polynomial root", "galois", "homomorph"],
            "analysis": ["integral", "derivativ", "limit", "series", "converg", "continuous", "differential"],
            "linear_algebra": ["eigen", "matrix", "vector space", "determinant", "svd", "rank"],
            "combinatorics": ["permut", "combin", "graph", "count", "bipartite", "matching"],
            "probability": ["probab", "expect", "variance", "markov", "stochast", "random"],
            "geometry": ["triangle", "circle", "manifold", "curvature", "polygon", "angle"],
            "topology": ["homotop", "homolog", "topolog", "knot", "manifold"],
            "logic": ["first-order", "predicate", "axiom", "proof system", "compactness"],
            "optimization": ["optimi", "minimi", "maximi", "constraint", "convex", "linear program"],
        }.items():
            scores[domain] = sum(lowered.count(k) for k in kws)
        best = max(scores, key=scores.get) if scores else "analysis"
        return best if scores.get(best, 0) > 0 else "analysis"

    def plan(self, goal: str, context: str = "") -> ExecutionPlan:
        domain = self.detect_domain(goal)
        plan = ExecutionPlan(goal=goal)
        plan.add("detect_domain", "planning", domain=domain)
        for tool in DOMAIN_TOOLS.get(domain, []):
            plan.add(f"apply_{tool.split('.')[-1]}", tool, goal=goal)
        plan.add("verify_result", "ai_core.knowledge_engine", goal=goal)
        return plan
