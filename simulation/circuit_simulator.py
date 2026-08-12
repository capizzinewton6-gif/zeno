"""Electronic circuit simulator: transient and DC analysis."""

from __future__ import annotations

import math


class CircuitSimulator:
    def rc_transient(self, v_source: float, r: float, c: float, t_end: float = 5.0,
                     dt: float = 0.01) -> dict:
        tau = r * c
        steps = int(t_end / dt)
        times = [i * dt for i in range(steps)]
        voltages = [v_source * (1 - math.exp(-t / tau)) for t in times]
        currents = [(v_source / r) * math.exp(-t / tau) for t in times]
        return {"time": times, "capacitor_voltage": voltages,
                "current": currents, "tau": tau}

    def rl_transient(self, v_source: float, r: float, l: float, t_end: float = 5.0,
                     dt: float = 0.01) -> dict:
        tau = l / r
        steps = int(t_end / dt)
        times = [i * dt for i in range(steps)]
        currents = [(v_source / r) * (1 - math.exp(-t / tau)) for t in times]
        voltages = [v_source * math.exp(-t / tau) for t in times]
        return {"time": times, "current": currents,
                "inductor_voltage": voltages, "tau": tau}

    def dc_node_analysis(self, conductances: list[list[float]],
                         currents: list[float]) -> list[float]:
        """Solve G*V = I for node voltages."""
        import numpy as np
        G = np.array(conductances, dtype=float)
        I = np.array(currents, dtype=float)
        return np.linalg.solve(G, I).tolist()

    def rlc_natural(self, r: float, l: float, c: float, x0: float = 1.0,
                    t_end: float = 5.0, dt: float = 0.01) -> dict:
        alpha = r / (2 * l)
        omega0 = 1 / math.sqrt(l * c)
        steps = int(t_end / dt)
        times = [i * dt for i in range(steps)]
        if alpha < omega0:  # underdamped
            wd = math.sqrt(omega0 ** 2 - alpha ** 2)
            volts = [x0 * math.exp(-alpha * t) * math.cos(wd * t) for t in times]
            damping = "underdamped"
        elif alpha > omega0:
            s1 = -alpha + math.sqrt(alpha ** 2 - omega0 ** 2)
            s2 = -alpha - math.sqrt(alpha ** 2 - omega0 ** 2)
            volts = [x0 * 0.5 * (math.exp(s1 * t) + math.exp(s2 * t)) for t in times]
            damping = "overdamped"
        else:
            volts = [x0 * (1 + alpha * t) * math.exp(-alpha * t) for t in times]
            damping = "critically damped"
        return {"time": times, "voltage": volts, "damping": damping}
