"""Physics-based simulations: kinematics, dynamics, and field problems."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

GRAVITY = 9.80665


@dataclass
class ProjectileResult:
    times: list
    x: list
    y: list
    range: float
    max_height: float
    flight_time: float


class PhysicsSimulator:
    def projectile(self, v0: float, angle_deg: float, dt: float = 0.01,
                   g: float = GRAVITY) -> ProjectileResult:
        angle = math.radians(angle_deg)
        vx = v0 * math.cos(angle)
        vy = v0 * math.sin(angle)
        t, x, y = 0.0, 0.0, 0.0
        times, xs, ys = [t], [x], [y]
        while y >= 0:
            t += dt
            x = vx * t
            y = vy * t - 0.5 * g * t ** 2
            if y < 0:
                break
            times.append(t)
            xs.append(x)
            ys.append(y)
        rng = v0 ** 2 * math.sin(2 * angle) / g
        h_max = (v0 * math.sin(angle)) ** 2 / (2 * g)
        tof = 2 * v0 * math.sin(angle) / g
        return ProjectileResult(times, xs, ys, rng, h_max, tof)

    def spring_mass(self, m: float, k: float, x0: float, t_end: float = 5.0,
                    dt: float = 0.01) -> dict:
        omega = math.sqrt(k / m)
        steps = int(t_end / dt)
        times = [i * dt for i in range(steps)]
        positions = [x0 * math.cos(omega * t) for t in times]
        return {"time": times, "position": positions,
                "natural_frequency": omega, "period": 2 * math.pi / omega}

    def heat_diffusion_1d(self, length: float, dx: float, dt: float, alpha: float,
                          t_steps: int, initial: list[float],
                          boundary: tuple[float, float]) -> list[list[float]]:
        nx = int(length / dx) + 1
        u = list(initial[:nx])
        if len(u) < nx:
            u += [0.0] * (nx - len(u))
        u[0], u[-1] = boundary
        results = [list(u)]
        for _ in range(t_steps):
            un = list(u)
            for i in range(1, nx - 1):
                un[i] = u[i] + alpha * dt / dx ** 2 * (u[i + 1] - 2 * u[i] + u[i - 1])
            un[0], un[-1] = boundary
            u = un
            results.append(list(u))
        return results
