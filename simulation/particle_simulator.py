"""N-body gravitational, Molecular Dynamics (Lennard-Jones), and PIC."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from tools.constant_engine import CONSTANTS
from simulation.simulation_manager import Integrators


G = CONSTANTS.value("G")


@dataclass
class NBodyConfig:
    positions: np.ndarray   # (N, 3)
    velocities: np.ndarray  # (N, 3)
    masses: np.ndarray      # (N,)


class NBodySimulator:
    """Direct-summation gravitational N-body integrator."""

    def __init__(self, config: NBodyConfig, softening: float = 1e-3):
        self.pos = np.array(config.positions, dtype=float)
        self.vel = np.array(config.velocities, dtype=float)
        self.m = np.array(config.masses, dtype=float)
        self.softening2 = softening ** 2
        self.N = len(self.m)
        self.history: list[np.ndarray] = []

    def _accel(self, pos: np.ndarray) -> np.ndarray:
        a = np.zeros_like(pos)
        for i in range(self.N):
            dr = pos - pos[i]
            r2 = np.sum(dr ** 2, axis=1) + self.softening2
            inv_r3 = np.where(r2 > 0, r2 ** -1.5, 0.0)
            inv_r3[i] = 0.0
            a += self.m[i] * dr * inv_r3[:, None]
        return G * a

    def step(self, dt: float) -> None:
        a = self._accel(self.pos)
        self.vel += a * dt
        self.pos += self.vel * dt
        self.history.append(self.pos.copy())

    def run(self, dt: float, n_steps: int, record_every: int = 1) -> np.ndarray:
        self.history = [self.pos.copy()]
        for n in range(1, n_steps + 1):
            self.step(dt)
            if n % record_every == 0:
                self.history.append(self.pos.copy())
        return np.array(self.history)


class LennardJonesMD:
    """2D Molecular Dynamics with the Lennard-Jones potential."""

    def __init__(self, positions: np.ndarray, velocities: np.ndarray, sigma: float = 1.0, eps: float = 1.0):
        self.pos = np.array(positions, dtype=float)
        self.vel = np.array(velocities, dtype=float)
        self.sigma = sigma
        self.eps = eps
        self.N = len(self.pos)
        self.history: list[np.ndarray] = []

    def _forces(self, pos: np.ndarray) -> np.ndarray:
        F = np.zeros_like(pos)
        for i in range(self.N):
            dr = pos - pos[i]
            r2 = np.sum(dr ** 2, axis=1)
            r2[i] = 1.0
            r6 = r2 ** 3
            sr6 = (self.sigma ** 2) ** 3 / r6
            f_mag = 24 * self.eps * (2 * sr6 ** 2 - sr6) / r2
            f_mag[i] = 0.0
            F += f_mag[:, None] * dr
        return F

    def step(self, dt: float) -> None:
        F = self._forces(self.pos)
        self.vel += F * dt
        self.pos += self.vel * dt
        self.history.append(self.pos.copy())

    def run(self, dt: float, n_steps: int) -> np.ndarray:
        self.history = [self.pos.copy()]
        for _ in range(n_steps):
            self.step(dt)
        return np.array(self.history)
