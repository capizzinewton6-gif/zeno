"""Vector metrics: cosine similarity, Euclidean distance, Mahalanobis distance."""

from __future__ import annotations

from typing import Sequence

import numpy as np


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def euclidean_distance(a: Sequence[float], b: Sequence[float]) -> float:
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    return float(np.linalg.norm(a - b))


def mahalanobis_distance(x: Sequence[float], mean: Sequence[float],
                         cov: np.ndarray) -> float:
    x = np.asarray(x, dtype=np.float32)
    mean = np.asarray(mean, dtype=np.float32)
    cov = np.asarray(cov, dtype=np.float32)
    diff = (x - mean).reshape(-1, 1)
    inv = np.linalg.pinv(cov)
    return float(np.sqrt((diff.T @ inv @ diff).item()))


def best_match(query: Sequence[float], gallery: np.ndarray,
               metric: str = "cosine") -> tuple:
    """Return (index, score) of the best match for ``query`` in ``gallery`` (N x D)."""
    gallery = np.asarray(gallery, dtype=np.float32)
    if gallery.shape[0] == 0:
        return (-1, 0.0)
    scores = np.array([_score(query, row, metric) for row in gallery])
    idx = int(np.argmax(scores)) if metric == "cosine" else int(np.argmin(scores))
    return (idx, float(scores[idx]))


def _score(a, b, metric: str) -> float:
    if metric == "cosine":
        return cosine_similarity(a, b)
    if metric == "euclidean":
        return -euclidean_distance(a, b)
    raise ValueError(f"Unknown metric: {metric}")
