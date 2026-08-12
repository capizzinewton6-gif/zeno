"""Publication-quality plotting helpers built on matplotlib.

The Physics AI renders simulations on the user interface. This module provides a thin,
consistent facade over matplotlib so every simulation/visualization module produces
figures the same way. Figures are returned as matplotlib Figure objects so the UI layer
can render them (Rich can display saved PNGs; tests can inspect the Figure directly).
"""

from __future__ import annotations

import io
import os
from typing import Callable, Iterable, Sequence

import matplotlib
matplotlib.use("Agg")  # headless-safe; UI saves to PNG and displays via Rich
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


DEFAULT_DPI = 110
DEFAULT_STYLE = {
    "figure.facecolor": "#0b0f14",
    "axes.facecolor": "#0b0f14",
    "axes.edgecolor": "#5b6b7b",
    "axes.labelcolor": "#cfd8e3",
    "axes.titlecolor": "#e6edf3",
    "xtick.color": "#9fb0c0",
    "ytick.color": "#9fb0c0",
    "grid.color": "#2a3441",
    "text.color": "#cfd8e3",
    "axes.grid": True,
    "axes.grid.which": "both",
    "axes.spines.top": False,
    "axes.spines.right": False,
}


class PlotGenerator:
    """Facade for creating and saving matplotlib figures consistently."""

    def __init__(self, dpi: int = DEFAULT_DPI, style: dict | None = None, out_dir: str = "plots"):
        self.dpi = dpi
        self.style = {**DEFAULT_STYLE, **(style or {})}
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)
        matplotlib.rcParams.update(self.style)

    def new_figure(self, n_rows: int = 1, n_cols: int = 1, figsize=(8, 5)) -> Figure:
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize, dpi=self.dpi)
        return fig

    @staticmethod
    def line(ax, x, y, *, label=None, color=None):
        ax.plot(np.asarray(x), np.asarray(y), label=label, color=color)
        if label:
            ax.legend()
        return ax

    @staticmethod
    def image(ax, z, *, extent=None, cmap="viridis", origin="lower"):
        return ax.imshow(np.asarray(z), extent=extent, cmap=cmap, origin=origin, aspect="auto")

    @staticmethod
    def vector_field(ax, x, y, u, v, *, color="#56b4e9"):
        return ax.quiver(np.asarray(x), np.asarray(y), np.asarray(u), np.asarray(v), color=color)

    def save(self, fig: Figure, name: str) -> str:
        path = os.path.join(self.out_dir, f"{name}.png")
        fig.savefig(path, dpi=self.dpi)
        plt.close(fig)
        return path

    def to_png_bytes(self, fig: Figure) -> bytes:
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=self.dpi)
        plt.close(fig)
        return buf.getvalue()

    def save_animation_frames(self, frames: Iterable, name: str, plotter: Callable, *, n_frames: int | None = None) -> list[str]:
        """Render an iterable of simulation states to numbered PNG frames.

        ``plotter(frame, ax)`` is called for each frame; the returned paths are
        suitable for the UI to animate. Kept simple (no ffmpeg dependency).
        """
        paths: list[str] = []
        for i, frame in enumerate(frames):
            if n_frames is not None and i >= n_frames:
                break
            fig = self.new_figure(figsize=(8, 5))
            ax = fig.axes[0] if fig.axes else fig.add_subplot(111)
            plotter(frame, ax)
            paths.append(self.save(fig, f"{name}_{i:05d}"))
        return paths


PLOTTER = PlotGenerator()
