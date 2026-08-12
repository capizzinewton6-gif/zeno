"""Conjecture agent: generates and tests mathematical conjectures."""

from __future__ import annotations

import itertools
from typing import Any

from mathematics_ai.agents.base import BaseAgent, AgentResult
from mathematics_ai.conjectures.pattern_finder import find_pattern, fit_polynomial
from mathematics_ai.conjectures.counterexample_search import find_counterexample
from mathematics_ai.conjectures.statement_builder import build_conjecture
from mathematics_ai.conjectures.consistency_checker import test_boundary_conditions
from mathematics_ai.memory import conjectures as conjecture_store


class ConjectureAgent(BaseAgent):
    """Generates conjectures from data and searches for counterexamples."""

    name = "conjecture_agent"

    def generate_from_sequence(self, sequence: list[int | float], name: str = "generated") -> AgentResult:
        steps = []
        pattern = find_pattern(sequence)
        steps.append({"stage": "pattern_finding", "pattern": pattern})

        # try polynomial fit on first-differences
        poly = fit_polynomial(sequence)
        if poly is not None:
            steps.append({"stage": "polynomial_fit", "polynomial": poly})

        statement = build_conjecture(name, sequence, pattern, poly)
        steps.append({"stage": "statement", "conjecture": statement})

        # test boundary / trivial cases
        boundary = test_boundary_conditions(statement, sequence)
        steps.append({"stage": "boundary_tests", "result": boundary})

        # search for counterexample
        counter = find_counterexample(sequence, pattern)
        steps.append({"stage": "counterexample_search", "result": counter})

        status = "falsified" if counter else "plausible"
        record = conjecture_store.add({
            "name": name,
            "sequence": sequence,
            "statement": statement,
            "status": status,
            "pattern": pattern,
        })
        return self.result(
            {"conjecture": statement, "status": status, "counterexample": counter, "id": record["id"]},
            steps=steps,
        )

    def test_conjecture(self, statement: str, checker) -> AgentResult:
        """Test an arbitrary conjecture via a user-supplied checker(n) -> bool."""
        counter = None
        for n in range(1, 1000):
            try:
                if not checker(n):
                    counter = n
                    break
            except Exception:
                continue
        status = "falsified" if counter is not None else "plausible"
        record = conjecture_store.add({"statement": statement, "status": status, "counterexample": counter})
        return self.result(
            {"statement": statement, "status": status, "counterexample": counter, "id": record["id"]},
            steps=[{"checked_up_to": 999}],
        )
