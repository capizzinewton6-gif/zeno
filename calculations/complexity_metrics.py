"""Cyclomatic complexity, cognitive load, and Halstead metrics."""
from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Any

# Decision-point node types that increase cyclomatic complexity
_DECISION_NODES = (
    ast.If, ast.For, ast.While, ast.And, ast.Or,
    ast.ExceptHandler, ast.comprehension,
)


class ComplexityMetrics:
    """Code complexity calculators grounded in the Python AST."""

    def cyclomatic_complexity(self, source: str, language: str = "python") -> float:
        if language.lower() != "python":
            return self._heuristic_complexity(source)
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return 1.0
        decisions = sum(1 for node in ast.walk(tree) if isinstance(node, _DECISION_NODES))
        # boolean ops add complexity
        bool_ops = sum(1 for n in ast.walk(tree)
                       if isinstance(n, (ast.BoolOp,))
                       for _ in getattr(n, "values", [1])[1:])
        return 1.0 + decisions + bool_ops

    def cognitive_complexity(self, source: str, language: str = "python") -> float:
        """Approximation: cyclomatic + nesting penalty."""
        if language.lower() != "python":
            return self._heuristic_complexity(source) * 1.5
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return 1.0
        score = 0.0

        def visit(node: ast.AST, depth: int) -> None:
            nonlocal score
            if isinstance(node, _DECISION_NODES):
                score += depth
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                    visit(child, depth + 1)
                else:
                    visit(child, depth)

        visit(tree, 1)
        return score + 1

    def halstead(self, source: str, language: str = "python") -> dict[str, float]:
        """Compute Halstead metrics from operators/operands counts."""
        operators, operands = self._count_tokens(source, language)
        n1, n2 = len(operators), len(operands)
        N1, N2 = sum(operators.values()), sum(operands.values())
        vocabulary = n1 + n2
        length = N1 + N2
        volume = length * (max(1, vocabulary) and _log2(max(1, vocabulary)))
        difficulty = (n1 / 2) * (n2 / max(1, n1)) if n1 and n2 else 0
        effort = difficulty * volume
        return {
            "n1": n1, "n2": n2, "N1": N1, "N2": N2,
            "vocabulary": vocabulary, "length": length,
            "volume": round(volume, 1), "difficulty": round(difficulty, 2),
            "effort": round(effort, 1),
        }

    def _count_tokens(self, source: str, language: str
                      ) -> tuple[dict[str, int], dict[str, int]]:
        import keyword
        import tokenize
        import io
        operators: dict[str, int] = {}
        operands: dict[str, int] = {}
        if language.lower() != "python":
            return self._generic_count(source)
        try:
            tokens = tokenize.tokenize(io.BytesIO(source.encode()).readline)
            for tok in tokens:
                ttype, string = tok.type, tok.string
                if ttype == tokenize.OP:
                    operators[string] = operators.get(string, 0) + 1
                elif ttype == tokenize.NAME and not keyword.iskeyword(string):
                    operands[string] = operands.get(string, 0) + 1
                elif ttype == tokenize.NAME and keyword.iskeyword(string):
                    operators[string] = operators.get(string, 0) + 1
                elif ttype == tokenize.STRING:
                    operands["__str__"] = operands.get("__str__", 0) + 1
                elif ttype == tokenize.NUMBER:
                    operands["__num__"] = operands.get("__num__", 0) + 1
        except Exception:
            return self._generic_count(source)
        return operators, operands

    def _generic_count(self, source: str) -> tuple[dict[str, int], dict[str, int]]:
        import re
        operators: dict[str, int] = {}
        operands: dict[str, int] = {}
        for m in re.finditer(r"[\+\-\*/%=<>!&|^\~]+", source):
            operators[m.group()] = operators.get(m.group(), 0) + 1
        for m in re.finditer(r"[A-Za-z_]\w*", source):
            operands[m.group()] = operands.get(m.group(), 0) + 1
        return operators, operands

    def _heuristic_complexity(self, source: str) -> float:
        # Non-python: count control-flow keywords as a rough proxy
        import re
        kws = re.findall(r"\b(if|for|while|switch|case|catch|&&|\|\|)\b", source)
        return 1.0 + len(kws)


def _log2(n: float) -> float:
    import math
    return math.log2(n) if n > 0 else 0.0
