"""PDE integration for wave, diffusion, Poisson, and Schrödinger equations."""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


class FieldSolvers:
    """Finite-difference PDE solvers on regular grids."""

    @staticmethod
    def wave_1d(u0: np.ndarray, ut0: np.ndarray, c: float, dx: float, dt: float, n_steps: int) -> np.ndarray:
        """1D wave equation u_tt = c^2 u_xx with fixed ends."""
        nx = len(u0)
        u = u0.copy().astype(float)
        u_prev = u - ut0 * dt  # first-order backward for u_{-1}
        u[0] = u[-1] = 0.0
        r = (c * dt / dx) ** 2
        history = np.empty((n_steps + 1, nx))
        history[0] = u
        for n in range(1, n_steps + 1):
            u_new = u.copy()
            u_new[1:-1] = (2 * u[1:-1] - u_prev[1:-1]
                           + r * (u[2:] - 2 * u[1:-1] + u[:-2]))
            u_new[0] = u_new[-1] = 0.0
            u_prev, u = u, u_new
            history[n] = u
        return history

    @staticmethod
    def diffusion_1d(u0: np.ndarray, alpha: float, dx: float, dt: float, n_steps: int) -> np.ndarray:
        """1D heat/diffusion equation u_t = alpha u_xx (FTCS)."""
        nx = len(u0)
        u = u0.copy().astype(float)
        r = alpha * dt / dx ** 2
        if r > 0.5:
            raise ValueError(f"FTCS unstable: r={r:.3f} > 0.5. Reduce dt.")
        history = np.empty((n_steps + 1, nx))
        history[0] = u
        for n in range(1, n_steps + 1):
            un = u.copy()
            u[1:-1] = un[1:-1] + r * (un[2:] - 2 * un[1:-1] + un[:-2])
            history[n] = u
        return history

    @staticmethod
    def poisson_1d(rho: np.ndarray, dx: float, bc: tuple[float, float] = (0.0, 0.0)) -> np.ndarray:
        """Solve d^2 phi/dx^2 = -rho/eps0 in 1D (Dirichlet BCs)."""
        nx = len(rho)
        main = -2 * np.ones(nx)
        off = np.ones(nx - 1)
        A = sparse.diags([off, main, off], [-1, 0, 1], format="csc")
        b = -rho * dx ** 2
        b[0] = bc[0]
        b[-1] = bc[1]
        A[0, :] = 0.0
        A[0, 0] = 1.0
        A[-1, :] = 0.0
        A[-1, -1] = 1.0
        return spsolve(A.tocsc(), b)

    @staticmethod
    def schrodinger_evolution(psi0: np.ndarray, H: np.ndarray, dt: float, n_steps: int) -> np.ndarray:
        """Crank-Nicolson-ish split-step: psi(t+dt) = exp(-i H dt/hbar) psi(t) via matrix power."""
        import scipy.linalg as la
        U = la.expm(-1j * H * dt)  # hbar = 1 in natural units for the demo
        psi = psi0.copy().astype(complex)
        history = np.empty((n_steps + 1, len(psi0)), dtype=complex)
        history[0] = psi
        for n in range(1, n_steps + 1):
            psi = U @ psi
            history[n] = psi
        return history

    @staticmethod
    def laplacian_2d(nx: int, ny: int, dx: float, dy: float) -> sparse.csc_matrix:
        """Discrete 2D Laplacian operator (sparse)."""
        Dxx = sparse.diags([1, -2, 1], [-1, 0, 1], shape=(nx, nx)) / dx ** 2
        Dyy = sparse.diags([1, -2, 1], [-1, 0, 1], shape=(ny, ny)) / dy ** 2
        Ix = sparse.eye(nx)
        Iy = sparse.eye(ny)
        return sparse.kron(Iy, Dxx) + sparse.kron(Dyy, Ix)


SOLVERS = FieldSolvers()
