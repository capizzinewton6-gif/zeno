"""Infinite-dimensional state spaces, bra-ket algebra, and Fock states."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


class HilbertSpace:
    """Bra-ket algebra and Fock-state operations for a discrete basis."""

    def __init__(self, dim: int = 2):
        self.dim = dim

    def basis(self, n: int) -> np.ndarray:
        v = np.zeros(self.dim, dtype=complex)
        v[n] = 1.0
        return v

    def bra(self, state: np.ndarray) -> np.ndarray:
        return state.conj()

    def inner(self, a: np.ndarray, b: np.ndarray) -> complex:
        return complex(np.vdot(a, b))

    def outer(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.outer(a, b.conj())

    def expectation(self, operator: np.ndarray, state: np.ndarray) -> complex:
        return complex(state.conj() @ operator @ state)

    def normalize(self, state: np.ndarray) -> np.ndarray:
        n = np.linalg.norm(state)
        return state / n if n > 0 else state


class FockSpace:
    """Bosonic Fock-space helpers."""

    @staticmethod
    def creation(n: int, dim: int) -> np.ndarray:
        """a^dagger |n> = sqrt(n+1) |n+1> in a truncated dimension."""
        a = np.zeros((dim, dim))
        for k in range(dim - 1):
            a[k + 1, k] = math.sqrt(k + 1)
        return a

    @staticmethod
    def annihilation(dim: int) -> np.ndarray:
        """a |n> = sqrt(n) |n-1>."""
        return FockSpace.creation(0, dim).T

    @staticmethod
    def number_operator(dim: int) -> np.ndarray:
        return FockSpace.creation(0, dim) @ FockSpace.annihilation(dim)

    @staticmethod
    def coherent_state(alpha: complex, dim: int = 20) -> np.ndarray:
        """|alpha> = e^{-|alpha|^2/2} sum_n alpha^n/sqrt(n!) |n>."""
        a = FockSpace.annihilation(dim)
        # |alpha> is eigenstate of a; build via repeated application on vacuum
        v = np.zeros(dim); v[0] = 1.0
        psi = v.copy()
        for _ in range(1, dim):
            v = a.conj().T @ v  # approximate via creation operator sequence
        # simpler direct construction:
        n = np.arange(dim)
        psi = (alpha ** n / np.sqrt([math.factorial(int(k)) for k in n]))
        psi = psi * math.exp(-abs(alpha) ** 2 / 2)
        return psi / np.linalg.norm(psi)
