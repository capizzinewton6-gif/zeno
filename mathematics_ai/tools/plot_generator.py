"""Publication-quality 2D/3D plots (Matplotlib-backed).

Headless-safe: uses the ``Agg`` backend so plots render without a display.
Saves figures to files and returns the file path.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import numpy as np

from mathematics_ai.config import get_config


def _styled():
    cfg = get_config()
    try:
        plt.style.use(cfg.plot_style)
    except Exception:
        plt.style.use("default")


def plot_function(f: Callable[[float], float], a: float, b: float, n: int = 400, title: str = "", xlabel: str = "x", ylabel: str = "f(x)", filename: str = "plot.png") -> str:
    _styled()
    xs = np.linspace(a, b, n)
    ys = np.array([f(x) for x in xs])
    fig, ax = plt.subplots()
    ax.plot(xs, ys)
    ax.set_title(title); ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(filename, dpi=get_config().settings.get("plot_dpi", 100))
    plt.close(fig)
    return str(Path(filename).resolve())


def plot_parametric(fx: Callable[[float], float], fy: Callable[[float], float], t_min: float = 0, t_max: float = 2 * np.pi, n: int = 400, title: str = "", filename: str = "parametric.png") -> str:
    _styled()
    ts = np.linspace(t_min, t_max, n)
    xs = np.array([fx(t) for t in ts])
    ys = np.array([fy(t) for t in ts])
    fig, ax = plt.subplots()
    ax.plot(xs, ys)
    ax.set_title(title); ax.set_aspect("equal", adjustable="box")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)
    return str(Path(filename).resolve())


def plot_3d_surface(f: Callable[[float, float], float], xmin: float = -2, xmax: float = 2, ymin: float = -2, ymax: float = 2, n: int = 50, title: str = "", filename: str = "surface.png") -> str:
    _styled()
    x = np.linspace(xmin, xmax, n)
    y = np.linspace(ymin, ymax, n)
    X, Y = np.meshgrid(x, y)
    Z = np.array([[f(xi, yi) for xi in x] for yi in y])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)
    return str(Path(filename).resolve())


def plot_scatter(xs: list[float], ys: list[float], title: str = "", filename: str = "scatter.png") -> str:
    _styled()
    fig, ax = plt.subplots()
    ax.scatter(xs, ys, s=1)
    ax.set_title(title); ax.grid(True)
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)
    return str(Path(filename).resolve())


def plot_heatmap(matrix: list[list[float]], title: str = "", filename: str = "heatmap.png") -> str:
    _styled()
    fig, ax = plt.subplots()
    im = ax.imshow(matrix, cmap="hot", interpolation="nearest")
    ax.set_title(title)
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)
    return str(Path(filename).resolve())


def plot_vector_field(fx: Callable[[float, float], float], fy: Callable[[float, float], float], xmin: float = -2, xmax: float = 2, ymin: float = -2, ymax: float = 2, n: int = 15, filename: str = "vector_field.png") -> str:
    _styled()
    x = np.linspace(xmin, xmax, n)
    y = np.linspace(ymin, ymax, n)
    X, Y = np.meshgrid(x, y)
    U = np.array([[fx(xi, yi) for xi in x] for yi in y])
    V = np.array([[fy(xi, yi) for xi in x] for yi in y])
    fig, ax = plt.subplots()
    ax.quiver(X, Y, U, V)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)
    return str(Path(filename).resolve())


__all__ = [
    "plot_function", "plot_parametric", "plot_3d_surface", "plot_scatter",
    "plot_heatmap", "plot_vector_field",
]
