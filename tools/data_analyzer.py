"""Data analyzer: detection counts, spatial heatmaps, confidence trends."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List

import numpy as np

from modeling.two_d_boxes import Detections


@dataclass
class TrendReport:
    label_counts: Dict[str, int] = field(default_factory=dict)
    avg_confidence: float = 0.0
    total_detections: int = 0
    per_frame: List[int] = field(default_factory=list)


class DataAnalyzer:
    """Aggregate detection statistics across frames."""

    def __init__(self) -> None:
        self._frames: List[Detections] = []
        self._counts: Counter = Counter()
        self._confidences: List[float] = []

    def add(self, detections: Detections) -> None:
        self._frames.append(detections)
        self._per_frame = None
        for d in detections.items:
            self._counts[d.label] += 1
            self._confidences.append(d.confidence)

    def report(self) -> TrendReport:
        return TrendReport(
            label_counts=dict(self._counts),
            avg_confidence=float(np.mean(self._confidences)) if self._confidences else 0.0,
            total_detections=sum(self._counts.values()),
            per_frame=[len(f.items) for f in self._frames],
        )

    def confidence_histogram(self, bins: int = 10) -> List[int]:
        if not self._confidences:
            return []
        counts, _ = np.histogram(self._confidences, bins=bins, range=(0, 1))
        return counts.astype(int).tolist()

    def top_labels(self, n: int = 5) -> List[tuple]:
        return self._counts.most_common(n)
