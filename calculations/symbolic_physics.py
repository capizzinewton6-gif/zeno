"""Symbolic derivations of Euler-Lagrange, Dirac, and Maxwell equations."""

from __future__ import annotations

import sympy as sp


class SymbolicPhysics:
    """High-level symbolic physics derivations built on SymPy."""

    @staticmethod
    def euler_lagrange_equation(L: sp.Expr, q: sp.Symbol, qdot: sp.Symbol, t: sp.Symbol) -> sp.Eq:
        dL_dqdot = sp.diff(L, qdot)
        el = sp.diff(dL_dqdot, t) - sp.diff(L, q)
        return sp.Eq(sp.simplify(el), 0)

    @staticmethod
    def maxwell_from_potentials() -> dict[str, sp.Expr]:
        """Express E and B in terms of the four-potential (phi, A)."""
        t, x, y, z = sp.symbols("t x y z")
        phi = sp.Function("phi")(t, x, y, z)
        Ax, Ay, Az = (sp.Function(f"A_{a}")(t, x, y, z) for a in ("x", "y", "z"))
        A = sp.Matrix([Ax, Ay, Az])
        Ex = -sp.diff(phi, x) - sp.diff(Ax, t)
        Ey = -sp.diff(phi, y) - sp.diff(Ay, t)
        Ez = -sp.diff(phi, z) - sp.diff(Az, t)
        Bx = sp.diff(Az, y) - sp.diff(Ay, z)
        By = sp.diff(Ax, z) - sp.diff(Az, x)
        Bz = sp.diff(Ay, x) - sp.diff(Ax, y)
        return {"E": sp.Matrix([Ex, Ey, Ez]), "B": sp.Matrix([Bx, By, Bz])}

    @staticmethod
    def dirac_equation_symbolic() -> sp.Eq:
        """Symbolic form (i hbar gamma^mu d_mu - m c) psi = 0."""
        psi = sp.Function("psi")
        m, c, hbar = sp.symbols("m c hbar", positive=True)
        gamma_mu = sp.Symbol("gamma^mu")
        d_mu = sp.Symbol("partial_mu")
        return sp.Eq(sp.I * hbar * gamma_mu * d_mu * psi - m * c * psi, 0)

    @staticmethod
    def legendre_transform(L: sp.Expr, q: sp.Symbol, qdot: sp.Symbol, t: sp.Symbol) -> tuple[sp.Symbol, sp.Expr]:
        p = sp.Symbol(f"p_{q}")
        p_def = sp.Eq(p, sp.diff(L, qdot))
        qdot_of_p = sp.solve(p_def, qdot)
        if not qdot_of_p:
            raise ValueError("Legendre transform singular.")
        H = sp.simplify(p * qdot_of_p[0] - L.subs(qdot, qdot_of_p[0]))
        return p, H

    @staticmethod
    def noether_charge(L: sp.Expr, q: sp.Symbol, qdot: sp.Symbol, t: sp.Symbol) -> sp.Expr:
        """The conserved canonical momentum p = dL/dqdot associated with q's symmetry."""
        return sp.simplify(sp.diff(L, qdot))


SYMBOLIC = SymbolicPhysics()
