"""Frame preprocessor: resize, letterbox, normalize, color space conversion."""

from __future__ import annotations

from typing import Tuple

import numpy as np


class FramePreprocessor:
    """Standardize frames before they reach detectors/engines."""

    def __init__(self, input_size: Tuple[int, int] = (640, 640),
                 normalize: bool = True, swap_rb: bool = True) -> None:
        self.input_size = input_size  # (h, w)
        self.normalize = normalize
        self.swap_rb = swap_rb

    def resize(self, image: np.ndarray) -> np.ndarray:
        try:
            import cv2  # type: ignore
        except Exception:  # pragma: no cover
            h, w = self.input_size
            return np.asarray(image.resize((w, h)) if hasattr(image, "resize") else image)
        return cv2.resize(image, (self.input_size[1], self.input_size[0]))

    def letterbox(self, image: np.ndarray) -> Tuple[np.ndarray, float, Tuple[int, int]]:
        """Resize keeping aspect ratio, pad with gray. Returns (image, scale, pad)."""
        try:
            import cv2  # type: ignore
        except Exception:  # pragma: no cover
            return self.resize(image), 1.0, (0, 0)
        h, w = self.input_size
        ih, iw = image.shape[:2]
        scale = min(w / iw, h / ih)
        nw, nh = int(iw * scale), int(ih * scale)
        resized = cv2.resize(image, (nw, nh))
        canvas = np.full((h, w, 3), 114, dtype=np.uint8)
        top = (h - nh) // 2
        left = (w - nw) // 2
        canvas[top:top + nh, left:left + nw] = resized
        return canvas, scale, (left, top)

    def normalize_(self, image: np.ndarray) -> np.ndarray:
        out = image.astype(np.float32) / 255.0
        if self.swap_rb and out.ndim == 3:
            out = out[:, :, ::-1]
        return out

    def process(self, image: np.ndarray) -> np.ndarray:
        resized, _, _ = self.letterbox(image)
        if self.normalize:
            return self.normalize_(resized)
        return resized

    def to_jpeg_bytes(self, image: np.ndarray, quality: int = 85) -> bytes:
        try:
            import cv2  # type: ignore
            ok, buf = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, int(quality)])
            if ok:
                return buf.tobytes()
        except Exception:  # pragma: no cover
            pass
        from io import BytesIO
        try:
            from PIL import Image  # type: ignore
            bgr = image[:, :, ::-1] if image.ndim == 3 else image
            img = Image.fromarray(bgr)
            bio = BytesIO()
            img.save(bio, format="JPEG", quality=quality)
            return bio.getvalue()
        except Exception:
            return b""


def scale_bbox_back(bbox_xyxy, scale: float, pad: Tuple[int, int]) -> list:
    """Undo letterbox padding/scale on a bbox."""
    x1, y1, x2, y2 = bbox_xyxy
    px, py = pad
    return [(x1 - px) / scale, (y1 - py) / scale, (x2 - px) / scale, (y2 - py) / scale]
