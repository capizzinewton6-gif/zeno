"""Robot simulator: forward kinematics and trajectory generation."""

from __future__ import annotations

import math


class RobotSimulator:
    def forward_2r(self, l1: float, l2: float, theta1_deg: float,
                   theta2_deg: float) -> dict:
        t1 = math.radians(theta1_deg)
        t2 = math.radians(theta2_deg)
        x = l1 * math.cos(t1) + l2 * math.cos(t1 + t2)
        y = l1 * math.sin(t1) + l2 * math.sin(t1 + t2)
        return {"x": x, "y": y, "theta_end_deg": math.degrees(t1 + t2)}

    def inverse_2r(self, l1: float, l2: float, x: float, y: float) -> dict:
        """Return joint angles (degrees) for a 2R arm reaching (x, y)."""
        d2 = x * x + y * y
        cos2 = (d2 - l1 ** 2 - l2 ** 2) / (2 * l1 * l2)
        if abs(cos2) > 1:
            return {"error": "Target out of reach"}
        theta2 = math.acos(cos2)
        theta1 = math.atan2(y, x) - math.atan2(l2 * math.sin(theta2),
                                               l1 + l2 * math.cos(theta2))
        return {"theta1_deg": math.degrees(theta1),
                "theta2_deg": math.degrees(theta2)}

    def joint_trajectory(self, q0: float, qf: float, tf: float,
                         n: int = 50) -> dict:
        """Cubic polynomial trajectory: q(t) = a0+a1 t+a2 t^2+a3 t^3."""
        a0 = q0
        a1 = 0
        a2 = 3 * (qf - q0) / tf ** 2
        a3 = -2 * (qf - q0) / tf ** 3
        times = [i * tf / n for i in range(n + 1)]
        positions = [a0 + a1 * t + a2 * t ** 2 + a3 * t ** 3 for t in times]
        return {"time": times, "position": positions}
