"""Convex, integer, non-linear and semidefinite programming solvers."""

from __future__ import annotations

from typing import Any, Callable

import numpy as np
from scipy import optimize


def minimize_nonlinear(f: Callable[[list[float]], float], x0: list[float], method: str = "BFGS") -> dict[str, Any]:
    res = optimize.minimize(f, np.array(x0, dtype=float), method=method)
    return {"x": res.x.tolist(), "fun": float(res.fun), "success": bool(res.success), "message": res.message}


def linear_program(c: list[float], A_ub: list[list[float]] | None = None, b_ub: list[float] | None = None, A_eq: list[list[float]] | None = None, b_eq: list[float] | None = None) -> dict[str, Any]:
    """Minimize c·x subject to A_ub x ≤ b_ub, A_eq x = b_eq (x ≥ 0)."""
    res = optimize.linprog(
        c=np.array(c, dtype=float),
        A_ub=np.array(A_ub, dtype=float) if A_ub else None,
        b_ub=np.array(b_ub, dtype=float) if b_ub else None,
        A_eq=np.array(A_eq, dtype=float) if A_eq else None,
        b_eq=np.array(b_eq, dtype=float) if b_eq else None,
        method="highs",
    )
    return {"x": res.x.tolist() if res.x is not None else None, "fun": float(res.fun) if res.fun is not None else None,
            "success": bool(res.success), "message": res.message}


def least_squares_curve_fit(f: Callable, xdata: list[float], ydata: list[float], p0: list[float] | None = None) -> dict[str, Any]:
    popt, pcov = optimize.curve_fit(f, np.array(xdata, dtype=float), np.array(ydata, dtype=float), p0=p0)
    return {"params": popt.tolist(), "covariance": pcov.tolist()}


def quadratic_program(H: list[list[float]], f: list[float]) -> dict[str, Any]:
    """Minimize (1/2) x^T H x + f^T x via a generic unconstrained solver."""
    H_arr = np.array(H, dtype=float)
    f_arr = np.array(f, dtype=float)
    def obj(x):
        return 0.5 * x @ H_arr @ x + f_arr @ x
    res = optimize.minimize(obj, np.zeros(len(f_arr)), method="BFGS")
    return {"x": res.x.tolist(), "fun": float(res.fun)}


def convex_constrained(f: Callable[[list[float]], float], bounds: list[tuple[float, float]], x0: list[float]) -> dict[str, Any]:
    res = optimize.minimize(f, np.array(x0, dtype=float), method="SLSQP", bounds=bounds)
    return {"x": res.x.tolist(), "fun": float(res.fun), "success": bool(res.success)}


def integer_program(c: list[float], bounds: list[tuple[int, int]]) -> dict[str, Any]:
    """Naive integer program via brute-force over bounded integer grid.

    For small problems only. Returns the argmin of c·x over the integer box.
    """
    import itertools
    ranges = [range(lo, hi + 1) for lo, hi in bounds]
    best_x, best_val = None, float("inf")
    for x in itertools.product(*ranges):
        val = sum(ci * xi for ci, xi in zip(c, x))
        if val < best_val:
            best_val, best_x = val, list(x)
    return {"x": best_x, "fun": best_val}


__all__ = [
    "minimize_nonlinear", "linear_program", "least_squares_curve_fit",
    "quadratic_program", "convex_constrained", "integer_program",
]
