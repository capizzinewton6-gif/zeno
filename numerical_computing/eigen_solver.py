"""Quantum energy-level and normal-mode matrix diagonalizers."""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh


class EigenSolver:
    """Diagonalize Hamiltonians and dynamical matrices."""

    @staticmethod
    def energy_levels(H: np.ndarray, n_lowest: int | None = None) -> tuple[np.ndarray, np.ndarray]:
        """Diagonalize a Hamiltonian; return sorted eigenvalues and eigenvectors."""
        if n_lowest is not None and H.shape[0] > 2 * n_lowest:
            vals, vecs = np.linalg.eigh(H)
        else:
            vals, vecs = np.linalg.eigh(H)
        idx = np.argsort(np.real(vals))
        vals = np.real(vals[idx])
        vecs = vecs[:, idx]
        if n_lowest is not None:
            return vals[:n_lowest], vecs[:, :n_lowest]
        return vals, vecs

    @staticmethod
    def normal_modes(dynamical_matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Frequencies (sqrt of eigenvalues) and mode shapes."""
        w2, modes = np.linalg.eigh(np.asarray(dynamical_matrix, dtype=float))
        omega = np.sqrt(np.maximum(w2, 0.0))
        return omega, modes

    @staticmethod
    def sparse_lowest(H: sparse.csc_matrix, k: int = 5) -> tuple[np.ndarray, np.ndarray]:
        vals, vecs = eigsh(H, k=k, which="SA")
        idx = np.argsort(np.real(vals))
        return np.real(vals[idx]), np.real(vecs[:, idx])
