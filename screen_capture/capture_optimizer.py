"""Optimize screen capture speed."""

from __future__ import annotations

import hashlib
import logging
import time
from typing import Any, Optional

logger = logging.getLogger(__name__)


class CaptureOptimizer:
    """Reduces redundant work during continuous screen capture.

    Strategies:
    - Frame deduplication via perceptual hash (skip identical frames).
    - Dynamic FPS throttling when frames change infrequently.
    - Region-of-interest cropping.
    """

    def __init__(self, change_threshold: float = 0.01, min_fps: int = 5,
                 max_fps: int = 30) -> None:
        self.change_threshold = change_threshold
        self.min_fps = min_fps
        self.max_fps = max_fps
        self._last_hash: Optional[str] = None
        self._unchanged_streak = 0
        self._current_fps = max_fps

    def should_process(self, frame: Any) -> bool:
        """Return True if the frame differs enough from the last to process."""
        h = self._hash(frame)
        if self._last_hash is None:
            self._last_hash = h
            self._unchanged_streak = 0
            return True
        if h == self._last_hash:
            self._unchanged_streak += 1
            self._adjust_fps()
            return False
        self._last_hash = h
        self._unchanged_streak = 0
        self._current_fps = self.max_fps
        return True

    def _adjust_fps(self) -> None:
        if self._unchanged_streak > 10:
            self._current_fps = self.min_fps
        elif self._unchanged_streak > 3:
            self._current_fps = max(self.min_fps, self._current_fps - 2)

    @property
    def current_fps(self) -> int:
        return self._current_fps

    @staticmethod
    def _hash(frame: Any) -> str:
        try:
            import numpy as np  # type: ignore
            if hasattr(frame, "rgb"):
                arr = np.frombuffer(frame.rgb, dtype=np.uint8)
                return hashlib.md5(arr[::1024].tobytes()).hexdigest()
            if isinstance(frame, (bytes, bytearray)):
                return hashlib.md5(bytes(frame[::1024])).hexdigest()
        except Exception:
            pass
        return hashlib.md5(str(id(frame)).encode()).hexdigest()

    def crop_region(self, frame: Any, region: tuple[int, int, int, int]) -> Any:
        """Crop a region (x, y, w, h) from a frame if possible."""
        try:
            import numpy as np  # type: ignore
            from PIL import Image  # type: ignore
            x, y, w, h = region
            if hasattr(frame, "rgb") and hasattr(frame, "size"):
                img = Image.frombytes("RGB", frame.size, frame.rgb)
                return img.crop((x, y, x + w, y + h))
        except Exception as exc:
            logger.debug("crop_region failed: %s", exc)
        return frame
