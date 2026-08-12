"""High-speed overlay drawing of bounding boxes, text, and masks."""

from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np

from modeling.two_d_boxes import Detection

# A simple color palette (BGR) for common labels.
PALETTE = [
    (0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0),
    (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0),
]


class OverlayRenderer:
    """Draw detections, labels, and masks onto frames."""

    def __init__(self, thickness: int = 2, font_scale: float = 0.5) -> None:
        self.thickness = thickness
        self.font_scale = font_scale

    def render(self, image: np.ndarray, detections: List[Detection],
               anonymize: bool = False) -> np.ndarray:
        out = image.copy()
        for i, d in enumerate(detections):
            color = PALETTE[hash(d.label) % len(PALETTE)]
            x1, y1, x2, y2 = d.bbox.to_int_tuple()
            self._rectangle(out, x1, y1, x2, y2, color)
            label_text = self._label_text(d)
            self._text(out, label_text, (x1, max(0, y1 - 5)), color)
        return out

    def _label_text(self, d: Detection) -> str:
        parts = [d.label, f"{d.confidence:.2f}"]
        if d.identity:
            parts.append(d.identity)
        return " ".join(parts)

    def _rectangle(self, img, x1, y1, x2, y2, color) -> None:
        try:
            import cv2  # type: ignore
            cv2.rectangle(img, (x1, y1), (x2, y2), color, self.thickness)
        except Exception:
            h, w = img.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            img[y1:y2, x1:x1 + self.thickness] = color
            img[y1:y2, x2:x2 + self.thickness] = color
            img[y1:y1 + self.thickness, x1:x2] = color
            img[y2:y2 + self.thickness, x1:x2] = color

    def _text(self, img, text, org, color) -> None:
        try:
            import cv2  # type: ignore
            cv2.putText(img, text, org, cv2.FONT_HERSHEY_SIMPLEX,
                        self.font_scale, color, 1, cv2.LINE_AA)
        except Exception:
            pass
