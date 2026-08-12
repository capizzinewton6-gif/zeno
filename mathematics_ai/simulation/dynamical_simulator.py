"""Chaos theory, attractors and bifurcation diagrams."""

from __future__ import annotations

from typing import Callable

import numpy as np


def logistic_map(r: float, x0: float = 0.5, n: int = 100, transient: int = 0) -> list[float]:
    """Iterate the logistic map x_{n+1} = r x_n (1 - x_n)."""
    x = x0
    for _ in range(transient):
        x = r * x * (1 - x)
    out = []
    for _ in range(n):
        x = r * x * (1 - x)
        out.append(x)
    return out


def bifurcation_diagram(f: Callable[[float, float], float], r_min: float, r_max: float, n_r: int = 200, n_iter: int = 300, n_samples: int = 50, x0: float = 0.5) -> dict[str, list]:
    """Bifurcation diagram: for each r, sample f after a transient."""
    rs = np.linspace(r_min, r_max, n_r)
    points_r: list[float] = []
    points_x: list[float] = []
    for r in rs:
        x = x0
        for _ in range(n_iter - n_samples):
            x = f(r, x)
        for _ in range(n_samples):
            x = f(r, x)
            points_r.append(float(r))
            points_x.append(float(x))
    return {"r": points_r, "x": points_x}


def lyapunov_exponent_1d(f: Callable[[float, float], float], fprime: Callable[[float, float], float], r: float, x0: float = 0.5, n: int = 1000) -> float:
    """Estimate the Lyapunov exponent of a 1-D map."""
    x = x0
    s = 0.0
    for _ in range(n):
        s += np.log(abs(fprime(r, x)) + 1e-12)
        x = f(r, x)
    return s / n


def lorenz_attractor(sigma: float = 10, rho: float = 28, beta: float = 8 / 3, t_span: tuple[float, float] = (0, 40), n: int = 5000) -> dict[str, list]:
    """Integrate the Lorenz system."""
    from scipy.integrate import solve_ivp
    def system(t, state):
        x, y, z = state
        return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]
    t_eval = np.linspace(*t_span, n)
    sol = solve_ivp(system, t_span, [1.0, 1.0, 1.0], t_eval=t_eval)
    return {"t": sol.t.tolist(), "x": sol.y[0].tolist(), "y": sol.y[1].tolist(), "z": sol.y[2].tolist()}


def henon_map(a: float = 1.4, b: float = 0.3, x0: float = 0.0, y0: float = 0.0, n: int = 5000, transient: int = 1000) -> dict[str, list]:
    """Hénon attractor: x_{n+1} = 1 - a x_n^2 + y_n, y_{n+1} = b x_n."""
    x, y = x0, y0
    for _ in range(transient):
        x, y = 1 - a * x * x + y, b * x
    xs, ys = [], []
    for _ in range(n):
        x, y = 1 - a * x * x + y, b * x
        xs.append(x); ys.append(y)
    return {"x": xs, "y": ys}


def double_pendulum(theta1_0: float = np.pi / 2, theta2_0: float = np.pi / 2, t_span: tuple[float, float] = (0, 10), n: int = 2000) -> dict[str, list]:
    """Double pendulum equations of motion (unit lengths/masses, g=9.81)."""
    from scipy.integrate import solve_ivp
    g = 9.81
    def deriv(t, s):
        t1, t2, p1, p2 = s
        delta = t2 - t1
        den = 2 - np.cos(delta)
        ddt1 = (6 * p1 - 6 * p2 * np.cos(delta)) / (16 - 8 * np.cos(delta) ** 2)
        ddt2 = (6 * p2 - 6 * p1 * np.cos(delta)) / (16 - 8 * np.cos(delta) ** 2)
        dp1 = -0.5 * (2 * 9.81) * np.sin(t1) - 0.5 * ddt1 * ddt2 * np.sin(delta) - 0.5 * np.cos(delta) * (ddt1 ** 2 + 2 * 9.81 * np.sin(t2)) * 0
        dp2 = -9.81 * np.sin(t2) + 0.5 * np.sin(delta) * (ddt1 ** 2) + 0
        return [ddt1, ddt2, dp1, dp2]
    t_eval = np.linspace(*t_span, n)
    sol = solve_ivp(deriv, t_span, [theta1_0, theta2_0, 0, 0], t_eval=t_eval)
    return {"t": sol.t.tolist(), "theta1": sol.y[0].tolist(), "theta2": sol.y[1].tolist()}


__all__ = [
    "logistic_map", "bifurcation_diagram", "lyapunov_exponent_1d",
    "lorenz_attractor", "henon_map", "double_pendulum",
]
