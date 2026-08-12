"""Tunable pipeline parameters: frame rates, confidence cutoffs, IOU thresholds."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Tuple


@dataclass
class Parameters:
    """Central parameter bundle. Loaded from config/settings.json at startup."""

    target_fps: int = 30
    frame_skip: int = 0
    jpeg_quality: int = 85

    detection_confidence: float = 0.40
    face_match_threshold: float = 0.55
    nms_iou_threshold: float = 0.45

    tracking_max_age: int = 30
    tracking_min_hits: int = 3
    tracking_iou_threshold: float = 0.30

    embedding_dim: int = 512
    input_size: Tuple[int, int] = (640, 640)  # (h, w)

    anonymize_unknown_faces: bool = False
    save_annotated_frames: bool = True
    telemetry: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_settings(cls, settings: dict) -> "Parameters":
        return cls(
            target_fps=int(settings.get("default_fps_target", 30)),
            frame_skip=int(settings.get("frame_skip", 0)),
            jpeg_quality=int(settings.get("jpeg_quality", 85)),
            detection_confidence=float(settings.get("detection_confidence_threshold", 0.40)),
            face_match_threshold=float(settings.get("face_match_threshold", 0.55)),
            nms_iou_threshold=float(settings.get("nms_iou_threshold", 0.45)),
            tracking_max_age=int(settings.get("tracking_max_age_frames", 30)),
            tracking_min_hits=int(settings.get("min_hits", 3)),
            anonymize_unknown_faces=bool(settings.get("anonymize_unknown_faces", False)),
            save_annotated_frames=bool(settings.get("save_annotated_frames", True)),
        )
