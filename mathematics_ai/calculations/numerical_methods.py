"""ODE/PDE solvers and root-finding algorithms via SciPy."""

from __future__ import annotations

from typing import Any, Callable

import numpy as np
from scipy import integrate, optimize


def solve_ode(f: Callable[[float, np.ndarray], np.ndarray], y0: list[float], t_span: tuple[float, float], n_points: int = 100) -> dict[str, list[float]]:
    t_eval = np.linspace(t_span[0], t_span[1], n_points)
    sol = integrate.solve_ivp(f, t_span, y0, t_eval=t_eval, method="RK45")
    return {"t": sol.t.tolist(), "y": sol.y.tolist()}


def solve_ode_symbolic(expr: Any, var: str = "t", func: str = "x") -> Any:
    """Symbolic ODE solution via SymPy: solves expr = 0 where expr uses x(t)."""
    import sympy as sp
    t = sp.Symbol(var)
    x = sp.Function(func)
    eq = sp.Eq(sp.sympify(expr), 0) if "=" not in str(expr) else sp.sympify(expr)
    return sp.dsolve(sp.Eq(sp.sympify(expr), 0), x(t))


def root_find(f: Callable[[float], float], a: float, b: float, method: str = "brentq") -> float:
    if method == "brentq":
        return float(optimize.brentq(f, a, b))
    if method == "newton":
        x0 = (a + b) / 2
        return float(optimize.newton(f, x0))
    raise ValueError(f"unknown method {method}")


def minimize_scalar(f: Callable[[float], float], bounds: tuple[float, float] | None = None) -> dict[str, float]:
    if bounds:
        res = optimize.minimize_scalar(f, bounds=bounds, method="bounded")
    else:
        res = optimize.minimize_scalar(f)
    return {"x": float(res.x), "fun": float(res.fun)}


def trapezoid_integrate(f: Callable[[float], float], a: float, b: float, n: int = 1000) -> float:
    xs = np.linspace(a, b, n + 1)
    ys = np.array([f(x) for x in xs])
    return float(np.trapezoid(ys, xs))


def simpson_integrate(f: Callable[[float], float], a: float, b: float, n: int = 1000) -> float:
    if n % 2 == 1:
        n += 1
    xs = np.linspace(a, b, n + 1)
    ys = np.array([f(x) for x in xs])
    h = (b - a) / n
    return float(h / 3 * (ys[0] + 4 * ys[1:-1:2].sum() + 2 * ys[2:-1:2].sum() + ys[-1]))


def heat_equation_1d(L: float = 1.0, T: float = 0.1, nx: int = 50, nt: int = 500, alpha: float = 1.0) -> dict[str, list]:
    """Solve u_t = alpha u_xx on [0,L] with zero boundary conditions via FTCS."""
    dx = L / (nx - 1)
    dt = T / nt
    if dt > 0.5 * dx ** 2 / alpha:
        dt = 0.4 * dx ** 2 / alpha  # stability
    u = np.zeros((nt, nx))
    u[0, nx // 2] = 1.0  # initial heat spike
    r = alpha * dt / dx ** 2
    for n in range(nt - 1):
        u[n + 1, 1:-1] = u[n, 1:-1] + r * (u[n, 2:] - 2 * u[n, 1:-1] + u[n, :-2])
    return {"t_steps": nt, "x_steps": nx, "u": u[-1].tolist()}


__all__ = [
    "solve_ode", "solve_ode_symbolic", "root_find", "minimize_scalar",
    "trapezoid_integrate", "simpson_integrate", "heat_equation_1d",
]
