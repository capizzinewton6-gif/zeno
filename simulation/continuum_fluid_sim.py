"""Navier-Stokes, Magnetohydrodynamics (MHD), and turbulent flows.

Simple 2D vorticity-streamfunction Navier-Stokes on a periodic grid. Intended for
qualitative UI visualization, not production CFD.
"""

from __future__ import annotations

import numpy as np
from numpy.fft import fft2, ifft2


class NavierStokes2D:
    """2D incompressible Navier-Stokes in vorticity form (spectral method)."""

    def __init__(self, n: int = 64, nu: float = 1e-3, L: float = 2 * np.pi):
        self.n = n
        self.nu = nu
        self.L = L
        x = np.linspace(0, L, n, endpoint=False)
        self.X, self.Y = np.meshgrid(x, x, indexing="ij")
        k = 2 * np.pi * np.fft.fftfreq(n, d=L / n)
        self.KX, self.KY = np.meshgrid(k, k, indexing="ij")
        self.K2 = self.KX ** 2 + self.KY ** 2
        self.K2[0, 0] = 1.0  # avoid div by zero
        self.omega = np.sin(2 * self.X) * np.cos(2 * self.Y)  # initial vorticity

    def psi(self, omega_hat):
        return -omega_hat / self.K2

    def step(self, dt: float) -> None:
        omega_hat = fft2(self.omega)
        psi_hat = self.psi(omega_hat)
        u = np.real(ifft2(1j * self.KY * psi_hat))
        v = np.real(ifft2(-1j * self.KX * psi_hat))
        # spectral advection + viscous dissipation
        adv_hat = -1j * self.KX * fft2(u * self.omega) - 1j * self.KY * fft2(v * self.omega)
        dissipation = -self.nu * self.K2 * omega_hat
        omega_hat = omega_hat + dt * (adv_hat + dissipation)
        omega_hat[0, 0] = 0.0  # enforce zero mean
        self.omega = np.real(ifft2(omega_hat))

    def run(self, dt: float, n_steps: int, record_every: int = 10) -> np.ndarray:
        frames = [self.omega.copy()]
        for n in range(1, n_steps + 1):
            self.step(dt)
            if n % record_every == 0:
                frames.append(self.omega.copy())
        return np.array(frames)


class MHD2D:
    """A reduced 2D MHD toy: advect a passive magnetic field with the NS flow."""

    def __init__(self, ns: NavierStokes2D, B0: np.ndarray | None = None):
        self.ns = ns
        self.B = B0.copy() if B0 is not None else np.sin(ns.X)

    def run(self, dt: float, n_steps: int, record_every: int = 10) -> np.ndarray:
        frames = [self.B.copy()]
        for n in range(n_steps):
            omega_hat = fft2(self.ns.omega)
            psi_hat = self.ns.psi(omega_hat)
            u = np.real(ifft2(1j * self.ns.KY * psi_hat))
            v = np.real(ifft2(-1j * self.ns.KX * psi_hat))
            self.ns.step(dt)
            # simple upwind advection
            self.B = self.B - dt * (u * np.roll(self.B, -1, axis=0) + v * np.roll(self.B, -1, axis=1))
            if n % record_every == 0:
                frames.append(self.B.copy())
        return np.array(frames)
