"""Manufacturing tolerances: standards and stack-up analysis."""

from __future__ import annotations

import math

# ISO 2768 fine (F) general tolerances.
ISO_2768_FINE = {
    "0.5-3": 0.05, "3-6": 0.05, "6-30": 0.1, "30-120": 0.15,
    "120-400": 0.2, "400-1000": 0.3, "1000-2000": 0.5,
}
ISO_2768_MEDIUM = {
    "0.5-3": 0.1, "3-6": 0.1, "6-30": 0.2, "30-120": 0.3,
    "120-400": 0.5, "400-1000": 0.8, "1000-2000": 1.2,
}


class Tolerance:
    def __init__(self, standard: dict | None = None):
        self.standard = standard or ISO_2768_MEDIUM

    def general(self, dimension: float) -> float:
        for rng, tol in self.standard.items():
            lo, hi = [float(x) for x in rng.split("-")]
            if lo <= dimension <= hi:
                return tol
        return 1.2

    def worst_case_stackup(self, tolerances: list[float]) -> float:
        return sum(tolerances)

    def statistical_stackup(self, tolerances: list[float]) -> float:
        return math.sqrt(sum(t ** 2 for t in tolerances))

    def clearance_fit(self, hole: float, shaft: float) -> dict:
        diff = hole - shaft
        if diff > 0:
            return {"type": "clearance", "value": round(diff, 4)}
        if diff < 0:
            return {"type": "interference", "value": round(-diff, 4)}
        return {"type": "transition", "value": 0.0}

    def it_grade(self, it: int, size: float) -> float:
        """ISO IT grade tolerance (approx)."""
        i = 0.45 * size ** (1 / 3) + 0.001 * size  # fundamental tolerance unit
        factors = {5: 7, 6: 10, 7: 16, 8: 25, 9: 40, 10: 64, 11: 100, 12: 160}
        return factors.get(it, 100) * i * 1e-3  # mm
