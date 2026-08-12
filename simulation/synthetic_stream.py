"""Synthetic stream: simulate webcam input from looped video files or RTSP."""

from __future__ import annotations

import os
import time
from typing import Iterator, Optional

import numpy as np

from core_vision.camera_stream import Frame


class SyntheticStream:
    """Loop a video file (or generate synthetic frames) as a camera-like stream."""

    def __init__(self, source: Optional[str] = None, fps: float = 30.0,
                 resolution=(640, 480)) -> None:
        self.source = source
        self.fps = fps
        self.resolution = resolution
        self._cap = None
        self._frame_index = 0
        self._period = 1.0 / fps if fps > 0 else 0.0

    def open(self) -> bool:
        if self.source and os.path.exists(self.source):
            try:
                import cv2  # type: ignore
                self._cap = cv2.VideoCapture(self.source)
                return self._cap.isOpened()
            except Exception:
                self._cap = None
        return self.source is None or not os.path.exists(self.source)

    def read(self) -> Optional[Frame]:
        image = None
        if self._cap is not None:
            ok, image = self._cap.read()
            if not ok:
                self._cap.set(2, 0)  # loop back
                ok, image = self._cap.read()
            if not ok:
                return None
        else:
            # Procedural synthetic frame with a moving square
            w, h = self.resolution
            image = np.zeros((h, w, 3), dtype=np.uint8)
            x = (self._frame_index * 5) % w
            y = h // 2
            image[y:y + 40, x:x + 40] = (0, 255, 0)
        frame = Frame(index=self._frame_index, image=image, timestamp=time.time())
        self._frame_index += 1
        if self._period:
            time.sleep(self._period)
        return frame

    def __iter__(self) -> Iterator[Frame]:
        while True:
            f = self.read()
            if f is None:
                break
            yield f

    def release(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None
