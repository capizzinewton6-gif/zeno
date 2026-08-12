"""Process live frames as a stream."""

from __future__ import annotations

import collections
import logging
import threading
import time
from typing import Any, Callable, Optional

from screen_capture.screen_recorder import ScreenRecorder

logger = logging.getLogger(__name__)


class FrameStream:
    """Buffers and dispatches live frames to subscribers."""

    def __init__(self, fps: int = 30, buffer_size: int = 30, monitor: int = 0) -> None:
        self.fps = fps
        self.buffer_size = buffer_size
        self._buffer: collections.deque = collections.deque(maxlen=buffer_size)
        self._subscribers: list[Callable[[Any], None]] = []
        self._recorder = ScreenRecorder(fps=fps, monitor=monitor, on_frame=self._on_frame)
        self._lock = threading.Lock()

    def _on_frame(self, frame: Any) -> None:
        timestamp = time.time()
        with self._lock:
            self._buffer.append({"timestamp": timestamp, "frame": frame})
            subs = list(self._subscribers)
        for sub in subs:
            try:
                sub(frame, timestamp)
            except Exception as exc:
                logger.warning("Subscriber error: %s", exc)

    def subscribe(self, callback: Callable[[Any, float], None]) -> None:
        with self._lock:
            self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[Any, float], None]) -> None:
        with self._lock:
            if callback in self._subscribers:
                self._subscribers.remove(callback)

    def start(self) -> None:
        self._recorder.start()

    def stop(self) -> None:
        self._recorder.stop()

    @property
    def latest(self) -> Optional[dict]:
        with self._lock:
            return self._buffer[-1] if self._buffer else None

    @property
    def buffered_frames(self) -> list:
        with self._lock:
            return list(self._buffer)

    def clear(self) -> None:
        with self._lock:
            self._buffer.clear()
