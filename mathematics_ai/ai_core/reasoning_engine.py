"""Mathematical reasoning engine.

Provides deductive, inductive and constructive reasoning helpers. Concrete
symbolic truth comes from the mathematics/calculation modules; this engine
structures the *process* of reasoning (claim/justification, proof strategies)
and optionally delegates high-level reasoning to the Gemini 2.5 Flash engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mathematics_ai.ai_core.gemini_25_flash_engine import Gemini25FlashEngine


@dataclass
class ReasoningStep:
    statement: str
    justification: str
    method: str = "deductive"
    verified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReasoningTrace:
    goal: str
    steps: list[ReasoningStep] = field(default_factory=list)
    conclusion: str | None = None
    confidence: float = 0.0

    def add(self, statement: str, justification: str, method: str = "deductive", **kw: Any) -> ReasoningStep:
        step = ReasoningStep(statement=statement, justification=justification, method=method, **kw)
        self.steps.append(step)
        return step

    def conclude(self, conclusion: str, confidence: float = 1.0) -> None:
        self.conclusion = conclusion
        self.confidence = confidence

    def as_dict(self) -> dict[str, Any]:
        return {
            "goal": self.goal,
            "steps": [
                {"statement": s.statement, "justification": s.justification, "method": s.method, "verified": s.verified}
                for s in self.steps
            ],
            "conclusion": self.conclusion,
            "confidence": self.confidence,
        }


PROOF_STRATEGIES = {
    "direct": "Direct proof: assume premises, derive conclusion.",
    "contradiction": "Proof by contradiction: assume the negation, derive an impossibility.",
    "induction": "Mathematical induction: base case + inductive step.",
    "construction": "Constructive proof: exhibit an explicit object witnessing the claim.",
    "contrapositive": "Proof by contrapositive: prove (not Q) => (not P).",
    "exhaustion": "Proof by exhaustion: check finitely many cases.",
    "counterexample": "Disprove by counterexample.",
}


class ReasoningEngine:
    """Structures mathematical reasoning traces and selects strategies."""

    def __init__(self, engine: Gemini25FlashEngine | None = None) -> None:
        self.engine = engine or Gemini25FlashEngine()

    def select_strategy(self, goal: str) -> str:
        lowered = goal.lower()
        if "disprove" in lowered or "false" in lowered or "counterexample" in lowered:
            return "counterexample"
        if "for all n" in lowered or "induct" in lowered or "every positive integer" in lowered:
            return "induction"
        if "there exists" in lowered or "construct" in lowered:
            return "construction"
        if "finite" in lowered and ("case" in lowered or "only" in lowered):
            return "exhaustion"
        return "direct"

    def begin_trace(self, goal: str) -> ReasoningTrace:
        return ReasoningTrace(goal=goal)

    def reason_about(self, goal: str, context: str = "") -> ReasoningTrace:
        trace = self.begin_trace(goal)
        strategy = self.select_strategy(goal)
        trace.add(
            f"Strategy: {strategy}",
            PROOF_STRATEGIES.get(strategy, strategy),
            method="planning",
        )
        if context:
            trace.add("Established context applies", context, method="deductive")
        # Delegate high-level decomposition to Gemini (or its local fallback).
        prompt = (
            f"Mathematical goal: {goal}\nContext: {context}\n"
            f"Selected strategy: {strategy}.\n"
            f"Decompose into 2-4 concrete sub-steps to verify the goal. "
            f"Return JSON: {{\"steps\": [{{\"statement\": str, \"justification\": str}}]}}."
        )
        resp = self.engine.complete(prompt)
        trace.metadata_response = resp.text  # type: ignore[attr-defined]
        return trace
