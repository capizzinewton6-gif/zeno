"""Re-export of the digit-prefixed ``2d_boxes`` module.

``2d_boxes`` cannot be imported with a normal ``import`` statement because the
module name starts with a digit. This module loads it via importlib and exposes
its public symbols so the rest of the codebase can simply do::

    from modeling.two_d_boxes import BBox, Detection, Detections
"""

from __future__ import annotations

import importlib.util
import os
import sys

_SPEC = importlib.util.spec_from_file_location(
    "modeling.two_d_boxes_impl",
    os.path.join(os.path.dirname(__file__), "2d_boxes.py"),
)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MODULE  # required for dataclasses to resolve __module__
_SPEC.loader.exec_module(_MODULE)

BBox = _MODULE.BBox
Detection = _MODULE.Detection
Detections = _MODULE.Detections
xyxy_to_xywh = _MODULE.xyxy_to_xywh
xywh_to_xyxy = _MODULE.xywh_to_xyxy
boxes_to_numpy = _MODULE.boxes_to_numpy

__all__ = ["BBox", "Detection", "Detections", "xyxy_to_xywh", "xywh_to_xyxy", "boxes_to_numpy"]
