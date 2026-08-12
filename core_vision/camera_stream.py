"""Camera stream capture pipeline: RTSP, WebCam, USB camera."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Iterator, Optional, Tuple

import numpy as np

from calculations.latency_metrics import LatencyMetrics


@dataclass
class Frame:
    index: int
    image: np.ndarray
    timestamp: float


class CameraStream:
    """Unified capture for RTSP / webcam / USB cameras via OpenCV."""

    def __init__(self, source: str | int = 0, resolution: Optional[Tuple[int, int]] = None,
                 fps_target: int = 30) -> None:
        self.source = source
        self.resolution = resolution
        self.fps_target = fps_target
        self._cap = None
        self._frame_index = 0
        self.metrics = LatencyMetrics()

    def open(self) -> bool:
        try:
            import cv2  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"OpenCV unavailable: {exc}")
        self._cap = cv2.VideoCapture(self.source if not isinstance(self.source, int) else self.source)
        if not self._cap.isOpened():
            return False
        if self.resolution:
            self._cap.set(3, self.resolution[0])
            self._cap.set(4, self.resolution[1])
        if self.fps_target:
            self._cap.set(5, self.fps_target)
        return True

    def is_open(self) -> bool:
        return self._cap is not None and self._cap.isOpened()

    def read(self) -> Optional[Frame]:
        if not self.is_open():
            return None
        ok, image = self._cap.read()
        if not ok:
            return None
        frame = Frame(index=self._frame_index, image=image, timestamp=time.time())
        self._frame_index += 1
        self.metrics.tick()
        return frame

    def __iter__(self) -> Iterator[Frame]:
        while True:
            frame = self.read()
            if frame is None:
                break
            yield frame

    def release(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *exc):
        self.release()


def list_webcam_indices(max_probe: int = 5) -> list:
    """Probe available webcam indices (best-effort, OpenCV-dependent)."""
    try:
        import cv2  # type: ignore
    except Exception:  # pragma: no cover
        return []
    found = []
    for i in range(max_probe):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            found.append(i)
        cap.release()
    return found
