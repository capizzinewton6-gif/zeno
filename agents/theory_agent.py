"""Formulates theoretical models and Lagrangian/Hamiltonian frameworks."""

from __future__ import annotations

from typing import Any

import sympy as sp

from calculations.symbolic_physics import SymbolicPhysics
from physics.classical_mechanics import LagrangianMechanics, HamiltonianMechanics


class TheoryAgent:
    """Builds symbolic theoretical models from natural-language descriptions."""

    def __init__(self):
        self.cas = SymbolicPhysics()

    def build_lagrangian(self, kinetic: sp.Expr, potential: sp.Expr, q: sp.Symbol,
                         qdot: sp.Symbol, t: sp.Symbol) -> sp.Expr:
        return sp.simplify(kinetic - potential)

    def equation_of_motion(self, L: sp.Expr, q: sp.Symbol, qdot: sp.Symbol, t: sp.Symbol) -> sp.Eq:
        return LagrangianMechanics.equation_of_motion(L, q, qdot, t)

    def hamiltonian(self, L: sp.Expr, q: sp.Symbol, qdot: sp.Symbol, t: sp.Symbol) -> tuple[sp.Symbol, sp.Expr]:
        return LagrangianMechanics.hamiltonian_from_lagrangian(L, q, qdot, t)

    def hamilton_equations(self, H: sp.Expr, q: sp.Symbol, p: sp.Symbol, t: sp.Symbol = sp.Symbol("t")) -> tuple[sp.Expr, sp.Expr]:
        return HamiltonianMechanics.equations(H, q, p, t)

    def noether_charge(self, L: sp.Expr, q: sp.Symbol, qdot: sp.Symbol, t: sp.Symbol) -> sp.Expr:
        return self.cas.noether_charge(L, q, qdot, t)

    def explain(self, concept: str) -> str:
        explanations = {
            "lagrangian": "The Lagrangian L = T - V is the difference between kinetic and potential energy. "
                          "Its action S = integral L dt is stationary on the true path (Hamilton's principle).",
            "hamiltonian": "The Hamiltonian H = p qdot - L is the Legendre transform of the Lagrangian; "
                           "it generates time evolution via Hamilton's equations: qdot = dH/dp, pdot = -dH/dq.",
            "noether": "Noether's theorem: every continuous symmetry of the action implies a conserved current. "
                       "Time translation -> energy conservation; spatial translation -> momentum; rotation -> angular momentum.",
            "gaussian": "Gauss's law div E = rho/eps0 relates the electric flux through a closed surface to enclosed charge.",
        }
        key = concept.lower()
        for k, v in explanations.items():
            if k in key or key in k:
                return v
        return (f"{concept}: a central concept in the chosen regime. The TheoryAgent can formulate the relevant "
                f"Lagrangian, derive the equations of motion, and extract conserved Noether charges on request.")
