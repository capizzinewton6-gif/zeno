"""FEM, FDM, and spectral methods for PDEs with boundary conditions."""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve, eigs

from calculations.field_solvers import FieldSolvers


class PDEBoundarySolvers:
    """Finite-difference, finite-element-like, and spectral solvers."""

    fdm_wave_1d = staticmethod(FieldSolvers.wave_1d)
    fdm_diffusion_1d = staticmethod(FieldSolvers.diffusion_1d)
    fdm_poisson_1d = staticmethod(FieldSolvers.poisson_1d)
    laplacian_2d = staticmethod(FieldSolvers.laplacian_2d)

    @staticmethod
    def fdm_poisson_2d(rho: np.ndarray, dx: float, dy: float, bc: tuple[float, float] = (0.0, 0.0)) -> np.ndarray:
        """Solve Laplacian(phi) = -rho on a 2D grid via sparse solve."""
        nx, ny = rho.shape
        L = FieldSolvers.laplacian_2d(nx, ny, dx, dy)
        b = -rho.flatten()
        # Dirichlet zero on boundaries
        b[0] = bc[0]
        b[-1] = bc[1]
        sol = spsolve(L.tocsc(), b)
        return sol.reshape(nx, ny)

    @staticmethod
    def spectral_derivative(f: np.ndarray, dx: float) -> np.ndarray:
        """Spectral (Fourier) derivative of a periodic function."""
        k = np.fft.fftfreq(len(f), d=dx) * 2 * np.pi
        fhat = np.fft.fft(f)
        return np.real(np.fft.ifft(1j * k * fhat))

    @staticmethod
    def fem_1d_stiffness(nx: int, dx: float) -> sparse.csc_matrix:
        """1D linear FEM stiffness matrix (tridiagonal)."""
        main = 2 * np.ones(nx) / dx
        off = -1 * np.ones(nx - 1) / dx
        return sparse.diags([off, main, off], [-1, 0, 1], format="csc")

    @staticmethod
    def eigenmodes(operator: sparse.csc_matrix, k: int = 6, sigma: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
        """Compute the lowest-k eigenmodes of a sparse operator."""
        vals, vecs = eigs(operator, k=k, sigma=sigma, which="LM")
        idx = np.argsort(np.real(vals))
        return np.real(vals[idx]), np.real(vecs[:, idx])
