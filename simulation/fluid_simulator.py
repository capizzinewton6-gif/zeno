"""Fluid simulator: pipe flow, Bernoulli, and drag."""

from __future__ import annotations

import math

GRAVITY = 9.80665


class FluidSimulator:
    def pipe_flow(self, rho: float, mu: float, v: float, d: float, length: float,
                  roughness: float = 0.0) -> dict:
        re = rho * v * d / mu
        if re < 2300:
            f = 64 / re
            regime = "laminar"
        else:
            # Swamee-Jain approximation for turbulent Darcy friction factor.
            f = 0.25 / (math.log10(roughness / (3.7 * d) + 5.74 / re ** 0.9)) ** 2
            regime = "turbulent"
        hl = f * (length / d) * v ** 2 / (2 * GRAVITY)
        return {"reynolds": re, "friction_factor": f, "regime": regime,
                "head_loss_m": hl, "pressure_drop_Pa": rho * GRAVITY * hl}

    def bernoulli_head(self, p1: float, v1: float, z1: float, p2: float,
                       v2: float, z2: float, rho: float) -> dict:
        h1 = p1 / (rho * GRAVITY) + v1 ** 2 / (2 * GRAVITY) + z1
        h2 = p2 / (rho * GRAVITY) + v2 ** 2 / (2 * GRAVITY) + z2
        return {"head_1": h1, "head_2": h2, "head_loss_m": h1 - h2}

    def drag(self, cd: float, rho: float, v: float, area: float) -> float:
        return 0.5 * cd * rho * v ** 2 * area

    def orifice_flow(self, cd: float, area: float, rho: float, dp: float) -> float:
        return cd * area * math.sqrt(2 * dp / rho)
