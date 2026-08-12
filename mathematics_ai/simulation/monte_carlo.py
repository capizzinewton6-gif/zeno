"""Probabilistic sampling, Markov chains and stochastic simulation."""

from __future__ import annotations

from typing import Callable

import numpy as np


def uniform_samples(n: int, low: float = 0, high: float = 1, seed: int | None = None) -> list[float]:
    rng = np.random.default_rng(seed)
    return rng.uniform(low, high, n).tolist()


def normal_samples(n: int, mu: float = 0, sigma: float = 1, seed: int | None = None) -> list[float]:
    rng = np.random.default_rng(seed)
    return rng.normal(mu, sigma, n).tolist()


def monte_carlo_pi(n: int = 100000, seed: int | None = None) -> dict[str, float]:
    """Estimate π by sampling points in the unit square."""
    rng = np.random.default_rng(seed)
    xs = rng.uniform(-1, 1, n)
    ys = rng.uniform(-1, 1, n)
    inside = np.sum(xs ** 2 + ys ** 2 <= 1)
    est = 4 * inside / n
    return {"estimate": float(est), "error": float(abs(est - np.pi)), "samples": n}


def monte_carlo_integral(f: Callable[[float], float], a: float, b: float, n: int = 10000, seed: int | None = None) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    xs = rng.uniform(a, b, n)
    fs = np.array([f(x) for x in xs])
    est = (b - a) * fs.mean()
    stderr = (b - a) * fs.std(ddof=1) / np.sqrt(n)
    return {"estimate": float(est), "std_error": float(stderr), "samples": n}


def importance_sampling(f: Callable[[float], float], proposal: Callable[[int, np.random.Generator], np.ndarray],
                       weight: Callable[[float], float], n: int = 10000, seed: int | None = None) -> dict[str, float]:
    """E[f(X)] via importance sampling with density proportional to ``weight``."""
    rng = np.random.default_rng(seed)
    samples = proposal(n, rng)
    vals = np.array([f(x) * weight(x) for x in samples])
    return {"estimate": float(vals.mean()), "std_error": float(vals.std(ddof=1) / np.sqrt(n)), "samples": n}


def metropolis_hastings(target_pdf: Callable[[float], float], x0: float, n: int, proposal_std: float = 1.0, seed: int | None = None) -> list[float]:
    """Metropolis-Hastings sampling from a 1-D target density."""
    rng = np.random.default_rng(seed)
    x = x0
    samples = []
    for _ in range(n):
        xp = x + rng.normal(0, proposal_std)
        ratio = target_pdf(xp) / (target_pdf(x) + 1e-300)
        if rng.uniform() < ratio:
            x = xp
        samples.append(x)
    return samples


def random_walk(steps: int, dim: int = 1, seed: int | None = None) -> dict[str, list]:
    rng = np.random.default_rng(seed)
    moves = rng.choice([-1, 1], size=(steps, dim))
    path = np.cumsum(moves, axis=0)
    return {"steps": steps, "path": path.tolist()}


def gambler_ruin(start: int, target: int, p: float = 0.5, seed: int | None = None) -> dict[str, Any]:
    """Simulate gambler's ruin until 0 or target reached."""
    rng = np.random.default_rng(seed)
    capital = start
    plays = 0
    while 0 < capital < target:
        capital += 1 if rng.random() < p else -1
        plays += 1
    return {"final_capital": capital, "plays": plays, "won": capital >= target}


from typing import Any


__all__ = [
    "uniform_samples", "normal_samples", "monte_carlo_pi", "monte_carlo_integral",
    "importance_sampling", "metropolis_hastings", "random_walk", "gambler_ruin",
]
