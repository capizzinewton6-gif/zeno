"""FDTD (Finite-Difference Time-Domain) electrodynamics and diffraction."""

from __future__ import annotations

import numpy as np

from tools.constant_engine import CONSTANTS


C = CONSTANTS.value("c")
EPS0 = CONSTANTS.value("eps0")
MU0 = CONSTANTS.value("mu0")


class FDTD1D:
    """1D Yee-grid FDTD solver for the TE/TM scalar wave.

    Updates Ez and Hy on a staggered grid with a soft sinusoidal source.
    """

    def __init__(self, nx: int = 200, dx: float = 1e-3, dt: float | None = None):
        self.nx = nx
        self.dx = dx
        # Courant condition: dt <= dx / c
        self.dt = dt if dt is not None else 0.95 * dx / C
        self.Ez = np.zeros(nx)
        self.Hy = np.zeros(nx - 1)
        self.t = 0.0
        self.history: list[np.ndarray] = []

    def step(self) -> None:
        # Update H field
        self.Hy += (self.dt / (MU0 * self.dx)) * (self.Ez[1:] - self.Ez[:-1])
        # Update E field (interior)
        self.Ez[1:-1] += (self.dt / (EPS0 * self.dx)) * (self.Hy[1:] - self.Hy[:-1])
        # Soft source
        src = 80
        self.Ez[src] += np.exp(-((self.t - 1e-9) / 0.2e-9) ** 2)
        # Mur 1st-order absorbing BC
        self.Ez[0] += (C * self.dt / self.dx) * (self.Ez[1] - self.Ez[0])
        self.Ez[-1] -= (C * self.dt / self.dx) * (self.Ez[-1] - self.Ez[-2])
        self.t += self.dt

    def run(self, n_steps: int, record_every: int = 5) -> np.ndarray:
        self.history = [self.Ez.copy()]
        for n in range(n_steps):
            self.step()
            if n % record_every == 0:
                self.history.append(self.Ez.copy())
        return np.array(self.history)


class FDTD2D:
    """Minimal 2D TMz FDTD with a point source (qualitative)."""

    def __init__(self, nx: int = 120, ny: int = 120, dx: float = 1e-3, dt: float | None = None):
        self.nx, self.ny = nx, ny
        self.dx = dx
        self.dt = dt if dt is not None else 0.5 * 0.95 * dx / C
        self.Ez = np.zeros((nx, ny))
        self.Hx = np.zeros((nx - 1, ny))
        self.Hy = np.zeros((nx, ny - 1))
        self.t = 0.0
        self.history: list[np.ndarray] = []

    def step(self) -> None:
        curl_h = ((self.Hy[1:, :] - self.Hy[:-1, :]) / self.dx -
                  (self.Hx[:, 1:] - self.Hx[:, :-1]) / self.dx)
        self.Ez[1:-1, 1:-1] += self.dt / EPS0 * curl_h
        # point source
        sx, sy = self.nx // 2, self.ny // 2
        self.Ez[sx, sy] += np.sin(2 * np.pi * 10e9 * self.t)
        # update H
        dEz_dx = (self.Ez[1:, :] - self.Ez[:-1, :]) / self.dx
        dEz_dy = (self.Ez[:, 1:] - self.Ez[:, :-1]) / self.dx
        self.Hy[:, :] += self.dt / MU0 * dEz_dx
        self.Hx[:, :] -= self.dt / MU0 * dEz_dy
        self.t += self.dt

    def run(self, n_steps: int, record_every: int = 10) -> np.ndarray:
        self.history = [self.Ez.copy()]
        for n in range(n_steps):
            self.step()
            if n % record_every == 0:
                self.history.append(self.Ez.copy())
        return np.array(self.history)
