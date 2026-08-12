"""Check Hermiticity of Hamiltonians and S-matrix unitarity."""

from __future__ import annotations

import numpy as np


class UnitaryChecker:
    """Hermiticity and unitarity checks for matrices."""

    @staticmethod
    def hermitian(H: np.ndarray, tol: float = 1e-10) -> bool:
        M = np.asarray(H, dtype=complex)
        if M.ndim != 2 or M.shape[0] != M.shape[1]:
            return False
        return bool(np.allclose(M, M.conj().T, atol=tol))

    @staticmethod
    def unitary(U: np.ndarray, tol: float = 1e-10) -> bool:
        M = np.asarray(U, dtype=complex)
        if M.ndim != 2 or M.shape[0] != M.shape[1]:
            return False
        return bool(np.allclose(M.conj().T @ M, np.eye(M.shape[0]), atol=tol))

    @staticmethod
    def eigenvalues_real(H: np.ndarray, tol: float = 1e-9) -> bool:
        """A Hermitian matrix has real eigenvalues."""
        w = np.linalg.eigvals(np.asarray(H, dtype=complex))
        return bool(np.allclose(np.imag(w), 0.0, atol=tol))

    @staticmethod
    def s_matrix_unitarity(S: np.ndarray, tol: float = 1e-8) -> dict:
        return {
            "shape": list(np.shape(S)),
            "unitary": UnitaryChecker.unitary(S, tol),
            "hermitian_of_generator": UnitaryChecker.hermitian(S, tol),
        }
