"""Biological and evolutionary reasoning engine."""
from __future__ import annotations

from typing import Any

from ai_core.ai_engine import AIEngine


class ReasoningEngine:
    """Wraps structured biological reasoning prompts."""

    def __init__(self, ai: AIEngine | None = None):
        self.ai = ai or AIEngine()

    def hypothesize(self, observation: str, domain: str = "general") -> str:
        prompt = (
            f"Given the following biological observation in the domain of {domain}, "
            f"generate a testable hypothesis, identify the underlying mechanism, and "
            f"propose a minimal experiment to confirm or refute it.\n\nObservation:\n{observation}"
        )
        return self.ai.reason(prompt)

    def explain_mechanism(self, phenomenon: str) -> str:
        prompt = (
            "Explain the molecular / cellular / ecological mechanism responsible for "
            "the following biological phenomenon, citing the relevant pathways and "
            "established principles:\n\n" + phenomenon
        )
        return self.ai.reason(prompt)

    def evaluate_evidence(self, claim: str, evidence: str) -> str:
        prompt = (
            "Evaluate whether the evidence supports, refutes, or is inconclusive for "
            "the claim. Reason step by step and give a confidence rating (low/medium/high).\n\n"
            f"Claim: {claim}\n\nEvidence:\n{evidence}"
        )
        return self.ai.reason(prompt)
