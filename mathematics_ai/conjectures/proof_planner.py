"""Plan proof strategies: induction, contradiction, exhaustion, etc."""

from __future__ import annotations

STRATEGIES = {
    "direct": "Assume premises, derive the conclusion by a chain of equalities/implications.",
    "contradiction": "Assume the negation of the conclusion and derive an impossibility.",
    "contrapositive": "Prove (not Q) => (not P) instead of P => Q.",
    "induction": "Base case + inductive step: assume P(k), prove P(k+1).",
    "strong_induction": "Assume P(j) for all j ≤ k, prove P(k+1).",
    "construction": "Exhibit an explicit object witnessing the existential claim.",
    "exhaustion": "Check all finitely many cases explicitly.",
    "counterexample": "Find a single example falsifying a universal claim.",
}


def plan_proof(statement: str) -> dict[str, object]:
    """Select a recommended proof strategy from the statement text."""
    lowered = statement.lower()
    if any(k in lowered for k in ("disprove", "counterexample", "is false")):
        strategy = "counterexample"
    elif any(k in lowered for k in ("for all", "for every", "for any", "all n", "every positive integer")):
        strategy = "induction"
    elif any(k in lowered for k in ("there exists", "construct", "find an")):
        strategy = "construction"
    elif "finite" in lowered and "cases" in lowered:
        strategy = "exhaustion"
    elif "if and only if" in lowered or " iff " in lowered:
        strategy = "direct"
    else:
        strategy = "direct"
    return {
        "strategy": strategy,
        "description": STRATEGIES[strategy],
        "outline": _outline(strategy, statement),
    }


def _outline(strategy: str, statement: str) -> list[str]:
    if strategy == "induction":
        return [
            "Base case: verify the claim for the smallest value of n.",
            "Inductive hypothesis: assume the claim holds for n = k.",
            "Inductive step: use the hypothesis to prove the claim for n = k+1.",
        ]
    if strategy == "contradiction":
        return [
            "Assume the negation of the desired conclusion.",
            "Derive a contradiction with the premises or known facts.",
            "Conclude the original statement.",
        ]
    if strategy == "construction":
        return [
            "Construct an explicit object satisfying the requirements.",
            "Verify the constructed object has the claimed properties.",
        ]
    if strategy == "counterexample":
        return [
            "Identify the universal claim being disproved.",
            "Produce a concrete counterexample.",
            "Verify the counterexample violates the claim.",
        ]
    if strategy == "exhaustion":
        return ["Enumerate all cases.", "Verify the claim in each case."]
    return [
        "Restate the goal precisely.",
        "Identify relevant definitions and theorems.",
        "Derive the conclusion from the premises.",
    ]


__all__ = ["plan_proof", "STRATEGIES"]
