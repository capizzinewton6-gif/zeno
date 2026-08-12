"""Persistence engine: re-identification (ReID) across temporary occlusions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np

from calculations.vector_metrics import cosine_similarity


@dataclass
class ReIDRecord:
    track_id: int
    embedding: np.ndarray
    label: str
    last_seen: int


class PersistenceEngine:
    """Re-associate a lost track to a new track using appearance embeddings."""

    def __init__(self, max_lost_frames: int = 60, sim_threshold: float = 0.6) -> None:
        self.max_lost_frames = max_lost_frames
        self.sim_threshold = sim_threshold
        self._archive: List[ReIDRecord] = []

    def archive(self, track_id: int, embedding: Optional[np.ndarray], label: str,
                frame_index: int) -> None:
        if embedding is None or len(embedding) == 0:
            return
        self._archive.append(ReIDRecord(track_id, np.asarray(embedding, dtype=np.float32),
                                        label, frame_index))
        self._prune(frame_index)

    def _prune(self, frame_index: int) -> None:
        self._archive = [r for r in self._archive
                         if frame_index - r.last_seen <= self.max_lost_frames]

    def reidentify(self, embedding: Optional[np.ndarray], frame_index: int,
                   sim_threshold: Optional[float] = None) -> Optional[int]:
        if embedding is None or len(embedding) == 0 or not self._archive:
            return None
        threshold = sim_threshold if sim_threshold is not None else self.sim_threshold
        best_id = None
        best_sim = threshold
        for r in self._archive:
            sim = cosine_similarity(embedding, r.embedding)
            if sim > best_sim:
                best_sim = sim
                best_id = r.track_id
        if best_id is not None:
            self._archive = [r for r in self._archive if r.track_id != best_id]
        return best_id
