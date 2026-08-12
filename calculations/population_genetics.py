"""Hardy-Weinberg equilibrium and genetic drift."""
from __future__ import annotations

import math


def hardy_weinberg_expected(observed):
    """observed: counts of AA, Aa, aa -> expected HWE counts."""
    aa, ab, bb = observed
    n = sum(observed)
    if n == 0:
        return [0, 0, 0]
    p = (2 * aa + ab) / (2 * n)
    q = 1 - p
    return [n * p ** 2, n * 2 * p * q, n * q ** 2]


def chi_square_hwe(observed):
    expected = hardy_weinberg_expected(observed)
    chi2 = sum(
        (o - e) ** 2 / e for o, e in zip(observed, expected) if e > 0
    )
    return chi2


def wright_fisher_drift(p0, ne, generations):
    """Deterministic-ish allele frequency drift demonstration (binomial sampling)."""
    import random
    rng = random.Random(0)
    p = p0
    history = [p]
    for _ in range(generations):
        k = rng.binomial(2 * ne, p) if hasattr(rng, "binomial") else sum(
            1 for _ in range(2 * ne) if rng.random() < p
        )
        p = k / (2 * ne)
        history.append(p)
    return history


def inbreeding_coefficient(observed_het, expected_het):
    if expected_het == 0:
        return 0.0
    return 1 - observed_het / expected_het


def genetic_drift_variance(p, ne, generations):
    """Variance of allele frequency under neutral drift."""
    return p * (1 - p) * (1 - (1 - 1 / (2 * ne)) ** generations)


def harmonic_mean_ne(pop_sizes):
    """Harmonic mean effective population size across generations."""
    if not pop_sizes:
        return 0.0
    return len(pop_sizes) / sum(1 / n for n in pop_sizes if n > 0)
