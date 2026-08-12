"""Interaction detector: object-person and person-person proximity events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

from calculations.bbox_geometry import iou
from modeling.two_d_boxes import Detection


@dataclass
class Interaction:
    kind: str  # person_person | object_person
    subject_a: str
    subject_b: str
    bbox_a: list
    bbox_b: list
    proximity: float  # 0..1, higher = closer


class InteractionDetector:
    """Flag proximity interactions between detections."""

    def __init__(self, iou_threshold: float = 0.05, distance_ratio: float = 1.5) -> None:
        self.iou_threshold = iou_threshold
        self.distance_ratio = distance_ratio

    def detect(self, detections: List[Detection]) -> List[Interaction]:
        out: List[Interaction] = []
        people = [d for d in detections if d.label.lower() in ("person", "people")]
        objects = [d for d in detections if d.label.lower() not in ("person", "people")]

        for i in range(len(people)):
            for j in range(i + 1, len(people)):
                prox = self._proximity(people[i], people[j])
                if prox > 0:
                    out.append(Interaction("person_person", people[i].label, people[j].label,
                                           people[i].bbox.to_xyxy(), people[j].bbox.to_xyxy(), prox))
        for p in people:
            for o in objects:
                prox = self._proximity(p, o)
                if prox > 0:
                    out.append(Interaction("object_person", p.label, o.label,
                                          p.bbox.to_xyxy(), o.bbox.to_xyxy(), prox))
        return out

    def _proximity(self, a: Detection, b: Detection) -> float:
        ov = iou(a.bbox.to_xyxy(), b.bbox.to_xyxy())
        if ov >= self.iou_threshold:
            return float(min(1.0, ov + 0.3))
        cx_a, cy_a = a.bbox.center
        cx_b, cy_b = b.bbox.center
        dist = float(np.hypot(cx_a - cx_b, cy_a - cy_b))
        size = (a.bbox.width + b.bbox.width) / 2.0
        if size == 0:
            return 0.0
        ratio = size / max(dist, 1e-6)
        return float(min(1.0, max(0.0, ratio - 1.0) / self.distance_ratio)) if ratio > 1.0 else 0.0
