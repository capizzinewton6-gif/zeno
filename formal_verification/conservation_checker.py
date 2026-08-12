"""Verify energy, momentum, charge, and probability conservation."""

from __future__ import annotations

import numpy as np


class ConservationChecker:
    """Numerical conservation-law checks for simulation trajectories."""

    @staticmethod
    def energy(trajectory: np.ndarray, energy_fn, tol: float = 1e-6) -> dict:
        """Energies across a trajectory. ``energy_fn(state) -> scalar``."""
        energies = np.array([energy_fn(s) for s in trajectory])
        drift = (energies[-1] - energies[0]) / (abs(energies[0]) + 1e-30)
        return {
            "E0": float(energies[0]),
            "E_final": float(energies[-1]),
            "max_drift": float(drift),
            "conserved": bool(abs(drift) < tol),
        }

    @staticmethod
    def momentum(trajectory: np.ndarray, momentum_fn, tol: float = 1e-6) -> dict:
        momenta = np.array([momentum_fn(s) for s in trajectory])
        if momenta.ndim == 1:
            drift = float(momenta[-1] - momenta[0])
            return {"p0": float(momenta[0]), "p_final": float(momenta[-1]), "drift": drift,
                    "conserved": bool(abs(drift) < tol)}
        drift = np.linalg.norm(momenta[-1] - momenta[0])
        return {"drift": float(drift), "conserved": bool(drift < tol)}

    @staticmethod
    def probability(psi_trajectory: np.ndarray, dx: float = 1.0, tol: float = 1e-6) -> dict:
        """Norm conservation for a Schrödinger wavefunction trajectory."""
        norms = np.array([np.sum(np.abs(psi) ** 2) * dx for psi in psi_trajectory])
        drift = (norms[-1] - norms[0]) / (abs(norms[0]) + 1e-30)
        return {"norm0": float(norms[0]), "norm_final": float(norms[-1]),
                "drift": float(drift), "conserved": bool(abs(drift) < tol)}

    @staticmethod
    def charge(q_final: float, q_initial: float, tol: float = 1e-9) -> bool:
        return abs(q_final - q_initial) < tol
