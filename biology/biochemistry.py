"""Enzymes, metabolic networks, and kinetics."""
from __future__ import annotations

import math

from biology._shared import safe_ai_reason

AMINO_ACID_MW = {
    "A": 89.09, "R": 174.20, "N": 132.12, "D": 133.10, "C": 121.16,
    "E": 147.13, "Q": 146.15, "G": 75.07, "H": 155.16, "I": 131.17,
    "L": 131.17, "K": 146.19, "M": 149.21, "F": 165.19, "P": 115.13,
    "S": 105.09, "T": 119.12, "W": 204.23, "Y": 181.19, "V": 117.15,
}

AA_HYDROPATHY = {
    "A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5,
    "E": -3.5, "Q": -3.5, "G": -0.4, "H": -3.2, "I": 4.5,
    "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6,
    "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2,
}


class BiochemistryModule:
    def handle(self, command: str, query: str, ctx) -> str:
        return safe_ai_reason(query, ctx)

    @staticmethod
    def michaelis_menten_rate(substrate: float, vmax: float, km: float) -> float:
        if km == 0:
            raise ValueError("Km must be > 0")
        return vmax * substrate / (km + substrate)

    @staticmethod
    def lineweaver_burk(vmax: float, km: float, n_points: int = 5) -> list[tuple[float, float]]:
        pts = []
        for i in range(1, n_points + 1):
            s = km * i
            v = vmax * s / (km + s)
            pts.append((round(1 / s, 4), round(1 / v, 4)))
        return pts

    @staticmethod
    def protein_molecular_weight(sequence: str) -> float:
        return sum(AMINO_ACID_MW.get(aa, 0.0) for aa in sequence.upper()) - (
            18.02 * max(len(sequence) - 1, 0)
        )

    @staticmethod
    def hydropathy_index(sequence: str, window: int = 9) -> list[float]:
        seq = sequence.upper()
        if len(seq) < window:
            return []
        out = []
        for i in range(len(seq) - window + 1):
            chunk = seq[i : i + window]
            out.append(round(sum(AA_HYDROPATHY.get(a, 0.0) for a in chunk) / window, 3))
        return out

    @staticmethod
    def extinction_coefficient_280(sequence: str) -> float:
        """Estimate using tryptophan (5500), tyrosine (1490), cystine (125)."""
        seq = sequence.upper()
        n_w = seq.count("W")
        n_y = seq.count("Y")
        n_c = seq.count("C") // 2
        return 5500 * n_w + 1490 * n_y + 125 * n_c
