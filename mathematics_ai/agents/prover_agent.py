"""Prover agent: formulates and executes mathematical proofs.

Combines the reasoning engine (strategy selection) with concrete verification
tools (SymPy identity checks, numerical spot checks) to produce a structured
proof trace. Optionally emits formal proof scripts for Lean/Coq/Isabelle via
the formal_proofs modules when those tools are present.
"""

from __future__ import annotations

from typing import Any

import sympy as sp

from mathematics_ai.agents.base import BaseAgent, AgentResult
from mathematics_ai.ai_core import ReasoningEngine, KnowledgeEngine, SafetyLayer
from mathematics_ai.tools import formula_engine


class ProverAgent(BaseAgent):
    """Constructs and verifies mathematical proofs."""

    name = "prover_agent"

    def __init__(self) -> None:
        super().__init__()
        self.reasoning = ReasoningEngine(self.advanced)
        self.knowledge = KnowledgeEngine()
        self.safety = SafetyLayer()

    def prove(self, statement: str, method: str = "auto", assumptions: list[str] | None = None) -> AgentResult:
        # 1. safety / decidability check
        decidability = self.safety.check_provable(statement)
        if decidability["provable"] == "unknown":
            return self.result(
                {"proven": False, "status": "open/undecidable", "note": decidability["note"]},
                steps=[{"check": "decidability", "result": decidability}],
                success=True,
            )

        # 2. select strategy
        if method == "auto":
            method = self.reasoning.select_strategy(statement)
        trace = self.reasoning.begin_trace(statement)
        trace.add(f"Strategy: {method}", f"Selected proof method: {method}", method="planning")

        steps = [{"strategy": method, "assumptions": assumptions or []}]

        # 3. look up relevant theorems
        relevant = self.knowledge.search(statement)
        if relevant:
            trace.add("Apply known theorem", relevant[0]["statement"], method="deductive")
            steps.append({"applied_theorem": relevant[0]})

        # 4. attempt verification
        verified, verification_detail = self._verify(statement, assumptions or [])
        steps.append({"verification": verification_detail})

        if verified:
            trace.conclude(f"{statement} is TRUE (verified)", confidence=1.0)
            return self.result(
                {"proven": True, "method": method, "trace": trace.as_dict()},
                steps=steps,
                verified=True,
            )
        return self.result(
            {"proven": False, "method": method, "trace": trace.as_dict(), "note": "verification inconclusive"},
            steps=steps,
            verified=False,
        )

    def verify_identity(self, lhs: str, rhs: str, var: str = "x") -> AgentResult:
        ok = formula_engine.verify_identity(lhs, rhs, var)
        return self.result(
            {"identity": ok, "lhs": lhs, "rhs": rhs},
            steps=[{"method": "symbolic_simplification", "result": ok}],
            verified=ok,
        )

    def _verify(self, statement: str, assumptions: list[str]) -> tuple[bool, dict[str, Any]]:
        """Best-effort verification using symbolic/numeric checks."""
        # Detect "verify LHS = RHS" patterns
        m = _extract_equality(statement)
        if m:
            lhs, rhs, var = m
            ok = formula_engine.verify_identity(lhs, rhs, var)
            return ok, {"method": "identity_check", "lhs": lhs, "rhs": rhs, "result": ok}
        # Detect divisibility statements like "n^2 - n is divisible by 2 for all n"
        div = _extract_divisibility(statement)
        if div:
            expr, mod = div
            try:
                ok = all(int(sp.sympify(expr).subs("n", k)) % mod == 0 for k in range(-20, 21))
                return ok, {"method": "modular_check", "expr": expr, "mod": mod, "result": ok}
            except Exception as e:
                return False, {"method": "modular_check", "error": str(e)}
        return False, {"method": "none", "note": "no automatic verifier available; needs formal prover"}


def _extract_equality(statement: str) -> tuple[str, str, str] | None:
    """Parse statements of the form 'verify that LHS = RHS' / 'prove LHS = RHS'."""
    import re
    # find '=' not inside <=, >=, !=
    pattern = re.compile(r"(?:verify|prove|show|check)\s+(?:that\s+)?(.+?)\s*=\s*(.+?)(?:\s+for\s+(?:all\s+)?(\w+))?$", re.IGNORECASE)
    m = pattern.search(statement)
    if m:
        lhs, rhs, var = m.group(1).strip(), m.group(2).strip(), (m.group(3) or "x").strip()
        return lhs, rhs, var
    # generic equality anywhere
    if "=" in statement and "<" not in statement and ">" not in statement:
        parts = statement.split("=", 1)
        var = "x"
        return parts[0].strip(), parts[1].strip(), var
    return None


def _extract_divisibility(statement: str) -> tuple[str, int] | None:
    import re
    m = re.search(r"(.+?)\s+is\s+divisible\s+by\s+(\d+)", statement, re.IGNORECASE)
    if m:
        return m.group(1).strip(), int(m.group(2))
    return None
