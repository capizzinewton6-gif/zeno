"""Verify formal proof steps and tactic applications.

Provides a lightweight, prover-agnostic checker that inspects a list of proof
steps for structural soundness (each step cites a rule and is well-formed). It
does not replace a real proof assistant but gives quick feedback for the
``tactic_engine`` and ``ProverAgent``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProofStep:
    statement: str
    rule: str
    justification: str = ""
    verified: bool = False
    depends_on: list[int] = field(default_factory=list)


@dataclass
class ProofCheck:
    steps: list[ProofStep]
    valid: bool
    errors: list[str] = field(default_factory=list)


def check_proof(steps: list[ProofStep]) -> ProofCheck:
    """Validate the structural soundness of a proof trace."""
    errors: list[str] = []
    for i, step in enumerate(steps):
        if not step.statement:
            errors.append(f"step {i}: empty statement")
        if not step.rule:
            errors.append(f"step {i}: missing rule")
        for dep in step.depends_on:
            if dep < 0 or dep >= i:
                errors.append(f"step {i}: invalid dependency {dep}")
    return ProofCheck(steps=steps, valid=not errors, errors=errors)


def check_tactic_application(tactic: str, goal: str) -> bool:
    """Heuristic: returns True if the tactic name is recognized."""
    known = {"simp", "rw", "induction", "apply", "exact", "ring", "omega", "linarith",
             "decide", "tauto", "contradiction", "linarith", "nlinarith", "norm_num"}
    return any(t in tactic for t in known)


__all__ = ["ProofStep", "ProofCheck", "check_proof", "check_tactic_application"]
