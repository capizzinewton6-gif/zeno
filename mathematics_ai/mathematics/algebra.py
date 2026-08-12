"""Abstract algebra: groups, rings, and fields.

Backed by SymPy's algebraic structures where possible, with additional helpers
for group-theoretic computations (order, subgroups, cyclic group checks).
"""

from __future__ import annotations

from typing import Any

import sympy as sp
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, DihedralGroup, AbelianGroup


class Group:
    """Thin wrapper over SymPy ``PermutationGroup`` with convenience methods."""

    def __init__(self, perm_group: PermutationGroup) -> None:
        self.g = perm_group

    @property
    def order(self) -> int:
        return self.g.order()

    @property
    def is_abelian(self) -> bool:
        return self.g.is_abelian

    @property
    def is_cyclic(self) -> bool:
        return self.g.is_cyclic

    def elements(self) -> list[Permutation]:
        return list(self.g.elements)

    def subgroups(self) -> list[PermutationGroup]:
        return self.g.subgroups()

    def center(self) -> "Group":
        return Group(self.g.center())

    def derived_series(self) -> list["Group"]:
        return [Group(sg) for sg in self.g.derived_series()]

    def __repr__(self) -> str:
        return f"Group(order={self.order}, abelian={self.is_abelian}, cyclic={self.is_cyclic})"


def symmetric(n: int) -> Group:
    return Group(SymmetricGroup(n))


def cyclic(n: int) -> Group:
    return Group(CyclicGroup(n))


def dihedral(n: int) -> Group:
    return Group(DihedralGroup(n))


def abelian(*orders: int) -> Group:
    return Group(AbelianGroup(*orders))


def element_order(g: Permutation, group: PermutationGroup) -> int:
    """Order of an element g in a group."""
    return g.order()


class Ring:
    """Basic commutative ring over a polynomial ring R[x]."""

    def __init__(self, symbols: str, domain: str = "ZZ") -> None:
        self.symbols = sp.symbols(symbols)
        self.domain = domain

    def quotient(self, modulus: Any) -> "QuotientRing":
        return QuotientRing(self, modulus)


class QuotientRing:
    """Quotient ring R[x]/(m(x)) — a field when m is irreducible over a field."""

    def __init__(self, ring: Ring, modulus: Any) -> None:
        self.ring = ring
        self.modulus = sp.sympify(modulus)
        self.is_field: bool | None = None
        try:
            self.is_field = sp.Poly(self.modulus, *sp.preprocess([self.modulus])[0] if False else self._vars(),
                                    domain=self.ring.domain).is_irreducible
        except Exception:
            self.is_field = None

    def _vars(self):
        return self.ring.symbols if isinstance(self.ring.symbols, tuple) else (self.ring.symbols,)

    def reduce(self, expr: Any) -> Any:
        x = self._vars()
        return sp.rem(sp.sympify(expr), self.modulus, *x, domain=self.ring.domain)


def is_prime_field(modulus: int) -> bool:
    """Z/pZ is a field iff p is prime."""
    return sp.isprime(modulus)


def galois_group_of_polynomial(expr: Any, var: str = "x") -> dict[str, Any]:
    """Attempt to compute the Galois group of a polynomial via SymPy."""
    x = sp.Symbol(var)
    poly = sp.Poly(sp.sympify(expr), x)
    g = sp.galois_group(poly, by_name=False)
    return {"polynomial": str(expr), "degree": poly.degree(), "galois_group": str(g)}


__all__ = [
    "Group", "Ring", "QuotientRing", "symmetric", "cyclic", "dihedral", "abelian",
    "element_order", "is_prime_field", "galois_group_of_polynomial",
]
