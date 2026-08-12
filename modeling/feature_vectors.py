"""Feature vector representations for embeddings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence

import numpy as np


@dataclass
class FeatureVector:
    """A normalized embedding vector with metadata."""

    vector: np.ndarray
    label: str = ""
    source: str = ""

    def __post_init__(self) -> None:
        self.vector = np.asarray(self.vector, dtype=np.float32)
        n = np.linalg.norm(self.vector)
        if n > 0:
            self.vector = self.vector / n

    @property
    def dim(self) -> int:
        return int(self.vector.shape[0])

    def to_list(self) -> List[float]:
        return self.vector.tolist()

    @classmethod
    def from_list(cls, data: Sequence[float], label: str = "", source: str = "") -> "FeatureVector":
        return cls(np.asarray(data, dtype=np.float32), label=label, source=source)


def stack(vectors: Sequence[FeatureVector]) -> np.ndarray:
    """Stack feature vectors into an (N x D) matrix (rows normalized)."""
    if not vectors:
        return np.zeros((0, 0), dtype=np.float32)
    return np.vstack([v.vector for v in vectors])
