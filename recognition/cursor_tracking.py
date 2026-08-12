"""Track mouse position."""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


class CursorTracking:
    """Tracks and reports the mouse cursor position."""

    def __init__(self, poll_interval: float = 0.05) -> None:
        self.poll_interval = poll_interval
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._position: tuple[int, int] = (0, 0)
        self._velocity: tuple[int, int] = (0, 0)
        self._last_pos: tuple[int, int] = (0, 0)
        self._last_time: float = 0.0
        self._subscribers: list[Callable[[tuple[int, int]], None]] = []

    def current_position(self) -> tuple[int, int]:
        try:
            import pyautogui  # type: ignore
            self._position = pyautogui.position()
        except Exception as exc:
            logger.debug("pyautogui unavailable (%s); returning last known position.", exc)
        return self._position

    def subscribe(self, callback: Callable[[tuple[int, int]], None]) -> None:
        self._subscribers.append(callback)

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None

    def _loop(self) -> None:
        while self._running:
            pos = self.current_position()
            now = time.time()
            if pos != self._last_pos:
                dt = max(now - self._last_time, 1e-6)
                self._velocity = (
                    int((pos[0] - self._last_pos[0]) / dt),
                    int((pos[1] - self._last_pos[1]) / dt),
                )
                self._last_pos = pos
                self._last_time = now
                self._position = pos
                for sub in list(self._subscribers):
                    try:
                        sub(pos)
                    except Exception as exc:
                        logger.warning("cursor subscriber error: %s", exc)
            time.sleep(self.poll_interval)

    @property
    def position(self) -> tuple[int, int]:
        return self.current_position()

    @property
    def velocity(self) -> tuple[int, int]:
        return self._velocity
