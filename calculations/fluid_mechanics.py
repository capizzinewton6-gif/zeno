"""Fluid mechanics calculations."""

from __future__ import annotations

import math

GRAVITY = 9.80665


class FluidMechanics:
    def reynolds_number(self, rho: float, v: float, d: float, mu: float) -> float:
        return rho * v * d / mu

    def bernoulli(self, p1: float, v1: float, z1: float, p2: float,
                  v2: float, z2: float, rho: float) -> float:
        """Return head loss (m); 0 if ideal."""
        term1 = (p1 + 0.5 * rho * v1 ** 2 + rho * GRAVITY * z1)
        term2 = (p2 + 0.5 * rho * v2 ** 2 + rho * GRAVITY * z2)
        return (term1 - term2) / (rho * GRAVITY)

    def continuity_flow(self, a1: float, v1: float, a2: float) -> float:
        return a1 * v1 / a2

    def darcy_weisbach(self, f: float, length: float, d: float, v: float) -> float:
        """Head loss due to friction (m)."""
        return f * (length / d) * v ** 2 / (2 * GRAVITY)

    def moody_friction_laminar(self, re: float) -> float:
        return 64 / re if re > 0 else float("inf")

    def hydrostatic_pressure(self, rho: float, h: float) -> float:
        return rho * GRAVITY * h

    def drag_force(self, cd: float, rho: float, v: float, area: float) -> float:
        return 0.5 * cd * rho * v ** 2 * area

    def pump_power(self, flow: float, head: float, rho: float,
                   efficiency: float = 1.0) -> float:
        return rho * GRAVITY * flow * head / efficiency
