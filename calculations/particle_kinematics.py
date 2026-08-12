"""4-momentum conservation, center-of-mass collisions, and decay rates."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from tools.constant_engine import CONSTANTS
from physics.special_relativity import FourVector


C = CONSTANTS.value("c")


@dataclass
class Collision:
    p1: FourVector
    p2: FourVector

    def total(self) -> FourVector:
        t = self.p1.as_array() + self.p2.as_array()
        return FourVector(t[0], t[1], t[2], t[3])

    def invariant_mass(self) -> float:
        """sqrt(s) / c^2-equivalent: sqrt(E_cm^2 - (p c)^2)."""
        t = self.total()
        p2 = t.px ** 2 + t.py ** 2 + t.pz ** 2
        return math.sqrt(max(t.E ** 2 - p2 * C ** 2, 0.0))


class ParticleKinematics:
    """Relativistic collision and decay kinematics."""

    @staticmethod
    def center_of_mass_energy(p1: FourVector, p2: FourVector) -> float:
        return Collision(p1, p2).invariant_mass()

    @staticmethod
    def threshold_energy(m_proj: float, m_target: float, m_products_total: float) -> float:
        """Fixed-target threshold kinetic energy to produce final-state mass sum."""
        s_thresh = m_products_total ** 2
        return (s_thresh - (m_proj + m_target) ** 2) / (2 * m_target)

    @staticmethod
    def decay_rate(Gamma: float) -> float:
        """Proper lifetime tau = 1/Gamma (natural units, hbar=1)."""
        return 1.0 / Gamma if Gamma > 0 else float("inf")

    @staticmethod
    def mean_free_path(Gamma: float, gamma: float, v: float) -> float:
        """Lab-frame decay length: beta gamma c / Gamma."""
        return (v * gamma) / Gamma if Gamma > 0 else float("inf")

    @staticmethod
    def two_body_momenta(M: float, m1: float, m2: float) -> float:
        """Magnitude of the 3-momentum of each product in the parent rest frame."""
        num = (M ** 2 - (m1 + m2) ** 2) * (M ** 2 - (m1 - m2) ** 2)
        return math.sqrt(max(num, 0.0)) / (2 * M)

    @staticmethod
    def lab_energy_from_cm(E_cm: float, M_total: float, m: float) -> float:
        """Energy of a product of mass m in the lab from CM energy."""
        return (E_cm ** 2 + m ** 2 - (M_total - m) ** 2) / (2 * M_total)


KINEMATICS = ParticleKinematics()
