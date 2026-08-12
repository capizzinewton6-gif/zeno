"""Render complex 2D/3D topological manifolds and embeddings."""

from __future__ import annotations

from typing import Any

import numpy as np


def render_2d_manifold(f, x_range=(-3, 3), y_range=(-3, 3), resolution=30):
    """Return a grid of points on a 2D surface z = f(x, y)."""
    xs = np.linspace(*x_range, resolution)
    ys = np.linspace(*y_range, resolution)
    X, Y = np.meshgrid(xs, ys)
    Z = np.vectorize(f)(X, Y)
    return {"x": X.tolist(), "y": Y.tolist(), "z": Z.tolist()}


def render_3d_embedding(param_curve, t_range=(0, 1), resolution=100):
    """Sample points on a parametric curve in 3D."""
    t = np.linspace(*t_range, resolution)
    pts = [param_curve(ti) for ti in t]
    return {"points": pts}


def render_torus(R=2.0, r=0.7, resolution=30):
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, 2 * np.pi, resolution)
    U, V = np.meshgrid(u, v)
    X = (R + r * np.cos(V)) * np.cos(U)
    Y = (R + r * np.cos(V)) * np.sin(U)
    Z = r * np.sin(V)
    return {"x": X.tolist(), "y": Y.tolist(), "z": Z.tolist()}


def render_sphere(radius=1.0, resolution=30):
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    U, V = np.meshgrid(u, v)
    X = radius * np.cos(U) * np.sin(V)
    Y = radius * np.sin(U) * np.sin(V)
    Z = radius * np.cos(V)
    return {"x": X.tolist(), "y": Y.tolist(), "z": Z.tolist()}


def render_mobius_strip(resolution=30):
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(-1, 1, resolution)
    U, V = np.meshgrid(u, v)
    X = (1 + V / 2 * np.cos(U / 2)) * np.cos(U)
    Y = (1 + V / 2 * np.cos(U / 2)) * np.sin(U)
    Z = V / 2 * np.sin(U / 2)
    return {"x": X.tolist(), "y": Y.tolist(), "z": Z.tolist()}


def render_klein_bottle(resolution=30):
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, 2 * np.pi, resolution)
    U, V = np.meshgrid(u, v)
    r = 2 + np.cos(U / 2) * np.sin(V) - np.sin(U / 2) * 2
    X = r * np.cos(U)
    Y = r * np.sin(U)
    Z = np.sin(U / 2) * 2 + np.cos(U / 2) * np.sin(V) * 2
    return {"x": X.tolist(), "y": Y.tolist(), "z": Z.tolist()}


__all__ = ["render_2d_manifold", "render_3d_embedding", "render_torus", "render_sphere", "render_mobius_strip", "render_klein_bottle"]
