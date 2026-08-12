"""Elementary, analytic and algebraic number theory."""

from __future__ import annotations

from typing import Any

import sympy as sp
import mpmath


def is_prime(n: int) -> bool:
    return bool(sp.isprime(n))


def prime_factorization(n: int) -> dict[int, int]:
    return dict(sp.factorint(n))


def divisors(n: int) -> list[int]:
    return sorted(sp.divisors(n))


def euler_totient(n: int) -> int:
    return int(sp.totient(n))


def mobius(n: int) -> int:
    return int(sp.mobius(n))


def gcd(a: int, b: int) -> int:
    return int(sp.gcd(a, b))


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    g, x, y = sp.gcdex(a, b)
    return int(g), int(x), int(y)


def crt(remainders: list[int], moduli: list[int]) -> int:
    """Chinese Remainder Theorem: solve x ≡ r_i (mod m_i) for coprime m_i."""
    return int(sp.crt(moduli, remainders))


def modular_power(base: int, exp: int, mod: int) -> int:
    return pow(base, exp, mod)


def modular_inverse(a: int, m: int) -> int:
    return int(sp.invert(a, m))


def is_quadratic_residue(a: int, p: int) -> bool:
    return bool(sp.is_quad_residue(a, p))


def riemann_zeta(s: Any, digits: int = 50) -> Any:
    """Riemann zeta function ζ(s). Symbolic for symbolic s, numeric otherwise."""
    try:
        val = sp.zeta(sp.sympify(s))
        if val.is_number and val.is_real:
            mpmath.mp.dps = digits
            return mpmath.zeta(float(s))
        return val
    except Exception:
        mpmath.mp.dps = digits
        return mpmath.zeta(complex(s))


def prime_counting(x: int) -> int:
    """π(x): number of primes ≤ x."""
    return sp.primepi(x)


def nth_prime(n: int) -> int:
    return int(sp.prime(n))


def fermat_little_check(a: int, p: int) -> bool:
    """Verify a^p ≡ a (mod p) for prime p."""
    return pow(a, p, p) == a % p


def legendre_symbol(a: int, p: int) -> int:
    return int(sp.legendre_symbol(a, p))


__all__ = [
    "is_prime", "prime_factorization", "divisors", "euler_totient", "mobius",
    "gcd", "extended_gcd", "crt", "modular_power", "modular_inverse",
    "is_quadratic_residue", "riemann_zeta", "prime_counting", "nth_prime",
    "fermat_little_check", "legendre_symbol",
]
