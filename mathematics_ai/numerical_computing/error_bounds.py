"""Interval arithmetic and rigorous numerical error estimation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Interval:
    """A closed interval [lo, hi]."""
    lo: float
    hi: float

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            self.lo, self.hi = self.hi, self.lo

    @property
    def width(self) -> float:
        return self.hi - self.lo

    @property
    def midpoint(self) -> float:
        return (self.lo + self.hi) / 2

    def __add__(self, other: "Interval") -> "Interval":
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def __sub__(self, other: "Interval") -> "Interval":
        return Interval(self.lo - other.hi, self.hi - other.lo)

    def __mul__(self, other: "Interval") -> "Interval":
        products = [self.lo * other.lo, self.lo * other.hi, self.hi * other.lo, self.hi * other.hi]
        return Interval(min(products), max(products))

    def __contains__(self, x: float) -> bool:
        return self.lo <= x <= self.hi

    def __repr__(self) -> str:
        return f"[{self.lo}, {self.hi}]"


def from_tolerance(center: float, tol: float) -> Interval:
    return Interval(center - tol, center + tol)


def error_bound(value: float, tol: float) -> Interval:
    return from_tolerance(value, tol)


def relative_error(approx: float, exact: float) -> float:
    if exact == 0:
        return float("inf") if approx != 0 else 0.0
    return abs((approx - exact) / exact)


def absolute_error(approx: float, exact: float) -> float:
    return abs(approx - exact)


def propagate_add(a: Interval, b: Interval) -> Interval:
    return a + b


def propagate_mul(a: Interval, b: Interval) -> Interval:
    return a * b


def taylor_remainder_bound(max_derivative: float, h: float, order: int) -> float:
    """Lagrange remainder |R_n| ≤ M * |h|^(n+1) / (n+1)!."""
    import math
    return max_derivative * abs(h) ** (order + 1) / math.factorial(order + 1)


__all__ = [
    "Interval", "from_tolerance", "error_bound", "relative_error",
    "absolute_error", "propagate_add", "propagate_mul", "taylor_remainder_bound",
]
