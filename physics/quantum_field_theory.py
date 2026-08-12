"""Feynman diagrams, second quantization, S-matrix, and QED/QCD essentials."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import numpy as np
import sympy as sp

from tools.constant_engine import CONSTANTS


HBAR = CONSTANTS.value("hbar")
C = CONSTANTS.value("c")


class SecondQuantization:
    """Creation/annihilation algebra and Fock-state construction."""

    @staticmethod
    def commutator(a_op, b_op) -> str:
        return f"[{a_op}, {b_op}] = delta_{{ab}}  (bosons)  or  {{{a_op},{b_op}}} = delta_{{ab}}  (fermions)"

    @staticmethod
    def number_operator_state(n: int) -> str:
        return f"N |{n}> = {n} |{n}>"

    @staticmethod
    def coherent_state_amplitude(alpha: complex, n: int) -> complex:
        """Coefficient of |n> in coherent state |alpha> (harmonic oscillator)."""
        return alpha ** n / math.sqrt(math.factorial(n)) * math.exp(-abs(alpha) ** 2 / 2)


@dataclass
class FeynmanDiagram:
    process: str
    channels: list[str]
    order: int  # perturbative order in e or g


class FeynmanCalculusLite:
    """Reduced Feynman rules for tree-level QED/QCD amplitudes."""

    QED_VERTEX = "-i e gamma^mu"
    PHOTON_PROPAGATOR = "-i g_{mu nu} / q^2"
    FERMION_PROPAGATOR = "i (q slash + m) / (q^2 - m^2)"

    @staticmethod
    def mandelstam(s: float, t: float, u: float) -> float:
        """s + t + u = sum of external masses squared."""
        return s + t + u

    @staticmethod
    def qed_moller_amplitude(s: float, t: float, u: float, m: float = 0.0) -> float:
        """Tree-level e- e- -> e- e- (Moller) |M|^2 averaged (massless limit, summed)."""
        # |M|^2 ~ 2 e^4 (s^2 + u^2)/t^2 + 2 e^4 (s^2 + t^2)/u^2 + 4 e^4 s^2/(tu)
        e = CONSTANTS.value("e")
        e4 = e ** 4
        return 2 * e4 * (s ** 2 + u ** 2) / t ** 2 + 2 * e4 * (s ** 2 + t ** 2) / u ** 2 + 4 * e4 * s ** 2 / (t * u)


class ScatteringMatrix:
    """S-matrix and cross-section helpers."""

    @staticmethod
    def unitarity_relation(M: np.ndarray, tol: float = 1e-6) -> bool:
        ident = M.conj().T @ M
        return bool(np.allclose(ident, np.eye(M.shape[0]), atol=tol))

    @staticmethod
    def cross_section_from_amplitude(M2: float, s: float, n_final: int = 2, flux: float = 1.0) -> float:
        """Schematic differential cross-section d sigma/d Omega ~ |M|^2 / (64 pi^2 s)."""
        return M2 / (64 * math.pi ** 2 * s) / max(flux, 1e-30)


@dataclass
class Particle:
    name: str
    mass_kg: float
    spin: float
    charge_e: float
    lifetime_s: float = float("inf")


QED_PARTICLES = {
    "electron": Particle("electron", CONSTANTS.value("me"), 0.5, -1.0, 0.0),
    "proton": Particle("proton", CONSTANTS.value("mp"), 0.5, 1.0, 0.0),
}
