"""Capture live screen content."""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


class ScreenRecorder:
    """Continuously captures the screen at a target frame rate."""

    def __init__(self, fps: int = 30, monitor: int = 0, on_frame: Optional[Callable] = None) -> None:
        self.fps = fps
        self.monitor = monitor
        self.on_frame = on_frame
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._frame_count = 0
        self._last_frame: Any = None

    def _grab(self) -> Any:
        try:
            import mss  # type: ignore
            with mss.mss() as sct:
                monitors = sct.monitors
                idx = min(self.monitor + 1, len(monitors) - 1) if len(monitors) > 1 else 0
                shot = sct.grab(monitors[idx])
                return shot
        except Exception as exc:
            logger.debug("mss capture failed: %s", exc)
            return None

    def _loop(self) -> None:
        interval = 1.0 / max(self.fps, 1)
        while self._running:
            start = time.time()
            frame = self._grab()
            if frame is not None:
                self._last_frame = frame
                self._frame_count += 1
                if self.on_frame:
                    try:
                        self.on_frame(frame)
                    except Exception as exc:
                        logger.warning("on_frame callback error: %s", exc)
            elapsed = time.time() - start
            time.sleep(max(0.0, interval - elapsed))

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.info("ScreenRecorder started at %d fps", self.fps)

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None

    def grab_frame(self) -> Any:
        """Grab a single frame synchronously."""
        return self._grab()

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def frame_count(self) -> int:
        return self._frame_count

    @property
    def last_frame(self) -> Any:
        return self._last_frame
