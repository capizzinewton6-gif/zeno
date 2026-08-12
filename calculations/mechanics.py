"""Mechanics calculations: statics, dynamics, strength of materials."""

from __future__ import annotations

import math

GRAVITY = 9.80665  # m/s^2


class Mechanics:
    def moment_of_inertia_rect(self, b: float, h: float) -> dict:
        """Rectangle about centroidal axes."""
        return {"I_x": b * h ** 3 / 12, "I_y": h * b ** 3 / 12}

    def bending_stress(self, moment: float, I: float, c: float) -> float:
        """sigma = M*c / I."""
        return moment * c / I

    def shear_stress(self, force: float, area: float) -> float:
        return force / area

    def deflection_cantilever(self, load: float, length: float, E: float, I: float) -> float:
        """Tip deflection of a cantilever with end load: P*L^3/(3EI)."""
        return load * length ** 3 / (3 * E * I)

    def power_torque(self, power: float, rpm: float) -> float:
        """Torque (Nm) from power (W) and rpm."""
        return power / (2 * math.pi * rpm / 60)

    def gear_ratio(self, n_driven: int, n_driver: int) -> float:
        return n_driven / n_driver

    def factor_of_safety(self, yield_strength: float, applied_stress: float) -> float:
        return yield_strength / applied_stress

    def natural_frequency(self, k: float, m: float) -> float:
        """omega_n = sqrt(k/m) [rad/s]."""
        return math.sqrt(k / m)

    def projectile_range(self, v: float, angle_deg: float, g: float = GRAVITY) -> float:
        return v ** 2 * math.sin(2 * math.radians(angle_deg)) / g
