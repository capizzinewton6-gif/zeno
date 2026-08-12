"""Identity resolver: resolve conflicting face matches via temporal voting."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Deque, Dict, List, Tuple


@dataclass
class _Vote:
    identity: str
    score: float


class IdentityResolver:
    """Stabilize per-track identity decisions by voting across recent frames."""

    def __init__(self, window: int = 10, min_votes: int = 3,
                 confidence: float = 0.5) -> None:
        self.window = window
        self.min_votes = min_votes
        self.confidence = confidence
        self._history: Dict[int, Deque[_Vote]] = defaultdict(lambda: deque(maxlen=window))

    def observe(self, track_id: int, identity: str, score: float) -> None:
        if track_id < 0:
            return
        self._history[track_id].append(_Vote(identity, score))

    def resolve(self, track_id: int) -> Tuple[str, float]:
        votes = self._history.get(track_id)
        if not votes:
            return ("", 0.0)
        totals: Dict[str, float] = defaultdict(float)
        counts: Dict[str, int] = defaultdict(int)
        for v in votes:
            totals[v.identity] += v.score
            counts[v.identity] += 1
        if not counts:
            return ("", 0.0)
        best = max(counts, key=counts.get)
        if counts[best] < self.min_votes:
            return ("", float(totals[best] / counts[best]))
        confidence = counts[best] / len(votes)
        return (best, confidence * (totals[best] / counts[best]) if confidence >= self.confidence else ("", 0.0))

    def reset(self, track_id: int) -> None:
        self._history.pop(track_id, None)
