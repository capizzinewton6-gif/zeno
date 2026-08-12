"""Post-processor: NMS, confidence thresholding, and filtering."""

from __future__ import annotations

from typing import List

import numpy as np

from calculations.bbox_geometry import iou as _iou
from modeling.two_d_boxes import Detection, Detections
from modeling.detection_rules import DetectionRules


def confidence_filter(detections: List[Detection], threshold: float) -> List[Detection]:
    return [d for d in detections if d.confidence >= threshold]


def non_max_suppression(detections: List[Detection], iou_threshold: float = 0.45) -> List[Detection]:
    """Greedy per-label NMS. Returns surviving detections."""
    if not detections:
        return []
    kept: List[Detection] = []
    by_label: dict = {}
    for d in detections:
        by_label.setdefault(d.label, []).append(d)
    for label, group in by_label.items():
        group.sort(key=lambda d: d.confidence, reverse=True)
        suppressed = [False] * len(group)
        for i in range(len(group)):
            if suppressed[i]:
                continue
            kept.append(group[i])
            for j in range(i + 1, len(group)):
                if suppressed[j]:
                    continue
                if _iou(group[i].bbox.to_xyxy(), group[j].bbox.to_xyxy()) > iou_threshold:
                    suppressed[j] = True
    return kept


class PostProcessor:
    """Applies rules + NMS to raw detector output."""

    def __init__(self, rules: DetectionRules = DetectionRules(), iou_threshold: float = 0.45) -> None:
        self.rules = rules
        self.iou_threshold = iou_threshold

    def process(self, detections: List[Detection], frame_index: int = -1,
                timestamp: float = 0.0, image_shape=(0, 0)) -> Detections:
        passed = [d for d in detections if self.rules.passes(d.label, d.confidence, d.bbox)]
        kept = non_max_suppression(passed, self.iou_threshold)
        return Detections(items=kept, frame_index=frame_index, timestamp=timestamp,
                          image_shape=image_shape)
