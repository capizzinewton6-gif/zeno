"""Occlusion handler: overlap detection and lost-track recovery."""

from __future__ import annotations

from typing import List, Tuple

import numpy as np

from calculations.bbox_geometry import iou
from tracking_analytics.object_tracker import Track


class OcclusionHandler:
    """Detect occlusions between tracks and decide which track to keep."""

    def __init__(self, overlap_threshold: float = 0.6) -> None:
        self.overlap_threshold = overlap_threshold

    def find_occlusions(self, tracks: List[Track]) -> List[Tuple[int, int, float]]:
        """Return pairs (track_idx_a, track_idx_b, iou) above the threshold."""
        pairs = []
        for i in range(len(tracks)):
            for j in range(i + 1, len(tracks)):
                ov = iou(tracks[i].bbox, tracks[j].bbox)
                if ov >= self.overlap_threshold:
                    pairs.append((i, j, float(ov)))
        return pairs

    def resolve(self, tracks: List[Track]) -> List[Track]:
        """Drop the lower-confidence track of an occluding pair."""
        drop = set()
        for i, j, _ in self.find_occlusions(tracks):
            if tracks[i].confidence >= tracks[j].confidence:
                drop.add(j)
            else:
                drop.add(i)
        return [t for k, t in enumerate(tracks) if k not in drop]
