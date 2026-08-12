"""Noether's theorem mapping, Lie groups, and broken symmetries."""

from __future__ import annotations

import sympy as sp


class SymmetryAnalyzer:
    """Map continuous symmetries to conserved charges (Noether's theorem)."""

    NOETHER_MAP = {
        "time_translation": ("Energy", "H = const"),
        "spatial_translation": ("Momentum", "p = const"),
        "rotation": ("Angular momentum", "L = const"),
        "u1_gauge": ("Charge", "Q = const"),
        "u1_phase": ("Particle number", "N = const"),
        "su2_isospin": ("Isospin", "I = const"),
    }

    @staticmethod
    def conserved_charge(symmetry: str) -> tuple[str, str]:
        try:
            return SymmetryAnalyzer.NOETHER_MAP[symmetry.lower()]
        except KeyError as exc:
            raise KeyError(f"Unknown symmetry: {symmetry}") from exc

    @staticmethod
    def lie_algebra(group: str) -> str:
        return {
            "u1": "1 generator, abelian: [T, T] = 0",
            "su2": "3 generators: [T_a, T_b] = i epsilon_abc T_c",
            "su3": "8 generators: [T_a, T_b] = i f_abc T_c",
            "so3": "3 generators (same algebra as su2): [L_i, L_j] = i eps_ijk L_k",
            "so32": "[K_i, K_j] = -i eps_ijk K_k  (Lorentz)",
        }.get(group.lower(), f"Unknown Lie group: {group}")

    @staticmethod
    def spontaneous_breaking(group: str, subgroup: str) -> dict:
        return {"original_group": group, "unbroken_subgroup": subgroup,
                "goldstone_bosons": f"dim({group}) - dim({subgroup}) massless modes (Goldstone theorem)"}
