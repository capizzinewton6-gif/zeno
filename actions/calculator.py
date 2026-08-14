"""
actions - calculator
=====================
Evaluate arithmetic expressions safely.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import ast
import operator
from typing import Any, Dict, Optional

from core.capability import Capability


class Calculator(Capability):
    """Evaluate arithmetic expressions safely."""

    _OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "calculator"
        self.description = "Evaluate arithmetic expressions safely."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        expr = self._extract(task)
        if not expr:
            return self.error("No arithmetic expression found in task.")
        try:
            node = ast.parse(expr, mode="eval").body
            value = self._eval(node)
        except ZeroDivisionError:
            return self.error("Division by zero.")
        except Exception as exc:
            return self.error(f"Could not evaluate '{expr}': {exc}")
        return self.ok(f"{expr} = {value}", expression=expr, value=value)

    def _eval(self, node):
        if isinstance(node, ast.Constant):  # numbers
            return node.value
        if isinstance(node, ast.BinOp):
            op = self._OPS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return op(self._eval(node.left), self._eval(node.right))
        if isinstance(node, ast.UnaryOp):
            op = self._OPS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            return op(self._eval(node.operand))
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    def _extract(self, task: str) -> str:
        task = task.strip()
        for prefix in ("calculate:", "calc:", "what is", "what's", "compute:", "evaluate:"):
            if task.lower().startswith(prefix):
                task = task[len(prefix):].strip()
                break
        else:
            # Word-prefixes without colon: "calculate 2+2", "calc 2+2", "compute 2+2"
            for word in ("calculate", "calc", "compute", "evaluate"):
                if task.lower().startswith(word):
                    task = task[len(word):].strip()
                    break
        return task.strip().strip("\"'").rstrip("?")

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
