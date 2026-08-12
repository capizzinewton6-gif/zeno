"""Construct mathematical trial solutions and wavefunctions."""

from __future__ import annotations

import numpy as np
import sympy as sp


class AnsatzGenerator:
    """Generate common trial solutions for boundary-value problems."""

    @staticmethod
    def fourier_ansatz(n_terms: int = 5, var: str = "x", L: float = 1.0) -> sp.Expr:
        x = sp.Symbol(var)
        terms = []
        for n in range(1, n_terms + 1):
            terms.append(sp.Symbol(f"a_{n}") * sp.sin(n * sp.pi * x / L))
        return sum(terms)

    @staticmethod
    def gaussian_wave_packet(x: np.ndarray, k0: float, x0: float, sigma: float) -> np.ndarray:
        return np.exp(1j * k0 * x) * np.exp(-((x - x0) ** 2) / (2 * sigma ** 2))

    @staticmethod
    def separable_ansatz(vars_: list[str], n_terms: int = 3) -> list[sp.Expr]:
        syms = [sp.Symbol(v) for v in vars_]
        terms = []
        for i in range(n_terms):
            coeff = sp.Symbol(f"c_{i}")
            prod = coeff
            for s in syms:
                prod *= sp.sin(sp.Symbol(f"n_{s}_{i}") * s)
            terms.append(prod)
        return terms
