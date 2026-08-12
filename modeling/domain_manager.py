"""Manage continuous manifolds, lattice grids, and spacetime geometries."""

from __future__ import annotations

import numpy as np


class DomainManager:
    """Construct 1D/2D/3D grids and spacetime domains."""

    @staticmethod
    def grid_1d(xmin: float, xmax: float, nx: int) -> tuple[np.ndarray, float]:
        x = np.linspace(xmin, xmax, nx)
        return x, x[1] - x[0]

    @staticmethod
    def grid_2d(xmin, xmax, nx, ymin, ny, ny_points=None):
        ny_ = ny_points if ny_points is not None else ny
        x = np.linspace(xmin, xmax, nx)
        y = np.linspace(ymin, ny, ny_)
        return np.meshgrid(x, y, indexing="ij")

    @staticmethod
    def grid_3d(nx: int, ny: int, nz: int, extent: tuple = (1.0, 1.0, 1.0)):
        x = np.linspace(-extent[0] / 2, extent[0] / 2, nx)
        y = np.linspace(-extent[1] / 2, extent[1] / 2, ny)
        z = np.linspace(-extent[2] / 2, extent[2] / 2, nz)
        return np.meshgrid(x, y, z, indexing="ij")

    @staticmethod
    def lattice_grid(a: float, n: int = 4, dim: int = 2) -> np.ndarray:
        """Bravais lattice sites on an n^dim grid with lattice constant a."""
        if dim == 1:
            return a * np.arange(n)
        return a * np.array(np.meshgrid(*[np.arange(n)] * dim, indexing="ij")).reshape(dim, -1).T
