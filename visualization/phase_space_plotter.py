"""Phase portraits, Poincare maps, and trajectory flows."""

from __future__ import annotations

import numpy as np

from tools.plot_generator import PlotGenerator


class PhaseSpacePlotter:
    """Render phase portraits and Poincare sections."""

    def __init__(self, plotter: PlotGenerator | None = None):
        self.plot = plotter or PlotGenerator()

    def phase_portrait(self, ax, deriv, x_range=(-3, 3), v_range=(-3, 3), n: int = 25):
        x = np.linspace(*x_range, n)
        v = np.linspace(*v_range, n)
        X, V = np.meshgrid(x, v)
        DX = np.zeros_like(X); DV = np.zeros_like(V)
        for i in range(n):
            for j in range(n):
                dx, dv = deriv(0, np.array([X[i, j], V[i, j]]))
                DX[i, j], DV[i, j] = dx, dv
        ax.streamplot(X, V, DX, DV, color="#56b4e9", linewidth=1)
        ax.set_xlabel("x"); ax.set_ylabel("v")
        ax.set_title("Phase portrait")

    def poincare_map(self, ax, trajectory: np.ndarray, period: float = 1.0, dt: float = 0.01):
        """Sample a trajectory stroboscopically at the given period."""
        step = max(int(period / dt), 1)
        samples = trajectory[::step]
        ax.scatter(samples[:, 0], samples[:, 1], color="#e69f00", s=10)
        ax.set_xlabel("q"); ax.set_ylabel("p")
        ax.set_title("Poincare section")
