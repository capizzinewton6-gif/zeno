"""Vector matcher: cosine and Euclidean matching against a gallery."""

from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np

from calculations.vector_metrics import cosine_similarity, euclidean_distance


class VectorMatcher:
    """Match a query embedding against a set of stored embeddings."""

    def __init__(self, metric: str = "cosine") -> None:
        self.metric = metric

    def match(self, query: np.ndarray, gallery: np.ndarray,
              threshold: float = 0.55) -> Tuple[int, float]:
        """Return (index, score). index=-1 if nothing passes threshold."""
        if gallery is None or len(gallery) == 0:
            return (-1, 0.0)
        query = np.asarray(query, dtype=np.float32)
        gallery = np.asarray(gallery, dtype=np.float32)
        if self.metric == "cosine":
            scores = np.array([cosine_similarity(query, g) for g in gallery])
            idx = int(np.argmax(scores))
            score = float(scores[idx])
            return (idx, score) if score >= threshold else (-1, score)
        if self.metric == "euclidean":
            scores = np.array([euclidean_distance(query, g) for g in gallery])
            idx = int(np.argmin(scores))
            score = float(scores[idx])
            sim = 1.0 / (1.0 + score)
            return (idx, sim) if sim >= threshold else (-1, sim)
        raise ValueError(f"Unknown metric: {self.metric}")
