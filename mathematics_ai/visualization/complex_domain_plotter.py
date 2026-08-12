"""Domain coloring for complex functions and Riemann surfaces."""

from __future__ import annotations

from typing import Callable

import numpy as np


def hsv_to_rgb(h, s, v):
    """Vectorized HSV to RGB conversion."""
    h = np.asarray(h) % 1.0
    s = np.asarray(s)
    v = np.asarray(v)
    i = (h * 6).astype(int)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6
    r = np.choose(i, [v, q, p, p, t, v])
    g = np.choose(i, [t, v, v, q, p, p])
    b = np.choose(i, [p, p, t, v, v, q])
    return np.stack([r, g, b], axis=-1)


def domain_coloring(f: Callable[[complex], complex],
                    x_range=(-2, 2), y_range=(-2, 2), resolution=100,
                    contour=True) -> dict:
    """Produce a domain coloring (RGB image) of a complex function."""
    xs = np.linspace(*x_range, resolution)
    ys = np.linspace(*y_range, resolution)
    X, Y = np.meshgrid(xs, ys)
    Z = X + 1j * Y
    W = np.vectorize(f)(Z)
    # hue from argument, value from modulus (log scale)
    H = (np.angle(W) / (2 * np.pi)) % 1.0
    mag = np.abs(W)
    V = 1 - 1 / (1 + np.log1p(mag))  # brighter near 0, darker near inf
    S = np.ones_like(H)
    rgb = hsv_to_rgb(H, S, V)
    if contour:
        # add contours at integer modulus and argument
        log_mag = np.log(mag + 1e-12)
        contour_mask = ((np.abs(log_mag - np.round(log_mag)) < 0.05) |
                        (np.abs(np.angle(W) - np.round(np.angle(W) / (2 * np.pi)) * 2 * np.pi) < 0.1))
        rgb[contour_mask] = rgb[contour_mask] * 0.5
    return {"image": rgb.tolist(), "x_range": x_range, "y_range": y_range, "resolution": resolution}


def riemann_surface_sheet(f: Callable[[complex], complex], sheet: int = 0,
                           x_range=(-2, 2), y_range=(-2, 2), resolution=50):
    """One sheet of a Riemann surface (real/imag part of sqrt-like function)."""
    xs = np.linspace(*x_range, resolution)
    ys = np.linspace(*y_range, resolution)
    X, Y = np.meshgrid(xs, ys)
    Z = X + 1j * Y
    W = np.vectorize(f)(Z)
    angle = np.angle(W) + sheet * 2 * np.pi
    return {"real": (np.abs(W) * np.cos(angle / 2)).tolist(),
            "imag": (np.abs(W) * np.sin(angle / 2)).tolist()}


__all__ = ["hsv_to_rgb", "domain_coloring", "riemann_surface_sheet"]
