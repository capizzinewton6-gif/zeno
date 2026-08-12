"""Engineering calculator."""

from __future__ import annotations

import math

from calculations.unit_converter import UnitConverter


class Calculator:
    def __init__(self):
        self.converter = UnitConverter()

    def evaluate(self, expression: str) -> float:
        """Safe evaluation of math expressions."""
        allowed = {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
            "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
            "exp": math.exp, "pi": math.pi, "e": math.e,
            "pow": pow, "abs": abs, "ceil": math.ceil, "floor": math.floor,
            "radians": math.radians, "degrees": math.degrees,
        }
        try:
            return float(eval(expression, {"__builtins__": {}}, allowed))  # noqa: S307
        except Exception as exc:
            raise ValueError(f"Cannot evaluate '{expression}': {exc}")

    def convert(self, value: float, frm: str, to: str) -> float:
        return self.converter.convert(value, frm, to)

    def ohms_law(self, v: float | None = None, i: float | None = None,
                 r: float | None = None) -> float:
        if v is None and i is not None and r is not None:
            return i * r
        if i is None and v is not None and r is not None:
            return v / r
        if r is None and v is not None and i is not None:
            return v / i
        raise ValueError("Provide exactly two of v, i, r.")
