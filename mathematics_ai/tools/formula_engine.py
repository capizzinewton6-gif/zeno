"""Evaluate mathematical expressions and verify identities."""

from __future__ import annotations

from typing import Any

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

_TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application, convert_xor)


def _parse(expr: Any) -> sp.Expr:
    if isinstance(expr, str):
        return parse_expr(expr, transformations=_TRANSFORMATIONS)
    return sp.sympify(expr)


def evaluate(expr: Any, subs: dict[str, Any] | None = None) -> Any:
    """Evaluate a symbolic expression, substituting any variables."""
    e = _parse(expr)
    if subs:
        e = e.subs({sp.Symbol(k): v for k, v in subs.items()})
    if e.is_number:
        return complex(e) if e.is_complex else float(e)
    return e


def verify_identity(lhs: Any, rhs: Any, var: str | None = None) -> bool:
    """Verify lhs ≡ rhs symbolically."""
    diff = sp.simplify(_parse(lhs) - _parse(rhs))
    if diff == 0:
        return True
    # try numeric spot checks at several points
    if var:
        v = sp.Symbol(var)
        for val in [-1.234, 0.5, 2.7, 7]:
            try:
                l = float(_parse(lhs).subs(v, val))
                r = float(_parse(rhs).subs(v, val))
                if abs(l - r) > 1e-9:
                    return False
            except Exception:
                return False
        return True
    return False


def substitute(expr: Any, subs: dict[str, Any]) -> Any:
    return _parse(expr).subs({sp.Symbol(k): v for k, v in subs.items()})


def numerical_value(expr: Any, subs: dict[str, Any] | None = None) -> complex:
    e = _parse(expr)
    if subs:
        e = e.subs({sp.Symbol(k): v for k, v in subs.items()})
    val = sp.N(e)
    try:
        return float(val)
    except (TypeError, ValueError):
        return complex(val)


def expand(expr: Any) -> Any:
    return sp.expand(_parse(expr))


def collect_terms(expr: Any, var: str = "x") -> Any:
    return sp.collect(_parse(expr), sp.Symbol(var))


def is_constant(expr: Any, var: str = "x") -> bool:
    return _parse(expr).free_symbols.isdisjoint({sp.Symbol(var)})


__all__ = [
    "evaluate", "verify_identity", "substitute", "numerical_value",
    "expand", "collect_terms", "is_constant",
]
