"""Black-hole ray tracing and accretion-disk particle orbits."""

from __future__ import annotations

import math

import numpy as np

from tools.constant_engine import CONSTANTS
from physics.general_relativity import GeodesicSolver


C = CONSTANTS.value("c")
G = CONSTANTS.value("G")


class RelativityGeodesicSim:
    """Trace null and timelike geodesics near a Schwarzschild black hole."""

    def __init__(self, rs: float = 1.0):
        self.rs = rs
        self.solver = GeodesicSolver(rs=rs)

    def photon_orbit(self, b: float, n_steps: int = 2000, dt: float = 0.05) -> np.ndarray:
        """Trace a photon with impact parameter b in the equatorial plane.

        Uses a simplified effective-potential formulation in (r, phi) with kappa=0 (null).
        The photon starts far away with an inward radial velocity so the trajectory
        bends around the black hole.
        """
        r0 = 50.0
        # inbound radial speed: vr^2 = 1 - b^2/r^2 (null geodesic, units c=G=M=1)
        vr0 = -np.sqrt(max(1.0 - (b / r0) ** 2, 0.0))
        vphi0 = b / r0 ** 2
        return self.solver.integrate(r0, 0.0, vr0, vphi0, L=b, dt=dt, n_steps=n_steps, kappa=0.0)

    def particle_orbit(self, r0: float, L: float, n_steps: int = 2000, dt: float = 0.05) -> np.ndarray:
        """Timelike equatorial orbit with specific angular momentum L."""
        return self.solver.integrate(r0, 0.0, 0.0, L / r0 ** 2, L=L, dt=dt, n_steps=n_steps, kappa=1.0)

    def to_xy(self, traj: np.ndarray) -> np.ndarray:
        r = traj[:, 0]
        phi = traj[:, 2]
        return np.vstack([r * np.cos(phi), r * np.sin(phi)]).T

    def horizon_mask(self, xy: np.ndarray) -> np.ndarray:
        """Boolean mask of points inside the event horizon."""
        return np.linalg.norm(xy, axis=1) <= self.rs
