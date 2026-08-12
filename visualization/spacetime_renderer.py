"""Minkowski light cones, Penrose diagrams, and embedding diagrams."""

from __future__ import annotations

import numpy as np

from tools.plot_generator import PlotGenerator


class SpacetimeRenderer:
    """Render spacetime diagrams for special and general relativity."""

    def __init__(self, plotter: PlotGenerator | None = None):
        self.plot = plotter or PlotGenerator()

    def light_cone(self, ax, c: float = 1.0, t_max: float = 3.0):
        t = np.linspace(0, t_max, 100)
        ax.plot(c * t, t, color="#e69f00", label="future light cone")
        ax.plot(-c * t, t, color="#e69f00")
        ax.plot(c * t, -t, color="#56b4e9", linestyle="--", label="past light cone")
        ax.plot(-c * t, -t, color="#56b4e9", linestyle="--")
        ax.set_xlabel("x (ct)")
        ax.set_ylabel("ct")
        ax.set_title("Minkowski light cone")
        ax.legend()
        ax.set_aspect("equal")

    def flrw_embedding(self, ax, k: float = 1.0, a: float = 1.0, n: int = 100):
        """Embed a 2-sphere slice of FLRW as a paraboloid in 3D (qualitative)."""
        theta = np.linspace(0, np.pi, n)
        r = a * np.sin(theta)
        z = k * r ** 2
        x = r * np.cos(np.linspace(0, 2 * np.pi, n)[..., None] if False else 0)
        ax.plot(r, z)
        ax.set_xlabel("r")
        ax.set_ylabel("z (embedding)")
        ax.set_title("FLRW spatial embedding (slice)")

    def penrose_schwarzschild(self, ax):
        """Schematic Penrose diagram regions for Schwarzschild."""
        ax.add_patch(__import__("matplotlib").patches.Polygon(
            [[0, 0], [1, 0], [0, 1], [0, 0]], closed=True, fill=False, color="#e69f00"))
        ax.add_patch(__import__("matplotlib").patches.Polygon(
            [[1, 0], [1, 1], [0, 1], [1, 0]], closed=True, fill=False, color="#56b4e9"))
        ax.text(0.25, 0.25, "exterior"); ax.text(0.65, 0.65, "interior")
        ax.set_title("Penrose diagram (Schwarzschild, schematic)")
        ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
