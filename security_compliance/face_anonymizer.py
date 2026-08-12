"""Face anonymizer: live face blurring and pixelation for privacy compliance."""

from __future__ import annotations

from typing import List

import numpy as np

from modeling.two_d_boxes import BBox


class FaceAnonymizer:
    """Blur or pixelate face regions on a frame."""

    def __init__(self, method: str = "blur", strength: int = 51,
                 pixel_block: int = 12) -> None:
        self.method = method
        self.strength = strength
        self.pixel_block = pixel_block

    def anonymize(self, image: np.ndarray, boxes: List[BBox]) -> np.ndarray:
        out = image.copy()
        for box in boxes:
            x1, y1, x2, y2 = box.to_int_tuple()
            h, w = out.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            if x2 <= x1 or y2 <= y1:
                continue
            region = out[y1:y2, x1:x2]
            out[y1:y2, x1:x2] = self._apply(region)
        return out

    def _apply(self, region: np.ndarray) -> np.ndarray:
        try:
            import cv2  # type: ignore
            if self.method == "pixelate":
                small = cv2.resize(region, (max(1, region.shape[1] // self.pixel_block),
                                           max(1, region.shape[0] // self.pixel_block)))
                return cv2.resize(small, (region.shape[1], region.shape[0]),
                                  interpolation=cv2.INTER_NEAREST)
            k = self.strength if self.strength % 2 == 1 else self.strength + 1
            return cv2.GaussianBlur(region, (k, k), 30)
        except Exception:
            # Fallback: simple downscale-upscale pixelation with numpy
            block = max(1, self.pixel_block)
            rh = max(1, region.shape[0] // block)
            rw = max(1, region.shape[1] // block)
            small = region[::block, ::block]
            return np.repeat(np.repeat(small, block, axis=0), block, axis=1)[:region.shape[0], :region.shape[1]]
