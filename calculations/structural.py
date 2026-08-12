"""Structural calculations: beams, columns, and connections."""

from __future__ import annotations

import math


class Structural:
    def euler_buckling(self, E: float, I: float, L: float, k: float = 1.0) -> float:
        """Critical load: pi^2*E*I / (k*L)^2."""
        return math.pi ** 2 * E * I / (k * L) ** 2

    def max_moment_simple_beam(self, w: float, L: float) -> float:
        """Simply supported beam, uniform load: w*L^2/8."""
        return w * L ** 2 / 8

    def max_deflection_simple_beam(self, w: float, L: float, E: float, I: float) -> float:
        """5*w*L^4 / (384*E*I)."""
        return 5 * w * L ** 4 / (384 * E * I)

    def reaction_simple_beam(self, w: float, L: float) -> float:
        return w * L / 2

    def shear_max_simple_beam(self, w: float, L: float) -> float:
        return w * L / 2

    def column_slenderness(self, L: float, r: float) -> float:
        return L / r

    def weldthroat(self, force: float, length: float, allowable: float) -> float:
        """Required weld throat thickness."""
        return force / (length * allowable)

    def bolt_shear(self, force: float, n_bolts: float, area: float, allowable: float) -> float:
        return force / (n_bolts * area * allowable)
