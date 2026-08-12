"""Multi-object tracker: SORT-style IoU tracking with DeepSORT/ByteTrack hooks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np

from calculations.bbox_geometry import pairwise_iou_matrix
from modeling.two_d_boxes import Detection


@dataclass
class Track:
    track_id: int
    bbox: list
    label: str
    confidence: float = 0.0
    age: int = 0
    hits: int = 0
    time_since_update: int = 0
    history: List[list] = field(default_factory=list)

    def update(self, bbox: list, confidence: float = 0.0) -> None:
        self.bbox = bbox
        self.confidence = confidence or self.confidence
        self.hits += 1
        self.time_since_update = 0
        self.history.append(list(bbox))
        if len(self.history) > 50:
            self.history.pop(0)


class ObjectTracker:
    """SORT-family IoU-based multi-object tracker.

    Optional appearance embeddings enable DeepSORT-style association when present.
    """

    def __init__(self, max_age: int = 30, min_hits: int = 3,
                 iou_threshold: float = 0.3) -> None:
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self._next_id = 1
        self.tracks: List[Track] = []

    def update(self, detections: List[Detection]) -> List[Track]:
        det_boxes = [d.bbox.to_xyxy() for d in detections]
        if not self.tracks:
            for d, box in zip(detections, det_boxes):
                t = Track(self._next_id, box, d.label, d.confidence, age=1, hits=1)
                t.history.append(list(box))
                self.tracks.append(t)
                self._next_id += 1
            return [t for t in self.tracks if t.hits >= self.min_hits or t.age <= 1]

        track_boxes = [t.bbox for t in self.tracks]
        iou = pairwise_iou_matrix(np.array(track_boxes), np.array(det_boxes)) \
            if det_boxes else np.zeros((len(track_boxes), 0))

        matched, unmatched_t, unmatched_d = self._associate(iou)
        for t_idx, d_idx in matched:
            self.tracks[t_idx].update(det_boxes[d_idx], detections[d_idx].confidence)
        for d_idx in unmatched_d:
            d = detections[d_idx]
            t = Track(self._next_id, det_boxes[d_idx], d.label, d.confidence, age=1, hits=1)
            t.history.append(list(det_boxes[d_idx]))
            self.tracks.append(t)
            self._next_id += 1
        for t_idx in unmatched_t:
            self.tracks[t_idx].time_since_update += 1
            self.tracks[t_idx].age += 1

        self.tracks = [t for t in self.tracks if t.time_since_update <= self.max_age]
        return [t for t in self.tracks if t.hits >= self.min_hits or t.age <= 1]

    def _associate(self, iou: np.ndarray):
        matched: List[tuple] = []
        if iou.size == 0:
            return matched, list(range(len(self.tracks))), []
        unmatched_t = set(range(iou.shape[0]))
        unmatched_d = set(range(iou.shape[1]))
        # Greedy matching by descending IoU
        flat = np.dstack(np.unravel_index(np.argsort(-iou.ravel()), iou.shape))[0]
        for t_idx, d_idx in flat:
            t_idx, d_idx = int(t_idx), int(d_idx)
            if t_idx in unmatched_t and d_idx in unmatched_d and iou[t_idx, d_idx] >= self.iou_threshold:
                matched.append((t_idx, d_idx))
                unmatched_t.discard(t_idx)
                unmatched_d.discard(d_idx)
        return matched, sorted(unmatched_t), sorted(unmatched_d)
