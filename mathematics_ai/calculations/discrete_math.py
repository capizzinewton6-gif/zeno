"""Combinatorial counting and modular arithmetic helpers."""

from __future__ import annotations

import math
from itertools import combinations, permutations


def binomial(n: int, k: int) -> int:
    return math.comb(n, k)


def multinomial(n: int, parts: list[int]) -> int:
    result = math.factorial(n)
    for p in parts:
        result //= math.factorial(p)
    return result


def derangements(n: int) -> int:
    """Number of derangements !n (subfactorial)."""
    if n == 0:
        return 1
    if n == 1:
        return 0
    return (n - 1) * (derangements(n - 1) + derangements(n - 2))


def catalan(n: int) -> int:
    """n-th Catalan number C_n = binom(2n,n)/(n+1)."""
    return math.comb(2 * n, n) // (n + 1)


def partitions(n: int, max_part: int | None = None) -> list[list[int]]:
    """Integer partitions of n."""
    if max_part is None:
        max_part = n
    if n == 0:
        return [[]]
    out = []
    for p in range(min(n, max_part), 0, -1):
        for rest in partitions(n - p, p):
            out.append([p] + rest)
    return out


def partition_count(n: int) -> int:
    """Number of integer partitions of n (p(n))."""
    return len(partitions(n))


def combinations_count(n: int, k: int) -> int:
    return math.comb(n, k)


def permutations_count(n: int, k: int | None = None) -> int:
    return math.perm(n, k) if k is not None else math.factorial(n)


def mod_add(a: int, b: int, m: int) -> int:
    return (a + b) % m


def mod_mul(a: int, b: int, m: int) -> int:
    return (a * b) % m


def mod_pow(a: int, b: int, m: int) -> int:
    return pow(a, b, m)


def chinese_remainder(remainders: list[int], moduli: list[int]) -> int:
    """CRT for pairwise-coprime moduli."""
    M = 1
    for m in moduli:
        M *= m
    x = 0
    for r, m in zip(remainders, moduli):
        Mi = M // m
        yi = pow(Mi, -1, m)
        x = (x + r * Mi * yi) % M
    return x % M


def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def lucas(n: int) -> int:
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a


__all__ = [
    "binomial", "multinomial", "derangements", "catalan", "partitions",
    "partition_count", "combinations_count", "permutations_count",
    "mod_add", "mod_mul", "mod_pow", "chinese_remainder", "fibonacci", "lucas",
]
