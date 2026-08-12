"""Lorentz transformations, four-vectors, and relativistic kinematics."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from tools.constant_engine import CONSTANTS


C = CONSTANTS.value("c")


def gamma(v: float) -> float:
    beta = v / C
    if abs(beta) >= 1.0:
        raise ValueError("Velocity must be subluminal (|v| < c).")
    return 1.0 / math.sqrt(1.0 - beta ** 2)


def beta_from_gamma(g: float) -> float:
    return math.sqrt(max(1.0 - 1.0 / g ** 2, 0.0))


class LorentzTransformation:
    """Boosts along an axis and velocity addition."""

    @staticmethod
    def boost(ct: float, x: float, v: float, axis: str = "x") -> tuple[float, float]:
        g = gamma(v)
        if axis == "x":
            ct_p = g * (ct - (v / C) * x)
            x_p = g * (x - (v / C) * ct)
            return ct_p, x_p
        raise NotImplementedError("Only x-boost implemented.")

    @staticmethod
    def velocity_addition(u: float, v: float) -> float:
        return (u + v) / (1.0 + u * v / C ** 2)

    @staticmethod
    def time_dilation(dt_proper: float, v: float) -> float:
        return gamma(v) * dt_proper

    @staticmethod
    def length_contraction(L_proper: float, v: float) -> float:
        return L_proper / gamma(v)

    @staticmethod
    def doppler_factor(v: float, receding: bool = True) -> float:
        beta = v / C
        sign = 1 if receding else -1
        return math.sqrt((1 - sign * beta) / (1 + sign * beta))


@dataclass
class FourVector:
    E: float  # energy (units where c may differ; we keep c explicit below)
    px: float
    py: float
    pz: float

    def as_array(self) -> np.ndarray:
        return np.array([self.E, self.px, self.py, self.pz], dtype=float)

    def mass(self) -> float:
        """Invariant mass: m^2 c^4 = E^2 - (pc)^2 -> returns mc^2 energy equivalent."""
        p2 = self.px ** 2 + self.py ** 2 + self.pz ** 2
        return math.sqrt(max(self.E ** 2 - (C * p2 / C) ** 2, 0.0)) if False else math.sqrt(max(self.E ** 2 - p2 * C ** 2, 0.0))

    def invariant_interval(self) -> float:
        p2 = self.px ** 2 + self.py ** 2 + self.pz ** 2
        return self.E ** 2 - p2 * C ** 2


class RelativisticKinematics:
    """Collisions, decays, and center-of-mass frames."""

    @staticmethod
    def total_energy(p1: FourVector, p2: FourVector) -> float:
        return (p1.as_array() + p2.as_array())[0]

    @staticmethod
    def invariant_mass(p1: FourVector, p2: FourVector) -> float:
        """sqrt(s) for two-particle system (energy-equivalent)."""
        total = p1.as_array() + p2.as_array()
        E = total[0]
        p = total[1:]
        return math.sqrt(max(E ** 2 - np.sum(p ** 2) * C ** 2, 0.0))

    @staticmethod
    def two_body_decay(m_parent: float, m1: float, m2: float) -> tuple[float, float]:
        """Rest-frame momenta and energies of a two-body decay."""
        pc2 = (m1 ** 2 - m2 ** 2) ** 2 / (4 * m_parent ** 2) - (m1 ** 2 + m2 ** 2) / 2 + m_parent ** 2 / 4
        # = ((M^2 - (m1+m2)^2)(M^2 - (m1-m2)^2)) / (4 M^2)
        pc2 = ((m_parent ** 2 - (m1 + m2) ** 2) * (m_parent ** 2 - (m1 - m2) ** 2)) / (4 * m_parent ** 2)
        pc = math.sqrt(max(pc2, 0.0))
        E1 = math.sqrt(m1 ** 2 + pc ** 2)
        E2 = math.sqrt(m2 ** 2 + pc ** 2)
        return E1, E2
