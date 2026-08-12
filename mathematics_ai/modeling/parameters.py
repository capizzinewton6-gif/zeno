"""Variables, parameters and fundamental constants."""

from __future__ import annotations

import math
from typing import Any

FUNDAMENTAL_CONSTANTS: dict[str, float] = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "golden_ratio": (1 + math.sqrt(5)) / 2,
    "euler_mascheroni": 0.5772156649015329,
    "sqrt2": math.sqrt(2),
    "sqrt3": math.sqrt(3),
    "ln2": math.log(2),
    "catalan": 0.9159655941772190,  # Catalan's constant
    "apery": 1.2020569031595942,  # Apéry's constant
}


def get_constant(name: str) -> float:
    return FUNDAMENTAL_CONSTANTS[name.lower().replace(" ", "_")]


def list_constants() -> dict[str, float]:
    return dict(FUNDAMENTAL_CONSTANTS)


class Variable:
    """A symbolic variable with a domain and optional default value."""

    def __init__(self, name: str, domain: str = "real", default: Any = None) -> None:
        self.name = name
        self.domain = domain
        self.default = default

    def __repr__(self) -> str:
        return f"Var({self.name}: {self.domain})"


class Parameter:
    """A named parameter with a value and uncertainty."""

    def __init__(self, name: str, value: float, uncertainty: float = 0.0, unit: str = "") -> None:
        self.name = name
        self.value = value
        self.uncertainty = uncertainty
        self.unit = unit

    def relative_uncertainty(self) -> float:
        return self.uncertainty / abs(self.value) if self.value != 0 else float("inf")

    def __repr__(self) -> str:
        return f"Param({self.name}={self.value}±{self.uncertainty} {self.unit})"


__all__ = ["FUNDAMENTAL_CONSTANTS", "get_constant", "list_constants", "Variable", "Parameter"]
