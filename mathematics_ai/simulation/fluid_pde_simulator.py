"""Navier-Stokes and partial differential equation solvers (2-D, FTCS)."""

from __future__ import annotations

import numpy as np


def diffusion_2d(nx: int = 50, ny: int = 50, nt: int = 100, D: float = 1.0, dx: float = 0.1, dy: float = 0.1, dt: float | None = None) -> list[list[float]]:
    """Solve u_t = D (u_xx + u_yy) with an initial Gaussian spike."""
    if dt is None:
        dt = 0.2 * min(dx, dy) ** 2 / D
    u = np.zeros((nx, ny))
    u[nx // 2, ny // 2] = 1.0
    rx = D * dt / dx ** 2
    ry = D * dt / dy ** 2
    for _ in range(nt):
        u_new = u.copy()
        u_new[1:-1, 1:-1] = (u[1:-1, 1:-1]
                             + rx * (u[2:, 1:-1] - 2 * u[1:-1, 1:-1] + u[:-2, 1:-1])
                             + ry * (u[1:-1, 2:] - 2 * u[1:-1, 1:-1] + u[1:-1, :-2]))
        u = u_new
    return u.tolist()


def wave_1d(nx: int = 100, nt: int = 200, c: float = 1.0, dx: float = 0.1, dt: float | None = None) -> dict[str, list]:
    """1-D wave equation u_tt = c^2 u_xx via leapfrog."""
    if dt is None:
        dt = 0.4 * dx / c
    u = np.zeros(nx)
    u[nx // 4: nx // 2] = 1.0  # initial displacement
    u_prev = u.copy()
    r = (c * dt / dx) ** 2
    history = [u.copy()]
    for _ in range(nt):
        u_new = u.copy()
        u_new[1:-1] = (2 * u[1:-1] - u_prev[1:-1]
                       + r * (u[2:] - 2 * u[1:-1] + u[:-2]))
        u_prev, u = u, u_new
        history.append(u.copy())
    return {"t_steps": nt, "final": u.tolist(), "history": [h.tolist() for h in history[::max(1, nt // 50)]]}


def burgers_1d(nx: int = 100, nt: int = 200, nu: float = 0.01, dx: float = 0.1, dt: float = 0.01) -> list[float]:
    """1-D viscous Burgers' equation u_t + u u_x = ν u_xx."""
    u = np.zeros(nx)
    u[:nx // 2] = 1.0
    for _ in range(nt):
        un = u.copy()
        u[1:-1] = (un[1:-1]
                   - un[1:-1] * dt / (2 * dx) * (un[2:] - un[:-2])
                   + nu * dt / dx ** 2 * (un[2:] - 2 * un[1:-1] + un[:-2]))
    return u.tolist()


def laplace_2d(nx: int = 30, ny: int = 30, iterations: int = 500) -> list[list[float]]:
    """Solve Laplace's equation ∇²u = 0 with Jacobi iteration."""
    u = np.zeros((nx, ny))
    u[0, :] = 1.0  # top boundary
    for _ in range(iterations):
        u[1:-1, 1:-1] = 0.25 * (u[2:, 1:-1] + u[:-2, 1:-1] + u[1:-1, 2:] + u[1:-1, :-2])
    return u.tolist()


def poisson_2d(f: list[list[float]] | None = None, nx: int = 30, ny: int = 30, iterations: int = 500) -> list[list[float]]:
    """Solve ∇²u = f with Jacobi iteration (homogeneous Dirichlet BC)."""
    u = np.zeros((nx, ny))
    rhs = np.array(f, dtype=float) if f is not None else np.zeros((nx, ny))
    for _ in range(iterations):
        u[1:-1, 1:-1] = 0.25 * (u[2:, 1:-1] + u[:-2, 1:-1] + u[1:-1, 2:] + u[1:-1, :-2] - rhs[1:-1, 1:-1])
    return u.tolist()


__all__ = ["diffusion_2d", "wave_1d", "burgers_1d", "laplace_2d", "poisson_2d"]
