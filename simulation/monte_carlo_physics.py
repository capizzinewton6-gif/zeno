"""Quantum Monte Carlo, Ising model lattice, and radiation transport."""

from __future__ import annotations

import math

import numpy as np

from tools.constant_engine import CONSTANTS


KB = CONSTANTS.value("kB")
J_OVER_KB = 1.0  # units of J/k_B for the Ising demo


class IsingMonteCarlo:
    """2D square-lattice Ising model via the Metropolis algorithm."""

    def __init__(self, n: int = 16, J: float = 1.0, T: float = 2.27, h: float = 0.0):
        self.n = n
        self.J = J
        self.T = T
        self.h = h
        self.lattice = np.random.choice([-1, 1], size=(n, n))
        self.energy_history: list[float] = []
        self.mag_history: list[float] = []

    def _dE(self, i: int, j: int) -> float:
        s = self.lattice[i, j]
        nbrs = (self.lattice[(i + 1) % self.n, j] + self.lattice[(i - 1) % self.n, j] +
                self.lattice[i, (j + 1) % self.n] + self.lattice[i, (j - 1) % self.n])
        return 2 * s * (self.J * nbrs + self.h)

    def step(self) -> None:
        # Reduced units: k_B = 1, so T is in units of J/k_B. This makes T_c = 2/ln(1+sqrt2) ~ 2.269.
        beta = 1.0 / self.T
        for _ in range(self.n * self.n):
            i, j = np.random.randint(0, self.n, size=2)
            dE = self._dE(i, j)
            if dE <= 0 or np.random.rand() < math.exp(-beta * dE):
                self.lattice[i, j] *= -1
        self.energy_history.append(self.total_energy())
        self.mag_history.append(self.magnetization())

    def total_energy(self) -> float:
        E = 0.0
        for i in range(self.n):
            for j in range(self.n):
                s = self.lattice[i, j]
                nbrs = (self.lattice[(i + 1) % self.n, j] + self.lattice[i, (j + 1) % self.n])
                E -= self.J * s * nbrs
                E -= self.h * s
        return float(E)

    def magnetization(self) -> float:
        return float(np.mean(self.lattice))

    def run(self, n_steps: int) -> dict:
        for _ in range(n_steps):
            self.step()
        return {"final_energy": self.total_energy(), "final_mag": self.magnetization(),
                "energy_history": list(self.energy_history), "mag_history": list(self.mag_history)}


class RadiationTransport:
    """A simple 1D attenuation Monte Carlo: Beer-Lambert with stochastic absorption."""

    @staticmethod
    def transmission(n_photons: int, sigma: float, thickness: float) -> dict:
        transmitted = 0
        absorbed = 0
        distances = []
        for _ in range(n_photons):
            x = 0.0
            while x < thickness:
                step = -math.log(np.random.rand()) / sigma
                x += step
                if x >= thickness:
                    transmitted += 1
                    distances.append(thickness)
                    break
                else:
                    absorbed += 1
                    distances.append(x)
                    break
        return {"transmitted": transmitted, "absorbed": absorbed, "fraction": transmitted / n_photons}


class QuantumMonteCarlo:
    """Diffusion Monte Carlo ground-state energy estimator for a 1D harmonic oscillator."""

    @staticmethod
    def harmonic_ground_state(n_walkers: int = 200, n_steps: int = 1000,
                             dt: float = 0.01, omega: float = 1.0) -> dict:
        walkers = np.random.uniform(-1, 1, n_walkers)
        E_ref = 0.5 * omega
        HBAR = CONSTANTS.value("hbar")
        for _ in range(n_steps):
            walkers += np.sqrt(HBAR * dt) * np.random.randn(n_walkers)
            E = 0.5 * omega ** 2 * walkers ** 2
            # branch
            weights = np.exp(-(E - E_ref) * dt / HBAR)
            new = []
            for w, weight in zip(walkers, weights):
                n_copy = max(int(np.floor(weight + np.random.rand())), 0)
                new.extend([w] * n_copy)
            walkers = np.array(new) if new else np.random.uniform(-1, 1, n_walkers)
            if len(walkers) > 0:
                E_ref = np.mean(E) - 0.5 * omega * dt * (len(walkers) / n_walkers - 1)
        return {"estimated_ground_state": float(E_ref), "n_walkers_final": len(walkers)}
