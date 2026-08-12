"""Scattering amplitudes, phase-space integrals, and loop corrections."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from tools.constant_engine import CONSTANTS
from physics.quantum_field_theory import FeynmanCalculusLite


HBAR = CONSTANTS.value("hbar")
C = CONSTANTS.value("c")


class FeynmanCalculus:
    """Tree-level amplitudes and 2->2 phase-space integration."""

    @staticmethod
    def two_body_phase_space(s: float, m1: float, m2: float) -> float:
        """d Phi_2 in the CM frame: sqrt(lambda(s,m1,m2,m2...))/(8 pi s)."""
        # Källén function for 2 final masses from initial sqrt(s)
        lam = (s - (m1 + m2) ** 2) * (s - (m1 - m2) ** 2)
        if lam <= 0:
            return 0.0
        return math.sqrt(lam) / (8 * math.pi * s)

    @staticmethod
    def cross_section_2to2(M2: float, s: float, m1: float, m2: float) -> float:
        """sigma = |M|^2 * dPhi_2 / (4 |p_i| sqrt(s))."""
        phi = FeynmanCalculus.two_body_phase_space(s, m1, m2)
        lam_i = (s - (m1 + m2) ** 2) * (s - (m1 - m2) ** 2)
        if lam_i <= 0:
            return 0.0
        p_i = math.sqrt(lam_i) / (2 * math.sqrt(s))
        return M2 * phi / (4 * p_i * math.sqrt(s))

    @staticmethod
    def decay_width(M2: float, M: float, m1: float, m2: float) -> float:
        """Gamma = |M|^2 * |p_f| / (8 pi M^2) for a two-body decay."""
        pf = ((M ** 2 - (m1 + m2) ** 2) * (M ** 2 - (m1 - m2) ** 2))
        if pf <= 0:
            return 0.0
        return M2 * math.sqrt(pf) / (8 * math.pi * M ** 2)

    @staticmethod
    def loop_correction_tree(tree: float, coupling: float, order: int = 1) -> float:
        """Schematic n-loop expansion: M = M_tree (1 + (g/4pi)^2 + ...)."""
        factor = 0.0
        g = coupling
        for k in range(1, order + 1):
            factor += (g / (4 * math.pi)) ** (2 * k)
        return tree * (1 + factor)


FEYNMAN = FeynmanCalculus()
