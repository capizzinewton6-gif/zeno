"""Unitary gate evolution, decoherence, and density-matrix dynamics."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np


class QuantumCircuitSim:
    """A small gate-based quantum-circuit simulator with density-matrix support."""

    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
    S = np.array([[1, 0], [0, 1j]], dtype=complex)
    T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)

    def __init__(self, n_qubits: int = 1):
        self.n = n_qubits
        self.state = np.zeros(2 ** n_qubits, dtype=complex)
        self.state[0] = 1.0
        self.density = np.outer(self.state, self.state.conj())

    @staticmethod
    def kron_all(gates: Iterable[np.ndarray]) -> np.ndarray:
        result = np.array([[1.0]], dtype=complex)
        for g in gates:
            result = np.kron(result, g)
        return result

    def apply_unitary(self, U: np.ndarray) -> None:
        self.state = U @ self.state
        self.density = np.outer(self.state, self.state.conj())

    def apply_gate(self, gate: np.ndarray, qubit: int) -> None:
        """Apply a single-qubit gate to qubit index (0 = least significant)."""
        gates = [QuantumCircuitSim.I] * self.n
        gates[qubit] = gate
        self.apply_unitary(self.kron_all(gates))

    def apply_cnot(self, control: int, target: int) -> None:
        """Controlled-NOT. Qubit indexing follows apply_gate: qubit 0 is the most
        significant bit (leftmost in the Kronecker product), so bit j of state
        index i sits at position (n-1-j)."""
        dim = 2 ** self.n
        cb = self.n - 1 - control   # control bit position in the integer index
        tb = self.n - 1 - target    # target bit position
        U = np.zeros((dim, dim), dtype=complex)
        for i in range(dim):
            j = i ^ (1 << tb) if (i >> cb) & 1 else i
            U[j, i] = 1.0
        self.apply_unitary(U)

    def measure(self, shots: int = 1000) -> dict[str, int]:
        probs = np.abs(self.state) ** 2
        outcomes = np.random.choice(2 ** self.n, size=shots, p=probs)
        counts: dict[str, int] = {}
        for o in outcomes:
            bits = format(o, f"0{self.n}b")
            counts[bits] = counts.get(bits, 0) + 1
        return counts

    def dephasing_channel(self, p: float) -> None:
        """Apply a single-qubit dephasing channel to qubit 0: rho -> (1-p) rho + p Z rho Z."""
        Z = QuantumCircuitSim.Z
        # qubit 0 is MSB (leftmost in Kronecker order)
        gates_z = [Z] + [QuantumCircuitSim.I] * (self.n - 1)
        Zn = self.kron_all(gates_z)
        self.density = (1 - p) * self.density + p * (Zn @ self.density @ Zn.conj().T)
        # reset pure-state from density diagonal
        self.state = np.diag(self.density).astype(complex)
        self.state /= np.linalg.norm(self.state) if np.linalg.norm(self.state) > 0 else 1.0

    def expectation(self, observable: np.ndarray) -> float:
        return float(np.real(np.trace(observable @ self.density)))
