"""Yang-Mills fields, vector potentials, and differential forms."""

from __future__ import annotations

import numpy as np
import sympy as sp


class GaugeFields:
    """Abelian and non-abelian gauge-field constructions."""

    @staticmethod
    def vector_potential_charged_wire(rho: np.ndarray, eps0: float = 8.85e-12) -> np.ndarray:
        """Scalar potential of a line charge ~ ln(r)."""
        return np.where(rho > 0, -np.log(np.abs(rho) + 1e-12) / (2 * np.pi * eps0), 0.0)

    @staticmethod
    def field_strength_from_potential(A: sp.Matrix, coords: list[sp.Symbol]) -> sp.Matrix:
        """F_{mu nu} = d_mu A_nu - d_nu A_mu (abelian)."""
        n = len(coords)
        F = sp.zeros(n, n)
        for mu in range(n):
            for nu in range(n):
                F[mu, nu] = sp.diff(A[nu], coords[mu]) - sp.diff(A[mu], coords[nu])
        return sp.simplify(F)

    @staticmethod
    def su2_generators() -> list[sp.Matrix]:
        return [sp.Matrix([[0, 1], [1, 0]]),
                sp.Matrix([[0, -sp.I], [sp.I, 0]]),
                sp.Matrix([[1, 0], [0, -1]])]

    @staticmethod
    def su3_gell_mann_matrices() -> list[sp.Matrix]:
        """Return the 8 Gell-Mann matrices (3x3)."""
        z = sp.zeros(3)
        mats = []
        def put(i, j, val):
            m = sp.zeros(3)
            m[i, j] = val
            m[j, i] = val if not sp.I in [val] else val
            return m
        l1 = sp.zeros(3); l1[0, 1] = l1[1, 0] = 1
        l2 = sp.zeros(3); l2[0, 1] = -sp.I; l2[1, 0] = sp.I
        l3 = sp.diag(1, -1, 0)
        l4 = sp.zeros(3); l4[0, 2] = l4[2, 0] = 1
        l5 = sp.zeros(3); l5[0, 2] = -sp.I; l5[2, 0] = sp.I
        l6 = sp.zeros(3); l6[1, 2] = l6[2, 1] = 1
        l7 = sp.zeros(3); l7[1, 2] = -sp.I; l7[2, 1] = sp.I
        l8 = sp.diag(1, 1, -2) / sp.sqrt(3)
        return [l1, l2, l3, l4, l5, l6, l7, l8]

    @staticmethod
    def exterior_derivative(form: sp.Matrix, coords: list[sp.Symbol]) -> sp.Matrix:
        """d of an antisymmetric 2-form: returns a 3-form component list (symbolic)."""
        return GaugeFields.field_strength_from_potential(form, coords)
