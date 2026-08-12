"""Sequences, series and 1-D dynamical systems."""

from __future__ import annotations

from typing import Any, Callable

import sympy as sp


def arithmetic_sequence(a0: float, d: float, n: int) -> list[float]:
    return [a0 + i * d for i in range(n)]


def geometric_sequence(a0: float, r: float, n: int) -> list[float]:
    return [a0 * (r ** i) for i in range(n)]


def fibonacci_sequence(n: int) -> list[int]:
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]


def series_sum(seq: list[float]) -> float:
    return sum(seq)


def partial_sums(seq: list[float]) -> list[float]:
    out = []
    s = 0.0
    for x in seq:
        s += x
        out.append(s)
    return out


def convergence_test(seq: list[float]) -> dict[str, Any]:
    """Heuristic convergence test for a sequence (not series)."""
    if len(seq) < 4:
        return {"converges": None, "reason": "insufficient terms"}
    diffs = [abs(seq[i + 1] - seq[i]) for i in range(len(seq) - 1)]
    if all(d < 1e-9 for d in diffs[-3:]):
        return {"converges": True, "limit": seq[-1], "reason": "successive differences vanishing"}
    if all(diffs[i] < diffs[i - 1] for i in range(1, len(diffs))):
        return {"converges": True, "limit": seq[-1], "reason": "monotone decreasing differences"}
    return {"converges": None, "reason": "inconclusive"}


def iterate_map(f: Callable[[float], float], x0: float, n: int) -> list[float]:
    """Iterate a 1-D dynamical system x_{n+1} = f(x_n)."""
    out = [x0]
    x = x0
    for _ in range(n):
        x = f(x)
        out.append(x)
    return out


def find_fixed_point(f: Callable[[float], float], x0: float = 0.0, tol: float = 1e-10, max_iter: int = 1000) -> float | None:
    x = x0
    for _ in range(max_iter):
        nx = f(x)
        if abs(nx - x) < tol:
            return nx
        x = nx
    return None


def nth_term_formula(seq: list[float]) -> Any | None:
    """Try to find a closed-form for the n-th term via interpolation."""
    if len(seq) < 3:
        return None
    x = sp.Symbol("n")
    try:
        poly = sp.interpolate(list(zip(range(len(seq)), seq)), x)
        return sp.expand(poly)
    except Exception:
        return None


__all__ = [
    "arithmetic_sequence", "geometric_sequence", "fibonacci_sequence",
    "series_sum", "partial_sums", "convergence_test", "iterate_map",
    "find_fixed_point", "nth_term_formula",
]
