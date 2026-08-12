"""Detection rules: class filters, ROIs, exclusion zones."""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from modeling import parameters as params_module
from modeling.two_d_boxes import BBox


class DetectionRules:
    """Rule engine applied after detection to accept/reject detections."""

    def __init__(self, parameters: Optional[params_module.Parameters] = None) -> None:
        self.parameters = parameters or params_module.Parameters()
        self.include_labels: Optional[set] = None
        self.exclude_labels: set = set()
        self.rois: List["BBox"] = []          # accept only if center inside an ROI
        self.exclusion_zones: List["BBox"] = []  # reject if center inside

    # -- configuration ---------------------------------------------------
    def set_include_labels(self, labels: Optional[Sequence[str]]) -> None:
        self.include_labels = set(labels) if labels else None

    def add_exclusion_label(self, label: str) -> None:
        self.exclude_labels.add(label)

    def add_roi(self, box: "BBox") -> None:
        self.rois.append(box)

    def add_exclusion_zone(self, box: "BBox") -> None:
        self.exclusion_zones.append(box)

    # -- predicates ------------------------------------------------------
    def _label_ok(self, label: str) -> bool:
        if label in self.exclude_labels:
            return False
        if self.include_labels is not None and label not in self.include_labels:
            return False
        return True

    def _in_zone(self, center: Tuple[float, float], zones: Sequence["BBox"]) -> bool:
        cx, cy = center
        for z in zones:
            if z.x1 <= cx <= z.x2 and z.y1 <= cy <= z.y2:
                return True
        return False

    # -- public ----------------------------------------------------------
    def passes(self, label: str, confidence: float, bbox: "BBox") -> bool:
        if not self._label_ok(label):
            return False
        if confidence < self.parameters.detection_confidence:
            return False
        center = bbox.center
        if self.rois and not self._in_zone(center, self.rois):
            return False
        if self._in_zone(center, self.exclusion_zones):
            return False
        return True
