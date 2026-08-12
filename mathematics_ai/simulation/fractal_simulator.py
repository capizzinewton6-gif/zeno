"""Mandelbrot set, Julia sets and IFS fractal generation."""

from __future__ import annotations

from typing import Callable

import numpy as np


def mandelbrot(width: int = 200, height: int = 200, xmin: float = -2.0, xmax: float = 0.5, ymin: float = -1.25, ymax: float = 1.25, max_iter: int = 100) -> list[list[int]]:
    """Escape-time Mandelbrot set on a grid."""
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)
    img = np.zeros(C.shape, dtype=int)
    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        Z[mask] = Z[mask] ** 2 + C[mask]
        img[mask & (np.abs(Z) > 2)] = i
    return img.tolist()


def julia(c: complex, width: int = 200, height: int = 200, xmin: float = -1.5, xmax: float = 1.5, ymin: float = -1.5, ymax: float = 1.5, max_iter: int = 100) -> list[list[int]]:
    """Escape-time Julia set for parameter c."""
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    img = np.zeros(Z.shape, dtype=int)
    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        Z[mask] = Z[mask] ** 2 + c
        img[mask & (np.abs(Z) > 2)] = i
    return img.tolist()


def burning_ship(width: int = 200, height: int = 200, xmin: float = -2.0, xmax: float = 1.0, ymin: float = -2.0, ymax: float = 1.0, max_iter: int = 100) -> list[list[int]]:
    """Burning ship fractal."""
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)
    img = np.zeros(C.shape, dtype=int)
    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        Z[mask] = (abs(Z[mask].real) + 1j * abs(Z[mask].imag)) ** 2 + C[mask]
        img[mask & (np.abs(Z) > 2)] = i
    return img.tolist()


def ifs_fractal(transforms: list[dict], iterations: int = 50000, seed: int | None = None) -> dict[str, list]:
    """Iterated Function System fractal (e.g., Sierpinski/Barnsley fern).

    Each transform is {'matrix': [[a,b],[c,d]], 'shift': [e,f], 'prob': p}.
    """
    rng = np.random.default_rng(seed)
    probs = np.array([t["prob"] for t in transforms])
    probs = probs / probs.sum()
    x, y = 0.0, 0.0
    xs, ys = [x], [y]
    for _ in range(iterations):
        t = transforms[rng.choice(len(transforms), p=probs)]
        M = np.array(t["matrix"])
        s = np.array(t["shift"])
        x, y = M @ np.array([x, y]) + s
        xs.append(x); ys.append(y)
    return {"x": xs, "y": ys}


def sierpinski_triangle(iterations: int = 20000, seed: int | None = None) -> dict[str, list]:
    """Sierpinski triangle via chaos game."""
    transforms = [
        {"matrix": [[0.5, 0], [0, 0.5]], "shift": [0, 0], "prob": 1 / 3},
        {"matrix": [[0.5, 0], [0, 0.5]], "shift": [0.5, 0], "prob": 1 / 3},
        {"matrix": [[0.5, 0], [0, 0.5]], "shift": [0.25, 0.5], "prob": 1 / 3},
    ]
    return ifs_fractal(transforms, iterations, seed)


def barnsley_fern(iterations: int = 50000, seed: int | None = None) -> dict[str, list]:
    """Barnsley fern via IFS."""
    transforms = [
        {"matrix": [[0, 0], [0, 0.16]], "shift": [0, 0], "prob": 0.01},
        {"matrix": [[0.85, 0.04], [-0.04, 0.85]], "shift": [0, 1.6], "prob": 0.85},
        {"matrix": [[0.20, -0.26], [0.23, 0.22]], "shift": [0, 1.6], "prob": 0.07},
        {"matrix": [[-0.15, 0.28], [0.26, 0.24]], "shift": [0, 0.44], "prob": 0.07},
    ]
    return ifs_fractal(transforms, iterations, seed)


def box_counting_dimension(points: list[tuple[float, float]], scales: list[float] | None = None) -> float:
    """Estimate the box-counting dimension of a point set."""
    pts = np.array(points)
    if scales is None:
        scales = np.logspace(-3, -1, 10)
    counts = []
    for eps in scales:
        grid = np.floor(pts / eps).astype(int)
        counts.append(len(set(map(tuple, grid))))
    log_s = np.log(1 / np.array(scales))
    log_c = np.log(np.array(counts))
    # linear fit slope
    coeffs = np.polyfit(log_s, log_c, 1)
    return float(coeffs[0])


__all__ = [
    "mandelbrot", "julia", "burning_ship", "ifs_fractal",
    "sierpinski_triangle", "barnsley_fern", "box_counting_dimension",
]
