"""Multi-precision decimal and rational arithmetic via mpmath."""

from __future__ import annotations

from typing import Any

import mpmath


def set_precision(digits: int) -> None:
    mpmath.mp.dps = digits


def get_precision() -> int:
    return mpmath.mp.dps


def mpf(value: Any) -> mpmath.mpf:
    return mpmath.mpf(value)


def pi(digits: int = 50) -> str:
    old = mpmath.mp.dps
    mpmath.mp.dps = digits
    try:
        return mpmath.nstr(mpmath.pi, digits)
    finally:
        mpmath.mp.dps = old


def e(digits: int = 50) -> str:
    old = mpmath.mp.dps
    mpmath.mp.dps = digits
    try:
        return mpmath.nstr(mpmath.e, digits)
    finally:
        mpmath.mp.dps = old


def sqrt_high_precision(x: Any, digits: int = 50) -> str:
    old = mpmath.mp.dps
    mpmath.mp.dps = digits
    try:
        return mpmath.nstr(mpmath.sqrt(mpmath.mpf(x)), digits)
    finally:
        mpmath.mp.dps = old


def exp_high_precision(x: Any, digits: int = 50) -> str:
    old = mpmath.mp.dps
    mpmath.mp.dps = digits
    try:
        return mpmath.nstr(mpmath.exp(mpmath.mpf(x)), digits)
    finally:
        mpmath.mp.dps = old


def rational_to_decimal(numerator: int, denominator: int, digits: int = 50) -> str:
    old = mpmath.mp.dps
    mpmath.mp.dps = digits
    try:
        return mpmath.nstr(mpmath.mpf(numerator) / mpmath.mpf(denominator), digits)
    finally:
        mpmath.mp.dps = old


def gamma_high_precision(x: Any, digits: int = 50) -> str:
    old = mpmath.mp.dps
    mpmath.mp.dps = digits
    try:
        return mpmath.nstr(mpmath.gamma(mpmath.mpf(x)), digits)
    finally:
        mpmath.mp.dps = old


def zeta_high_precision(s: Any, digits: int = 50) -> str:
    old = mpmath.mp.dps
    mpmath.mp.dps = digits
    try:
        return mpmath.nstr(mpmath.zeta(mpmath.mpf(s)), digits)
    finally:
        mpmath.mp.dps = old


__all__ = [
    "set_precision", "get_precision", "mpf", "pi", "e", "sqrt_high_precision",
    "exp_high_precision", "rational_to_decimal", "gamma_high_precision",
    "zeta_high_precision",
]
