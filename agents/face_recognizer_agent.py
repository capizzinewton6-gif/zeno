"""Face recognizer agent: manages facial identification and embedding lookups."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from core_vision.face_recognition import FaceRecognizer
from facial_processing.anti_spoofing import AntiSpoofing
from facial_processing.identity_resolver import IdentityResolver
from modeling.two_d_boxes import Detection, Detections
from tracking_analytics.object_tracker import Track


@dataclass
class FaceResult:
    detections: Detections
    known_count: int
    unknown_count: int
    spoof_flags: List[bool]


class FaceRecognizerAgent:
    """Detect, recognize, liveness-check, and temporally resolve identities."""

    def __init__(self, recognizer: Optional[FaceRecognizer] = None,
                 anti_spoof: Optional[AntiSpoofing] = None,
                 resolver: Optional[IdentityResolver] = None) -> None:
        self.recognizer = recognizer or FaceRecognizer()
        self.anti_spoof = anti_spoof or AntiSpoofing()
        self.resolver = resolver or IdentityResolver()

    def run(self, image: np.ndarray, tracks: Optional[List[Track]] = None,
            frame_index: int = -1, timestamp: float = 0.0) -> FaceResult:
        dets = self.recognizer.recognize(image)
        known = unknown = 0
        spoof_flags: List[bool] = []
        for d in dets:
            if d.identity:
                known += 1
            else:
                unknown += 1
            face = image[d.bbox.y1:d.bbox.y2, d.bbox.x1:d.bbox.x2]
            live = self.anti_spoof.check(face).is_live
            spoof_flags.append(not live)
        return FaceResult(
            detections=Detections(items=dets, frame_index=frame_index,
                                  timestamp=timestamp, image_shape=image.shape[:2]),
            known_count=known, unknown_count=unknown, spoof_flags=spoof_flags)
