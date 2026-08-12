"""Robot simulator: dynamics and trajectory simulation."""

from __future__ import annotations

import math
import numpy as np


class RobotSimulator:
    def dynamics_2r(self, l1: float, l2: float, m1: float, m2: float,
                    q: list[float], qd: list[float], tau: list[float]) -> dict:
        """Simplified 2R arm dynamics: M(q)qdd + C(q,qd)qd + G(q) = tau."""
        t1, t2 = q
        td1, td2 = qd
        I1 = m1 * l1 ** 2 / 3
        I2 = m2 * l2 ** 2 / 3
        M = np.array([[I1 + I2 + m2 * l1 * l2 * math.cos(t2), I2 + 0.5 * m2 * l1 * l2 * math.cos(t2)],
                      [I2 + 0.5 * m2 * l1 * l2 * math.cos(t2), I2]])
        C = np.array([[-m2 * l1 * l2 * math.sin(t2) * td2 ** 2],
                      [0.5 * m2 * l1 * l2 * math.sin(t2) * td1 ** 2]])
        G = np.array([[m1 * 9.81 * (l1 / 2) * math.cos(t1) + m2 * 9.81 * (l1 * math.cos(t1) + (l2 / 2) * math.cos(t1 + t2))],
                      [m2 * 9.81 * (l2 / 2) * math.cos(t1 + t2)]])
        qdd = np.linalg.solve(M, np.array([[tau[0]], [tau[1]]]) - C - G)
        return {"M": M.tolist(), "C": C.tolist(), "G": G.tolist(),
                "qdd": qdd.flatten().tolist()}

    def trajectory_cubic(self, q0: float, qf: float, tf: float, n: int = 50) -> dict:
        a0, a1 = q0, 0.0
        a2 = 3 * (qf - q0) / tf ** 2
        a3 = -2 * (qf - q0) / tf ** 3
        times = [i * tf / n for i in range(n + 1)]
        positions = [a0 + a1 * t + a2 * t ** 2 + a3 * t ** 3 for t in times]
        return {"time": times, "position": positions}
