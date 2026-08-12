"""Find mathematical patterns and invariants in sequences."""

from __future__ import annotations

from typing import Any

import sympy as sp


def find_pattern(sequence: list[int | float]) -> dict[str, Any]:
    """Heuristically identify the kind of pattern in a sequence."""
    if len(sequence) < 2:
        return {"type": "unknown"}

    # arithmetic progression: constant difference
    diffs = [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]
    if len(set(diffs)) == 1:
        return {"type": "arithmetic", "common_difference": diffs[0]}

    # geometric progression: constant ratio
    if all(s != 0 for s in sequence[:-1]):
        ratios = [sequence[i + 1] / sequence[i] for i in range(len(sequence) - 1)]
        if all(abs(r - ratios[0]) < 1e-9 for r in ratios):
            return {"type": "geometric", "common_ratio": ratios[0]}

    # quadratic: constant second difference
    second = [diffs[i + 1] - diffs[i] for i in range(len(diffs) - 1)]
    if len(set(second)) == 1:
        return {"type": "quadratic", "second_difference": second[0]}

    # Fibonacci-like: a_n = a_{n-1} + a_{n-2}
    if len(sequence) >= 3 and all(
        abs(sequence[i] - sequence[i - 1] - sequence[i - 2]) < 1e-9 for i in range(2, len(sequence))
    ):
        return {"type": "fibonacci"}

    return {"type": "unknown", "first_differences": diffs, "second_differences": second}


def fit_polynomial(sequence: list[int | float]) -> Any | None:
    """Fit a polynomial to the sequence (index -> value) via Lagrange interpolation."""
    n = len(sequence)
    if n < 3:
        return None
    x = sp.Symbol("x")
    xs = list(range(n))
    try:
        poly = sp.interpolate(list(zip(xs, sequence)), x)
        if _fits(poly, sequence):
            return str(sp.expand(poly))
    except Exception:
        return None
    return None


def _fits(poly: Any, sequence: list[int | float]) -> bool:
    n = sp.Symbol("x")
    for i, val in enumerate(sequence):
        try:
            if abs(float(poly.subs(n, i)) - float(val)) > 1e-6:
                return False
        except Exception:
            return False
    return True


__all__ = ["find_pattern", "fit_polynomial"]
