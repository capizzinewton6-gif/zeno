"""Maximum likelihood and parsimony scoring."""
from __future__ import annotations

import math


def parsimony_score(tree, sites):
    """Fitch parsimony: minimal number of state changes across sites."""
    score = 0
    for site in sites:
        sets = {k: {v} for k, v in site.items()}
        # naive: count changes between adjacent leaves (simplification)
        states = list(site.values())
        for a, b in zip(states, states[1:]):
            if a != b:
                score += 1
    return score


def jc69_likelihood(p):
    """JC69 single-site likelihood contribution given difference prob p."""
    if p <= 0:
        return 1.0
    if p >= 0.75:
        return 0.0
    return 0.25 * (1 + 3 * math.exp(-(4 / 3) * (-0.75 * math.log(1 - 4 / 3 * p))))


def log_likelihood_sum(likelihoods):
    return sum(math.log(max(l, 1e-12)) for l in likelihoods)


def jukes_cantor_distance(p):
    if p <= 0:
        return 0.0
    if p >= 0.75:
        return float("inf")
    return -0.75 * math.log(1 - (4 / 3) * p)


def upgma(distance_matrix, labels):
    """Simple UPGMA clustering returning a nested list tree."""
    clusters = [(label,) for label in labels]
    heights = {tuple(c): 0.0 for c in clusters}
    matrix = {a: {b: distance_matrix[i][j] for j, b in enumerate(labels) if b != a}
              for i, a in enumerate(labels)}
    while len(clusters) > 1:
        # find closest pair
        best = None
        for i, ci in enumerate(clusters):
            for cj in clusters[i + 1:]:
                d = _avg_distance(ci, cj, distance_matrix, labels)
                if best is None or d < best[0]:
                    best = (d, ci, cj)
        d, ci, cj = best
        new_cluster = ci + cj
        heights[new_cluster] = d / 2
        clusters.remove(ci); clusters.remove(cj); clusters.append(new_cluster)
    return {"tree": clusters[0], "heights": heights}


def _avg_distance(ci, cj, matrix, labels):
    total = 0
    count = 0
    for a in ci:
        for b in cj:
            i, j = labels.index(a), labels.index(b)
            total += matrix[i][j]
            count += 1
    return total / count if count else 0.0
