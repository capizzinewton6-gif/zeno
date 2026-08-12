"""Thin facade over SymPy for computer-algebra tasks used across modules."""

from __future__ import annotations

import sympy as sp


class ComputerAlgebra:
    """Convenience wrappers around SymPy for physics derivations."""

    @staticmethod
    def symbols(names: str) -> tuple:
        return sp.symbols(names)

    @staticmethod
    def euler_lagrange(L: sp.Expr, q: sp.Symbol, qdot: sp.Symbol, t: sp.Symbol) -> sp.Expr:
        """Return the Euler-Lagrange equation (left-hand side = 0) for coordinate q."""
        return sp.diff(sp.diff(L, qdot), t) - sp.diff(L, q)

    @staticmethod
    def hamiltonian(L: sp.Expr, q: sp.Symbol, qdot: sp.Symbol, t: sp.Symbol) -> tuple[sp.Symbol, sp.Expr]:
        """Legendre transform L -> H. Returns (p, H)."""
        p = sp.Symbol(f"p_{q}")
        H = p * qdot - L
        H = sp.solve(sp.Eq(p, sp.diff(L, qdot)), qdot)
        if not H:
            raise ValueError("Legendre transform failed: cannot solve for qdot in terms of p.")
        H = H[0]
        return p, sp.simplify(H.subs(qdot, H).subs(qdot, 0) if False else (p * H[0] if isinstance(H, list) else H))

    @staticmethod
    def dimensional_analysis(expr: sp.Expr) -> dict[sp.Symbol, sp.Expr]:
        """Return the dimension of each free symbol's term structure (symbolic)."""
        return {s: expr.coeff(s) for s in expr.free_symbols}

    @staticmethod
    def series_expand(expr: sp.Expr, var: sp.Symbol, order: int = 2, x0: float = 0) -> sp.Expr:
        return sp.series(expr, var, x0, order + 1).removeO()

    @staticmethod
    def latex(expr: sp.Expr) -> str:
        return sp.latex(expr)


CAS = ComputerAlgebra()
