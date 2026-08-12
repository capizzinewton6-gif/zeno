"""Probability theory, measure theory and stochastic processes."""

from __future__ import annotations

from typing import Any

import sympy as sp
import numpy as np
from math import comb


def _x():
    return sp.Symbol("x")


# --- standard distributions -----------------------------------------
def normal_pdf(x: Any, mu: float = 0, sigma: float = 1) -> Any:
    return sp.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * sp.sqrt(2 * sp.pi))


def normal_cdf(x: Any, mu: float = 0, sigma: float = 1) -> Any:
    return sp.Rational(1, 2) * (1 + sp.erf((x - mu) / (sigma * sp.sqrt(2))))


def binomial_pmf(k: int, n: int, p: float) -> Any:
    return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))


def expectation(expr: Any, var: str = "x", dist: str = "uniform", params: dict[str, Any] | None = None) -> Any:
    """E[f(X)] = ∫ f(x) p(x) dx over the support."""
    v = sp.Symbol(var)
    f = sp.sympify(expr)
    params = params or {}
    if dist == "uniform":
        a, b = params.get("a", 0), params.get("b", 1)
        return sp.integrate(f / (b - a), (v, a, b))
    if dist == "exponential":
        lam = params.get("lambda", 1)
        return sp.integrate(f * lam * sp.exp(-lam * v), (v, 0, sp.oo))
    if dist == "normal":
        mu, sigma = params.get("mu", 0), params.get("sigma", 1)
        return sp.integrate(f * normal_pdf(v, mu, sigma), (v, -sp.oo, sp.oo))
    raise ValueError(f"unknown distribution {dist}")


def variance(expr: Any, var: str = "x", dist: str = "uniform", params: dict[str, Any] | None = None) -> Any:
    v = sp.Symbol(var)
    ex = expectation(expr, var, dist, params)
    ex2 = expectation(expr ** 2, var, dist, params)
    return sp.simplify(ex2 - ex ** 2)


def law_of_large_numbers_demo(sampler, n: int = 10000) -> float:
    """Demonstrate LLN: return the running mean after n samples."""
    samples = np.array([sampler() for _ in range(n)])
    return float(samples.mean())


def simple_markov_chain(transition: list[list[float]], initial: list[float], steps: int) -> list[float]:
    """Compute state distribution after ``steps`` steps."""
    P = np.array(transition, dtype=float)
    v = np.array(initial, dtype=float)
    for _ in range(steps):
        v = v @ P
    return v.tolist()


def monte_carlo_estimate(func, n: int = 10000, low: float = 0, high: float = 1) -> dict[str, float]:
    """Monte Carlo estimate of ∫_low^high f(x) dx."""
    xs = np.random.uniform(low, high, n)
    fs = np.array([func(x) for x in xs])
    mean = fs.mean()
    est = (high - low) * mean
    stderr = (high - low) * fs.std(ddof=1) / np.sqrt(n)
    return {"estimate": float(est), "std_error": float(stderr), "samples": n}


def bayes(p_a: float, p_b_given_a: float, p_b_given_not_a: float) -> float:
    """P(A|B) = P(B|A)P(A) / P(B)."""
    p_b = p_b_given_a * p_a + p_b_given_not_a * (1 - p_a)
    return p_b_given_a * p_a / p_b


__all__ = [
    "normal_pdf", "normal_cdf", "binomial_pmf", "expectation", "variance",
    "law_of_large_numbers_demo", "simple_markov_chain", "monte_carlo_estimate", "bayes",
]
