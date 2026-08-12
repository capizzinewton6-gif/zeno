"""Electromagnetic field tensors, fluid flows, and gravitational metrics."""

from __future__ import annotations

import numpy as np
import sympy as sp

from physics.electrodynamics import RelativisticElectrodynamics
from physics.general_relativity import schwarzschild_metric


class Spacetime3D:
    """3D/spacetime tensor constructions."""

    @staticmethod
    def field_tensor(Ex, Ey, Ez, Bx, By, Bz) -> np.ndarray:
        return RelativisticElectrodynamics.field_tensor(Ex, Ey, Ez, Bx, By, Bz)

    @staticmethod
    def flow_velocity_field_2d(X, Y, omega=1.0) -> tuple[np.ndarray, np.ndarray]:
        u = -omega * Y
        v = omega * X
        return u, v

    @staticmethod
    def minkowski_metric() -> sp.Matrix:
        return sp.diag(-1, 1, 1, 1)

    @staticmethod
    def schwarzschild(r_sym=None, rs_sym=None) -> sp.Matrix:
        r = r_sym or sp.Symbol("r")
        rs = rs_sym or sp.Symbol("r_s")
        return schwarzschild_metric(r, rs)

    @staticmethod
    def flrw_metric() -> tuple[sp.Matrix, list[sp.Symbol]]:
        from calculations.tensor_calculus import TensorCalculus
        return TensorCalculus.flrw_metric()
