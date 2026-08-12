"""Compute agent: executes numerical and symbolic computations.

Wraps the calculations/numerical_computing/mathematics modules behind a single
``compute`` entry point that dispatches by operation name.
"""

from __future__ import annotations

import re
from typing import Any

from mathematics_ai.agents.base import BaseAgent, AgentResult
from mathematics_ai.calculations import (
    symbolic_math, matrix_algebra, discrete_math, numerical_methods,
)
from mathematics_ai.mathematics import number_theory


class ComputeAgent(BaseAgent):
    """Executes concrete symbolic/numerical computations."""

    name = "compute_agent"

    # maps operation -> handler
    OPERATIONS = {
        "differentiate", "integrate", "limit", "solve", "simplify", "series",
        "factor", "eigenvalues", "eigenvectors", "determinant", "inverse",
        "svd", "rank", "solve_linear", "modular_power", "crt", "factorize",
        "is_prime", "totient", "binomial", "catalan", "partitions", "fft",
        "root_find", "minimize", "monte_carlo",
    }

    def compute(self, operation: str, **args: Any) -> AgentResult:
        op = operation.lower().replace("-", "_")
        steps = [{"operation": op, "args": {k: str(v) for k, v in args.items()}}]
        try:
            handler = getattr(self, f"_op_{op}", None)
            if handler is None:
                return self.fail(f"unknown operation: {operation}")
            result = handler(**args)
            steps.append({"result": str(result)})
            return self.result(result, steps, operation=op)
        except Exception as exc:
            return self.fail(f"{op} failed: {exc}", operation=op)

    # --- symbolic -----------------------------------------------------
    def _op_differentiate(self, expr: str, var: str = "x", order: int = 1, **_) -> Any:
        return symbolic_math.differentiate(expr, var, order)

    def _op_integrate(self, expr: str, var: str = "x", a: Any | None = None, b: Any | None = None, **_) -> Any:
        if a is not None and b is not None:
            return symbolic_math.integrate(expr, var, a, b)
        return symbolic_math.integrate(expr, var)

    def _op_limit(self, expr: str, var: str = "x", to: Any = 0, direction: str = "+", **_) -> Any:
        return symbolic_math.limit(expr, var, to, direction)

    def _op_solve(self, expr: str, var: str = "x", **_) -> Any:
        return symbolic_math.solve(expr, var)

    def _op_simplify(self, expr: str, **_) -> Any:
        return symbolic_math.simplify(expr)

    def _op_series(self, expr: str, var: str = "x", around: Any = 0, n: int = 6, **_) -> Any:
        return symbolic_math.series_expansion(expr, var, around, n)

    def _op_factor(self, expr: str, var: str = "x", **_) -> Any:
        import sympy as sp
        return sp.factor(sp.sympify(expr), sp.Symbol(var))

    # --- linear algebra ---------------------------------------------
    def _op_eigenvalues(self, matrix: list[list[Any]], **_) -> Any:
        return matrix_algebra.eigenvalues(matrix)

    def _op_eigenvectors(self, matrix: list[list[Any]], **_) -> Any:
        return matrix_algebra.eigendecomposition(matrix)

    def _op_determinant(self, matrix: list[list[Any]], **_) -> Any:
        return matrix_algebra.determinant(matrix)

    def _op_inverse(self, matrix: list[list[Any]], **_) -> Any:
        return matrix_algebra.inverse(matrix)

    def _op_svd(self, matrix: list[list[Any]], **_) -> Any:
        return matrix_algebra.svd(matrix)

    def _op_rank(self, matrix: list[list[Any]], **_) -> Any:
        import numpy as np
        return int(np.linalg.matrix_rank(np.array(matrix, dtype=float)))

    def _op_solve_linear(self, A: list[list[Any]], b: list[Any], **_) -> Any:
        return matrix_algebra.solve_linear(A, b)

    # --- number theory / discrete -----------------------------------
    def _op_modular_power(self, base: int, exp: int, mod: int, **_) -> Any:
        return discrete_math.mod_pow(base, exp, mod)

    def _op_crt(self, remainders: list[int], moduli: list[int], **_) -> Any:
        return discrete_math.chinese_remainder(remainders, moduli)

    def _op_factorize(self, n: int, **_) -> Any:
        return number_theory.prime_factorization(n)

    def _op_is_prime(self, n: int, **_) -> Any:
        return number_theory.is_prime(n)

    def _op_totient(self, n: int, **_) -> Any:
        return number_theory.euler_totient(n)

    def _op_binomial(self, n: int, k: int, **_) -> Any:
        return discrete_math.binomial(n, k)

    def _op_catalan(self, n: int, **_) -> Any:
        return discrete_math.catalan(n)

    def _op_partitions(self, n: int, **_) -> Any:
        return discrete_math.partition_count(n)

    # --- numerical ---------------------------------------------------
    def _op_fft(self, signal: list[Any], **_) -> Any:
        from mathematics_ai.numerical_computing import fast_fourier
        return fast_fourier.fft(signal)

    def _op_root_find(self, expr: str, a: float, b: float, **_) -> Any:
        import sympy as sp
        f = sp.lambdify("x", sp.sympify(expr), "numpy")
        return numerical_methods.root_find(f, a, b)

    def _op_minimize(self, expr: str, bounds: tuple[float, float], **_) -> Any:
        import sympy as sp
        f = sp.lambdify("x", sp.sympify(expr), "numpy")
        return numerical_methods.minimize_scalar(f, bounds)
