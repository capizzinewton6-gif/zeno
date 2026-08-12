"""Calculates time and space complexity formulas."""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from typing import Any

from calculations.complexity_metrics import ComplexityMetrics


@dataclass
class ComplexityFormula:
    time: str  # e.g. O(n^2)
    space: str  # e.g. O(n)
    confidence: float = 0.0
    notes: list[str] = field(default_factory=list)


class FormulaEngine:
    """Derives Big-O formulas from code structure."""

    def __init__(self, metrics: ComplexityMetrics | None = None) -> None:
        self.metrics = metrics or ComplexityMetrics()

    def analyze(self, source: str, language: str = "python") -> ComplexityFormula:
        if language.lower() != "python":
            return self._heuristic(source)
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return ComplexityFormula("O(?)", "O(?)", 0.0, ["syntax error"])
        time, space, notes = self._walk(tree, depth=0)
        return ComplexityFormula(time, space, confidence=0.7, notes=notes)

    def _walk(self, node: ast.AST, depth: int) -> tuple[str, str, list[str]]:
        time_factors: list[str] = []
        space_factors: list[str] = []
        notes: list[str] = []
        loops = 0

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.For, ast.While)):
                loops += 1
                # Recurse into loop body for nesting
                inner_time, inner_space, inner_notes = self._walk(child, depth + 1)
                time_factors.append(inner_time if inner_time != "O(1)" else "n")
                space_factors.append(inner_space)
                notes.extend(inner_notes)
            elif isinstance(child, (ast.List, ast.Dict, ast.Set, ast.ListComp,
                                    ast.DictComp, ast.SetComp)):
                space_factors.append("n")
            else:
                _, sp, n = self._walk(child, depth)
                space_factors.append(sp)
                notes.extend(n)

        # Combine
        if loops == 0:
            time = "O(1)" if not time_factors else f"O({' + '.join(time_factors)})"
        elif loops == 1:
            time = "O(n)"
        elif loops == 2:
            time = "O(n^2)"
        elif loops == 3:
            time = "O(n^3)"
        else:
            time = f"O(n^{loops})"

        space = "O(1)" if not any(s != "O(1)" for s in space_factors) else "O(n)"
        if depth > 0 and "n" in space_factors:
            space = "O(n)"
        return time, space, notes

    def _heuristic(self, source: str) -> ComplexityFormula:
        loop_keywords = re.findall(r"\b(?:for|while|forEach|map|filter)\b", source)
        nested = source.count("{")  # rough nesting proxy
        if not loop_keywords:
            return ComplexityFormula("O(1)", "O(1)", 0.4, ["heuristic: no loops detected"])
        if len(loop_keywords) == 1:
            return ComplexityFormula("O(n)", "O(1)", 0.4, ["heuristic"])
        if len(loop_keywords) == 2:
            return ComplexityFormula("O(n^2)", "O(1)", 0.4, ["heuristic"])
        return ComplexityFormula(f"O(n^{len(loop_keywords)})", "O(n)", 0.3, ["heuristic"])
