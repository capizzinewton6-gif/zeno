"""2D/3D electric, magnetic, and gravitational field-line visualizers."""

from __future__ import annotations

import numpy as np

from tools.plot_generator import PlotGenerator


class FieldLinePlotter:
    """Render field lines and equipotentials via the plot generator."""

    def __init__(self, plotter: PlotGenerator | None = None):
        self.plot = plotter or PlotGenerator()

    def electric_dipole(self, ax, x_range=(-3, 3), y_range=(-3, 3), n: int = 40):
        x = np.linspace(*x_range, n)
        y = np.linspace(*y_range, n)
        X, Y = np.meshgrid(x, y)
        Ex = (X - 1) / ((X - 1) ** 2 + Y ** 2 + 1e-3) - (X + 1) / ((X + 1) ** 2 + Y ** 2 + 1e-3)
        Ey = Y / ((X - 1) ** 2 + Y ** 2 + 1e-3) - Y / ((X + 1) ** 2 + Y ** 2 + 1e-3)
        ax.streamplot(X, Y, Ex, Ey, color="#e69f00", linewidth=1)
        ax.set_title("Electric dipole field lines")
        ax.set_xlabel("x"); ax.set_ylabel("y")
        ax.set_aspect("equal")

    def gravitational_field(self, ax, M: float = 1.0, n: int = 40):
        from tools.constant_engine import CONSTANTS
        G = CONSTANTS.value("G")
        x = np.linspace(-3, 3, n)
        X, Y = np.meshgrid(x, x)
        r = np.sqrt(X ** 2 + Y ** 2) + 0.2
        gx = -G * M * X / r ** 3
        gy = -G * M * Y / r ** 3
        ax.streamplot(X, Y, gx, gy, color="#56b4e9", linewidth=1)
        ax.set_title("Gravitational field")
        ax.set_aspect("equal")
