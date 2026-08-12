"""Mechanical simulator: mechanisms, vibrations, multi-body."""

from __future__ import annotations

import math


class MechanicalSimulator:
    def four_bar(self, l1: float, l2: float, l3: float, l4: float,
                 theta2_deg: float) -> dict:
        """Position analysis of a 4-bar linkage (Grashof) for a given input angle."""
        theta2 = math.radians(theta2_deg)
        # Vector loop: l1 + l2 + l3 + l4 = 0 (l1 ground)
        K = math.sqrt(l1 ** 2 + l2 ** 2 - 2 * l1 * l2 * math.cos(theta2))
        # angle of vector from B to D
        gamma = math.acos((K ** 2 + l3 ** 2 - l4 ** 2) / (2 * K * l3))
        beta = math.acos((l1 ** 2 + K ** 2 - l2 ** 2) / (2 * l1 * K))
        theta3 = (math.pi - beta - gamma) if (theta2 % (2 * math.pi)) < math.pi else (beta - gamma)
        theta4 = math.acos((l1 ** 2 + l4 ** 2 - K ** 2) / (2 * l1 * l4)) if False else 0.0
        return {"theta2_deg": theta2_deg,
                "theta3_deg": math.degrees(theta3),
                "K": K, "note": "Simplified Freudenstein position solution"}

    def forced_vibration(self, m: float, k: float, c: float, F0: float, w: float,
                         t_end: float = 5.0, dt: float = 0.01) -> dict:
        """Steady-state amplitude of a forced damped SDOF system."""
        wn = math.sqrt(k / m)
        zeta = c / (2 * math.sqrt(k * m))
        wd = wn * math.sqrt(1 - zeta ** 2) if zeta < 1 else wn
        r = w / wn
        X = (F0 / k) / math.sqrt((1 - r ** 2) ** 2 + (2 * zeta * r) ** 2)
        phase = math.atan2(2 * zeta * r, 1 - r ** 2)
        steps = int(t_end / dt)
        times = [i * dt for i in range(steps)]
        response = [X * math.sin(w * t - phase) for t in times]
        return {"time": times, "response": response,
                "amplitude": X, "phase_rad": phase,
                "natural_frequency": wn, "damping_ratio": zeta}

    def shaft_torsion(self, torque: float, length: float, G: float, J: float) -> dict:
        angle = torque * length / (G * J)
        return {"twist_angle_rad": angle, "twist_angle_deg": math.degrees(angle)}
