"""Test gauge transformations (U(1), SU(2), SU(3)) on Lagrangians."""

from __future__ import annotations

import sympy as sp


class GaugeInvarianceCheck:
    """Symbolic gauge-transformation checks for field-theoretic Lagrangians."""

    @staticmethod
    def u1_scalar(phi: sp.Symbol, L: sp.Expr) -> dict:
        """Check invariance of a complex-scalar Lagrangian under phi -> e^{i alpha} phi."""
        alpha = sp.Symbol("alpha")
        transformed = L.subs(phi, sp.exp(sp.I * alpha) * phi)
        diff = sp.simplify(transformed - L)
        return {"group": "U(1)", "invariant": diff == 0, "deviation": str(diff)}

    @staticmethod
    def su2_triplet(fields: list[sp.Symbol], L: sp.Expr) -> dict:
        """A rotation R in SO(3)~SU(2) on a triplet; report whether L changes."""
        n = len(fields)
        theta = sp.symbols("theta")
        R = sp.Matrix([[sp.cos(theta), -sp.sin(theta), 0],
                       [sp.sin(theta), sp.cos(theta), 0],
                       [0, 0, 1]][:n][:3])
        if n != 3:
            return {"group": "SU(2)", "invariant": None, "deviation": "requires a triplet of fields"}
        phi_vec = sp.Matrix(fields)
        rotated = R * phi_vec
        subs = {fields[i]: rotated[i] for i in range(3)}
        transformed = L.subs(subs)
        diff = sp.simplify(transformed - L)
        return {"group": "SU(2)", "invariant": diff == 0, "deviation": str(diff)}

    @staticmethod
    def su3_invariant_candidates(L: sp.Expr) -> dict:
        """Heuristic: an SU(3)-invariant Lagrangian must be built from traces of field products."""
        trace_like = ("Tr(", "trace", "f_abc") in str(L) or any(
            s in str(L) for s in ("Tr(", "trace", "f_{abc"))
        return {"group": "SU(3)", "candidate_invariant": bool(trace_like)}
