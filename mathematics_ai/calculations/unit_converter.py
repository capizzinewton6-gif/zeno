"""Scale, base and coordinate system conversions."""

from __future__ import annotations

import math
from typing import Any


# --- base conversions ----------------------------------------------
def to_base(n: int, base: int = 2) -> str:
    if n == 0:
        return "0"
    if base < 2 or base > 36:
        raise ValueError("base must be 2..36")
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    neg = n < 0
    n = abs(n)
    out = ""
    while n:
        out = digits[n % base] + out
        n //= base
    return ("-" + out) if neg else out


def from_base(s: str, base: int = 2) -> int:
    return int(s, base)


# --- temperature / metric scale conversions -------------------------
def celsius_to_fahrenheit(c: float) -> float:
    return c * 9 / 5 + 32


def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) * 5 / 9


# --- coordinate system conversions ----------------------------------
def cartesian_to_polar(x: float, y: float) -> tuple[float, float]:
    return math.hypot(x, y), math.atan2(y, x)


def polar_to_cartesian(r: float, theta: float) -> tuple[float, float]:
    return r * math.cos(theta), r * math.sin(theta)


def cartesian_to_spherical(x: float, y: float, z: float) -> tuple[float, float, float]:
    r = math.sqrt(x * x + y * y + z * z)
    theta = math.acos(z / r) if r != 0 else 0
    phi = math.atan2(y, x)
    return r, theta, phi


def spherical_to_cartesian(r: float, theta: float, phi: float) -> tuple[float, float, float]:
    x = r * math.sin(theta) * math.cos(phi)
    y = r * math.sin(theta) * math.sin(phi)
    z = r * math.cos(theta)
    return x, y, z


def cartesian_to_cylindrical(x: float, y: float, z: float) -> tuple[float, float, float]:
    r, theta = cartesian_to_polar(x, y)
    return r, theta, z


def cylindrical_to_cartesian(r: float, theta: float, z: float) -> tuple[float, float, float]:
    x, y = polar_to_cartesian(r, theta)
    return x, y, z


# --- angle units ----------------------------------------------------
def degrees_to_radians(d: float) -> float:
    return math.radians(d)


def radians_to_degrees(r: float) -> float:
    return math.degrees(r)


__all__ = [
    "to_base", "from_base", "celsius_to_fahrenheit", "fahrenheit_to_celsius",
    "cartesian_to_polar", "polar_to_cartesian", "cartesian_to_spherical",
    "spherical_to_cartesian", "cartesian_to_cylindrical",
    "cylindrical_to_cartesian", "degrees_to_radians", "radians_to_degrees",
]
