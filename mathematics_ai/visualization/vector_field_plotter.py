"""Plot direction fields, phase portraits and flows."""

from __future__ import annotations

from typing import Callable

import numpy as np


def direction_field(fx: Callable[[float, float], float], fy: Callable[[float, float], float],
                    x_range=(-3, 3), y_range=(-3, 3), resolution=15):
    """Generate a direction field for the system dx/dt=fx, dy/dt=fy."""
    xs = np.linspace(*x_range, resolution)
    ys = np.linspace(*y_range, resolution)
    X, Y = np.meshgrid(xs, ys)
    U = np.vectorize(fx)(X, Y)
    V = np.vectorize(fy)(X, Y)
    # normalize arrows
    M = np.sqrt(U ** 2 + V ** 2)
    M[M == 0] = 1
    return {"x": X.tolist(), "y": Y.tolist(), "u": (U / M).tolist(), "v": (V / M).tolist()}


def phase_portrait(fx, fy, initial_conditions, t_end=10, dt=0.01):
    """Integrate trajectories for the system."""
    trajectories = []
    for x0, y0 in initial_conditions:
        x, y = x0, y0
        traj = [(x, y)]
        t = 0
        while t < t_end:
            dx, dy = fx(x, y), fy(x, y)
            x += dx * dt
            y += dy * dt
            traj.append((x, y))
            t += dt
        trajectories.append(traj)
    return trajectories


def find_equilibria(fx: Callable, fy: Callable, grid_points=20, x_range=(-3, 3), y_range=(-3, 3)):
    """Find approximate equilibria (where fx≈0 and fy≈0)."""
    xs = np.linspace(*x_range, grid_points)
    ys = np.linspace(*y_range, grid_points)
    eqs = []
    for x in xs:
        for y in ys:
            if abs(fx(x, y)) < 0.05 and abs(fy(x, y)) < 0.05:
                eqs.append((float(x), float(y)))
    return eqs


def classify_equilibrium(fx, fy, x0, y0, eps=1e-5):
    """Classify an equilibrium via the Jacobian eigenvalues."""
    a = (fx(x0 + eps, y0) - fx(x0 - eps, y0)) / (2 * eps)
    b = (fx(x0, y0 + eps) - fx(x0, y0 - eps)) / (2 * eps)
    c = (fy(x0 + eps, y0) - fy(x0 - eps, y0)) / (2 * eps)
    d = (fy(x0, y0 + eps) - fy(x0, y0 - eps)) / (2 * eps)
    J = np.array([[a, b], [c, d]])
    eigvals = np.linalg.eigvals(J)
    types = []
    if all(e.real > 0 for e in eigvals):
        types.append("unstable_node")
    elif all(e.real < 0 for e in eigvals):
        types.append("stable_node")
    else:
        types.append("saddle")
    if any(abs(e.imag) > 1e-9 for e in eigvals):
        types.append("spiral")
    return {"jacobian": J.tolist(), "eigenvalues": eigvals.tolist(), "type": types}


__all__ = ["direction_field", "phase_portrait", "find_equilibria", "classify_equilibrium"]
