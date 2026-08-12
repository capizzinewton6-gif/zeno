"""Wavefunction probability densities, Bloch spheres, and Wigner functions."""

from __future__ import annotations

import numpy as np

from tools.plot_generator import PlotGenerator


class QuantumStatePlotter:
    """Render quantum probability densities and quasi-probability distributions."""

    def __init__(self, plotter: PlotGenerator | None = None):
        self.plot = plotter or PlotGenerator()

    def probability_density(self, ax, x: np.ndarray, psi: np.ndarray, n: int = 0):
        ax.plot(x, np.abs(psi) ** 2, color="#0072b2")
        ax.set_xlabel("x"); ax.set_ylabel("|psi|^2")
        ax.set_title(f"Probability density (n={n})")

    def bloch_sphere(self, ax, state: np.ndarray | None = None):
        """Project a single-qubit state onto a Bloch sphere (3D scatter)."""
        import matplotlib.pyplot as plt
        if state is None:
            state = np.array([1, 0], dtype=complex)
        a, b = state
        x = 2 * np.real(a * np.conj(b))
        y = 2 * np.imag(np.conj(a) * b)
        z = np.abs(a) ** 2 - np.abs(b) ** 2
        ax.scatter([x], [y], [z], color="#cc79a7", s=50)
        u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]
        xs = np.cos(u) * np.sin(v); ys = np.sin(u) * np.sin(v); zs = np.cos(v)
        ax.plot_wireframe(xs, ys, zs, color="#2a3441", alpha=0.3)
        ax.set_title("Bloch sphere")

    def wigner_function(self, ax, psi: np.ndarray, x_grid: np.ndarray, p_grid: np.ndarray) -> np.ndarray:
        """Compute and plot the Wigner function of a 1D state on a (x,p) grid."""
        dx = x_grid[1] - x_grid[0]
        X, P = np.meshgrid(x_grid, p_grid, indexing="ij")
        W = np.zeros_like(X)
        n = len(psi)
        for i in range(len(x_grid)):
            for j in range(len(p_grid)):
                s_vals = np.array([psi[k] * np.conj(psi[(k + i) % n]) * np.exp(-1j * p_grid[j] * (x_grid[(k + i) % n] - x_grid[k])) * dx for k in range(n)])
                W[i, j] = np.real(np.sum(s_vals)) / np.pi
        ax.imshow(W, origin="lower", extent=[x_grid[0], x_grid[-1], p_grid[0], p_grid[-1]],
                  cmap="RdBu", aspect="auto")
        ax.set_xlabel("x"); ax.set_ylabel("p")
        ax.set_title("Wigner quasi-probability")
        return W
