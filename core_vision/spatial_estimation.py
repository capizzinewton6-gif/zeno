"""Spatial estimation: monocular depth and 3D bounding box projection."""

from __future__ import annotations

from typing import List, Optional

import numpy as np

from calculations.spatial_math import intrinsic_matrix, project_point, back_project_pixel
from modeling.three_d_cuboids import Cuboid3D, cuboid_from_2d
from modeling.two_d_boxes import Detection


class SpatialEstimator:
    """Estimate depth and 3D cuboids from 2D detections using camera geometry."""

    def __init__(self, intrinsic: Optional[np.ndarray] = None,
                 reference_height_m: float = 1.7) -> None:
        self.intrinsic = intrinsic if intrinsic is not None else intrinsic_matrix(700, 700, 320, 240)
        self.reference_height_m = reference_height_m
        self._depth_model = None

    def estimate_depth(self, image: np.ndarray, bbox_xyxy) -> float:
        """Estimate metric depth for a box. Uses MiDaS if available, else geometry proxy."""
        depth = self._depth_midas(image)
        if depth is not None:
            x1, y1, x2, y2 = bbox_xyxy
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            cx = max(0, min(cx, depth.shape[1] - 1))
            cy = max(0, min(cy, depth.shape[0] - 1))
            return float(depth[cy, cx])
        return self._geometry_depth(bbox_xyxy)

    def _depth_midas(self, image: np.ndarray) -> Optional[np.ndarray]:
        if self._depth_model is not None:
            return self._depth_model(image)
        try:
            import torch  # type: ignore
            from torchvision.transforms.functional import to_tensor  # type: ignore
            model = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
            model.eval()
            self._depth_model = lambda img: model(to_tensor(img).unsqueeze(0).float()).squeeze().detach().numpy()
            return self._depth_model(image)
        except Exception:
            return None

    def _geometry_depth(self, bbox_xyxy) -> float:
        x1, y1, x2, y2 = bbox_xyxy
        height_px = max(1.0, y2 - y1)
        focal_px = self.intrinsic[1, 1]
        return float(self.reference_height_m * focal_px / height_px)

    def to_cuboid(self, detection: Detection, image: np.ndarray) -> Cuboid3D:
        depth = self.estimate_depth(image, detection.bbox.to_xyxy())
        return cuboid_from_2d(detection.bbox.to_xyxy(), depth, self.intrinsic,
                              label=detection.label, confidence=detection.confidence)
