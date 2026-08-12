"""Hardware-accelerated annotated video recording engine."""

from __future__ import annotations

import os
from typing import Optional, Tuple

import numpy as np


class VideoWriter:
    """Write annotated frames to MP4/AVI with optional GPU encoding."""

    def __init__(self, path: str, fps: float = 30.0,
                 frame_size: Tuple[int, int] = (640, 480),
                 codec: str = "mp4v") -> None:
        self.path = path
        self.fps = fps
        self.frame_size = frame_size
        self.codec = codec
        self._writer = None

    def open(self) -> bool:
        try:
            import cv2  # type: ignore
            fourcc = cv2.VideoWriter_fourcc(*self.codec)
            os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
            self._writer = cv2.VideoWriter(self.path, fourcc, self.fps, self.frame_size)
            return self._writer.isOpened()
        except Exception:
            self._writer = None
            return False

    def write(self, frame: np.ndarray) -> bool:
        if self._writer is None:
            return False
        try:
            import cv2  # type: ignore
            if frame.shape[1] != self.frame_size[0] or frame.shape[0] != self.frame_size[1]:
                frame = cv2.resize(frame, self.frame_size)
            self._writer.write(frame)
            return True
        except Exception:
            return False

    def release(self) -> None:
        if self._writer is not None:
            try:
                self._writer.release()
            except Exception:
                pass
            self._writer = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *exc):
        self.release()
