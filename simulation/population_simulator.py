"""Predator-prey (Lotka-Volterra) and ecological simulations."""
from __future__ import annotations

import math


class LotkaVolterraSimulator:
    def run(self, prey0=40, predator0=9, alpha=0.1, beta=0.02,
            delta=0.01, gamma=0.1, days=200, dt=0.1) -> dict:
        prey, predator = float(prey0), float(predator0)
        history = {"time": [], "prey": [], "predator": []}
        t = 0.0
        steps = max(int(days / dt), 1)
        # record at integer time points (tolerant of float accumulation)
        next_record = 1.0
        eps = dt / 2.0
        for _ in range(steps):
            d_prey = prey * (alpha - beta * predator) * dt
            d_pred = predator * (-gamma + delta * prey) * dt
            prey = max(prey + d_prey, 0.0)
            predator = max(predator + d_pred, 0.0)
            t += dt
            if t >= next_record - eps:
                history["time"].append(round(t))
                history["prey"].append(round(prey, 3))
                history["predator"].append(round(predator, 3))
                next_record += 1.0
        return {"params": dict(prey0=prey0, predator0=predator0, alpha=alpha,
                               beta=beta, delta=delta, gamma=gamma, days=days),
                **history}


class LogisticGrowthSimulator:
    def run(self, n0=10, carrying_capacity=500, rate=0.5, days=50, dt=0.5) -> dict:
        n = float(n0)
        history = {"time": [], "population": []}
        t = 0.0
        steps = max(int(days / dt), 1)
        next_record = 1.0
        eps = dt / 2.0
        for _ in range(steps):
            dn = rate * n * (1 - n / carrying_capacity) * dt
            n += dn
            t += dt
            if t >= next_record - eps:
                history["time"].append(round(t))
                history["population"].append(round(n, 3))
                next_record += 1.0
        return {"carrying_capacity": carrying_capacity, "rate": rate, **history}
