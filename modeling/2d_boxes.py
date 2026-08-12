"""2D bounding box data structures and coordinate math.

These dataclasses are the lingua franca of the whole pipeline. They use pure
Python + numpy only and have no dependency on OpenCV so they can be used in any
context (local math, tests, agents).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence, Tuple, Union

import numpy as np

Box = Sequence[float]  # [x1, y1, x2, y2]


@dataclass
class BBox:
    """Axis-aligned 2D bounding box in [x1, y1, x2, y2] pixel coordinates."""

    x1: float
    y1: float
    x2: float
    y2: float

    @classmethod
    def from_xywh(cls, x: float, y: float, w: float, h: float) -> "BBox":
        return cls(float(x), float(y), float(x + w), float(y + h))

    @classmethod
    def from_xyxy(cls, box: Sequence[float]) -> "BBox":
        return cls(float(box[0]), float(box[1]), float(box[2]), float(box[3]))

    def to_xyxy(self) -> List[float]:
        return [self.x1, self.y1, self.x2, self.y2]

    def to_xywh(self) -> List[float]:
        return [self.x1, self.y1, self.width, self.height]

    @property
    def width(self) -> float:
        return max(0.0, self.x2 - self.x1)

    @property
    def height(self) -> float:
        return max(0.0, self.y2 - self.y1)

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def cx(self) -> float:
        return (self.x1 + self.x2) / 2.0

    @property
    def cy(self) -> float:
        return (self.y1 + self.y2) / 2.0

    @property
    def center(self) -> Tuple[float, float]:
        return (self.cx, self.cy)

    def clip(self, width: float, height: float) -> "BBox":
        return BBox(
            max(0.0, min(self.x1, width)),
            max(0.0, min(self.y1, height)),
            max(0.0, min(self.x2, width)),
            max(0.0, min(self.y2, height)),
        )

    def scale(self, sx: float, sy: float) -> "BBox":
        return BBox(self.x1 * sx, self.y1 * sy, self.x2 * sx, self.y2 * sy)

    def to_int_tuple(self) -> Tuple[int, int, int, int]:
        return (int(self.x1), int(self.y1), int(self.x2), int(self.y2))

    def to_numpy(self) -> np.ndarray:
        return np.array([self.x1, self.y1, self.x2, self.y2], dtype=np.float32)

    def __repr__(self) -> str:  # pragma: no cover
        return f"BBox(x1={self.x1:.1f}, y1={self.y1:.1f}, x2={self.x2:.1f}, y2={self.y2:.1f})"


@dataclass
class Detection:
    """A single detection result produced by any detector in the pipeline."""

    label: str
    confidence: float
    bbox: BBox
    track_id: int = -1
    identity: str = ""
    embedding: List[float] = field(default_factory=list)
    attributes: dict = field(default_factory=dict)
    source: str = ""  # which module produced it

    @classmethod
    def from_xyxy(cls, label: str, conf: float, box: Sequence[float], **kw) -> "Detection":
        return cls(label=label, confidence=float(conf), bbox=BBox.from_xyxy(box), **kw)

    @classmethod
    def from_xywh(cls, label: str, conf: float, x: float, y: float, w: float, h: float, **kw) -> "Detection":
        return cls(label=label, confidence=float(conf), bbox=BBox.from_xywh(x, y, w, h), **kw)

    @property
    def cx(self) -> float:
        return self.bbox.cx

    @property
    def cy(self) -> float:
        return self.bbox.cy

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "confidence": round(float(self.confidence), 4),
            "bbox": self.bbox.to_xyxy(),
            "track_id": self.track_id,
            "identity": self.identity,
            "source": self.source,
        }


@dataclass
class Detections:
    """A collection of detections for a single frame."""

    items: List[Detection] = field(default_factory=list)
    frame_index: int = -1
    timestamp: float = 0.0
    image_shape: Tuple[int, int] = (0, 0)  # (h, w)

    def __iter__(self):
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def add(self, d: Detection) -> None:
        self.items.append(d)

    def filter_label(self, label: str) -> List[Detection]:
        return [d for d in self.items if d.label == label]

    def labels(self) -> List[str]:
        return sorted({d.label for d in self.items})

    def to_dict(self) -> dict:
        return {"frame_index": self.frame_index, "timestamp": self.timestamp,
                "image_shape": list(self.image_shape),
                "detections": [d.to_dict() for d in self.items]}


def xyxy_to_xywh(box: Sequence[float]) -> List[float]:
    return [float(box[0]), float(box[1]), float(box[2]) - float(box[0]), float(box[3]) - float(box[1])]


def xywh_to_xyxy(box: Sequence[float]) -> List[float]:
    return [float(box[0]), float(box[1]), float(box[0] + box[2]), float(box[1] + box[3])]


def boxes_to_numpy(boxes: Sequence[Union[Sequence[float], BBox]]) -> np.ndarray:
    rows = [b.to_xyxy() if isinstance(b, BBox) else list(b) for b in boxes]
    return np.asarray(rows, dtype=np.float32)
