"""First/second-order expansions and adiabatic approximations."""

from __future__ import annotations

import sympy as sp


class PerturbationEngine:
    """Systematic perturbation expansions."""

    @staticmethod
    def first_order(expr: sp.Expr, var: sp.Symbol, x0: float = 0) -> sp.Expr:
        return sp.series(expr, var, x0, 2).removeO()

    @staticmethod
    def second_order(expr: sp.Expr, var: sp.Symbol, x0: float = 0) -> sp.Expr:
        return sp.series(expr, var, x0, 3).removeO()

    @staticmethod
    def adiabatic_invariant(q: sp.Symbol, p: sp.Symbol, action_integral: sp.Expr) -> str:
        """J = closed contour integral p dq is the adiabatic invariant for slow parameter changes."""
        return f"J = closedoint p dq = {sp.simplify(action_integral)}  (constant under slow changes)"

    @staticmethod
    def wkb_connection_formula(E: float, V: float, m: float, hbar: float = 1.054571817e-34) -> dict:
        """WKB decay constant and connection prefactor across a turning point."""
        kappa = ((2 * m * (V - E)) ** 0.5) / hbar if V > E else 0.0
        return {"kappa": kappa, "tunneling_factor": f"exp(-{kappa:.3g} a) for barrier width a"}
