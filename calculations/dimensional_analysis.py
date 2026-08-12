"""Buckingham Pi theorem, SI/Natural units, and scale transformations."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from tools.constant_engine import CONSTANTS


# SI base dimension symbols and their canonical exponent vectors in order
# [L, M, T, I, theta, N, J]
BASE_DIMS = ["L", "M", "T", "I", "theta", "N", "J"]

# A small registry mapping named physical quantities to their SI dimensions.
QUANTITY_DIMS: dict[str, dict[str, int]] = {
    "length": {"L": 1},
    "area": {"L": 2},
    "volume": {"L": 3},
    "velocity": {"L": 1, "T": -1},
    "acceleration": {"L": 1, "T": -2},
    "force": {"L": 1, "M": 1, "T": -2},
    "energy": {"L": 2, "M": 1, "T": -2},
    "power": {"L": 2, "M": 1, "T": -3},
    "pressure": {"L": -1, "M": 1, "T": -2},
    "charge": {"T": 1, "I": 1},
    "voltage": {"L": 2, "M": 1, "T": -3, "I": -1},
    "resistance": {"L": 2, "M": 1, "T": -3, "I": -2},
    "capacitance": {"L": -2, "M": -1, "T": 4, "I": 2},
    "magnetic_field": {"L": 0, "M": 1, "T": -2, "I": -1},
    "frequency": {"T": -1},
    "action": {"L": 2, "M": 1, "T": -1},
    "mass_density": {"L": -3, "M": 1},
    "temperature": {"theta": 1},
    "entropy": {"L": 2, "M": 1, "T": -2, "theta": -1},
    "magnetic_flux": {"L": 2, "M": 1, "T": -2, "I": -1},
}


@dataclass
class Dimension:
    exponents: dict[str, int]

    def __mul__(self, other: "Dimension") -> "Dimension":
        return Dimension({k: self.exponents.get(k, 0) + other.exponents.get(k, 0) for k in BASE_DIMS})

    def __truediv__(self, other: "Dimension") -> "Dimension":
        return Dimension({k: self.exponents.get(k, 0) - other.exponents.get(k, 0) for k in BASE_DIMS})

    def power(self, n: int) -> "Dimension":
        return Dimension({k: self.exponents.get(k, 0) * n for k in BASE_DIMS})

    def is_dimensionless(self) -> bool:
        return all(v == 0 for v in self.exponents.values())

    def as_str(self) -> str:
        pos = {k: v for k, v in self.exponents.items() if v > 0}
        neg = {k: -v for k, v in self.exponents.items() if v < 0}
        num = "*".join(f"{k}^{v}" for k, v in pos.items()) or "1"
        den = "*".join(f"{k}^{v}" for k, v in neg.items())
        return num if not neg else f"{num}/{den}"


class DimensionalAnalysis:
    """Buckingham Pi theorem, unit consistency, and natural-unit conversions."""

    @staticmethod
    def dim_of(quantity: str) -> Dimension:
        try:
            return Dimension({k: QUANTITY_DIMS[quantity].get(k, 0) for k in BASE_DIMS})
        except KeyError as exc:
            raise KeyError(f"Unknown quantity '{quantity}'. Register it in QUANTITY_DIMS.") from exc

    @staticmethod
    def consistent(left: Dimension, right: Dimension) -> bool:
        return left.exponents == right.exponents

    @staticmethod
    def buckingham_pi(quantities: list[str], repeating: list[str]) -> list[str]:
        """Return a textual description of Pi groups for the given quantities.

        A proper implementation solves the linear system for the null space of the
        dimension matrix; here we return a structured textual description suitable
        for the reasoning trace and the dimensional validator.
        """
        if len(repeating) < 2:
            return ["Need at least 2 repeating variables to form dimensionless groups."]
        groups: list[str] = []
        rep_dims = [DimensionalAnalysis.dim_of(q) for q in repeating]
        for q in quantities:
            if q in repeating:
                continue
            target = DimensionalAnalysis.dim_of(q)
            desc = (f"Pi_{q}: combination of {q} and powers of ({', '.join(repeating)}) "
                    f"chosen so the net dimensions cancel. Target dim = {target.as_str()}.")
            groups.append(desc)
        return groups

    @staticmethod
    def natural_units_scale() -> dict[str, float]:
        """Conversion factors for c = hbar = kB = 1 (energy is the base unit)."""
        return CONSTANTS.natural_units()

    @staticmethod
    def planck_units() -> dict[str, float]:
        return CONSTANTS.planck_units()

    @staticmethod
    def scale_transform(value: float, scale_factor: float) -> float:
        """Apply a uniform scale factor to a dimensionless ratio."""
        return value * scale_factor


DIM_ANALYSIS = DimensionalAnalysis()
