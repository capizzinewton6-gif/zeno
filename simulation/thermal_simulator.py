"""Thermal simulator: heat conduction, convection, and transient response."""

from __future__ import annotations

import math


class ThermalSimulator:
    def steady_conduction_wall(self, k: float, area: float, thickness: float,
                               t_hot: float, t_cold: float) -> dict:
        q = k * area * (t_hot - t_cold) / thickness
        return {"heat_transfer_W": q, "resistance_K_per_W": thickness / (k * area)}

    def lumped_capacitance(self, rho: float, cp: float, volume: float, area: float,
                           h: float, t_initial: float, t_inf: float,
                           t_end: float = 100.0, dt: float = 1.0) -> dict:
        m = rho * volume
        tau = (rho * cp * volume) / (h * area)  # time constant
        steps = int(t_end / dt)
        times = [i * dt for i in range(steps)]
        temps = [(t_initial - t_inf) * math.exp(-t / tau) + t_inf for t in times]
        return {"time": times, "temperature": temps, "tau": tau,
                "biot": (h * (volume / area)) / k if 'k' in dir() else None}

    def fin_efficiency(self, h: float, k: float, length: float, thickness: float,
                        perimeter: float) -> dict:
        import numpy as np
        area = thickness * (perimeter / 2 if perimeter else 1.0)
        m = math.sqrt(h * perimeter / (k * area))
        eta = math.tanh(m * length) / (m * length) if m * length else 1.0
        return {"m": m, "efficiency": float(eta)}

    def thermal_resistance_network(self, resistances: list[float], parallel: bool = False) -> float:
        if parallel:
            return 1.0 / sum(1.0 / r for r in resistances)
        return sum(resistances)
