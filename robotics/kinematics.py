"""Robot kinematics: forward, inverse, and Jacobian computations."""

from __future__ import annotations

import math

import numpy as np


class Kinematics:
    def forward_2r(self, l1: float, l2: float, t1_deg: float, t2_deg: float) -> dict:
        t1, t2 = math.radians(t1_deg), math.radians(t2_deg)
        x = l1 * math.cos(t1) + l2 * math.cos(t1 + t2)
        y = l1 * math.sin(t1) + l2 * math.sin(t1 + t2)
        return {"x": x, "y": y, "phi_deg": math.degrees(t1 + t2)}

    def inverse_2r(self, l1: float, l2: float, x: float, y: float) -> dict:
        r2 = x * x + y * y
        cos2 = (r2 - l1 * l1 - l2 * l2) / (2 * l1 * l2)
        if abs(cos2) > 1:
            return {"error": "Unreachable target"}
        t2 = math.acos(cos2)
        t1 = math.atan2(y, x) - math.atan2(l2 * math.sin(t2), l1 + l2 * math.cos(t2))
        return {"theta1_deg": math.degrees(t1), "theta2_deg": math.degrees(t2)}

    def jacobian_2r(self, l1: float, l2: float, t1_deg: float, t2_deg: float) -> np.ndarray:
        t1, t2 = math.radians(t1_deg), math.radians(t2_deg)
        return np.array([
            [-l1 * math.sin(t1) - l2 * math.sin(t1 + t2), -l2 * math.sin(t1 + t2)],
            [l1 * math.cos(t1) + l2 * math.cos(t1 + t2), l2 * math.cos(t1 + t2)],
        ])

    def dh_transform(self, a: float, alpha: float, d: float, theta: float) -> np.ndarray:
        """Standard Denavit-Hartenberg transform."""
        ct, st = math.cos(theta), math.sin(theta)
        ca, sa = math.cos(alpha), math.sin(alpha)
        return np.array([
            [ct, -st * ca, st * sa, a * ct],
            [st, ct * ca, -ct * sa, a * st],
            [0, sa, ca, d],
            [0, 0, 0, 1],
        ])
