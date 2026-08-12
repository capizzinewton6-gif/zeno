"""Object detector agent: manages object classification and bounding box workflows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from core_vision.object_detection import ObjectDetector
from core_vision.post_processor import PostProcessor
from modeling.two_d_boxes import Detection, Detections
from modeling.detection_rules import DetectionRules


@dataclass
class DetectionResult:
    detections: Detections
    raw_count: int


class ObjectDetectorAgent:
    """Orchestrate detection + post-processing for a single frame."""

    def __init__(self, detector: Optional[ObjectDetector] = None,
                 rules: DetectionRules = DetectionRules()) -> None:
        self.detector = detector or ObjectDetector()
        self.post = PostProcessor(rules=rules)

    def run(self, image: np.ndarray, frame_index: int = -1,
            timestamp: float = 0.0) -> DetectionResult:
        raw = self.detector.detect(image)
        dets = self.post.process(raw, frame_index=frame_index, timestamp=timestamp,
                                 image_shape=image.shape[:2])
        return DetectionResult(detections=dets, raw_count=len(raw))
