"""Strategy for solving field equations and boundary value problems."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Strategy:
    name: str
    steps: list[str]


class ModelPlanner:
    """Recommend solution strategies for field/BVP problems."""

    @staticmethod
    def recommend(problem: str) -> Strategy:
        p = problem.lower()
        if "wave" in p:
            return Strategy("Wave equation",
                            ["Choose Fourier or separation of variables",
                             "Apply boundary conditions (Dirichlet/Neumann/periodic)",
                             "Sum normal modes"])
        if "poisson" in p or "laplace" in p:
            return Strategy("Poisson/Laplace",
                            ["Green's function expansion",
                             "Apply Dirichlet boundary conditions",
                             "Evaluate integral"])
        if "schrodinger" in p:
            return Strategy("Schrodinger",
                            ["Bound state: matrix diagonalization (FEM/spectral)",
                             "Scattering: S-matrix / WKB",
                             "Time evolution: split-step or Crank-Nicolson"])
        if "diffusion" in p or "heat" in p:
            return Strategy("Diffusion",
                            ["FTCS / Crank-Nicolson finite difference",
                             "Apply boundary & initial conditions",
                             "Check stability (r <= 1/2 for FTCS)"])
        return Strategy("Generic",
                        ["Identify the relevant PDE and its type",
                         "Select analytic (separation/series) or numeric (FDM/FEM/spectral)",
                         "Impose boundary/initial conditions",
                         "Verify with conservation/dimensional checks"])
