"""Control mouse actions."""

from __future__ import annotations

import logging
import time
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class MouseController:
    """Programmatic mouse control with safety guards."""

    def __init__(self, default_duration: float = 0.3, safe_mode: bool = True) -> None:
        self.default_duration = default_duration
        self.safe_mode = safe_mode
        self._ensure_available()

    def _ensure_available(self) -> None:
        try:
            import pyautogui  # type: ignore
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.1
        except Exception as exc:
            logger.warning("pyautogui unavailable; mouse control disabled: %s", exc)

    @staticmethod
    def position() -> Tuple[int, int]:
        try:
            import pyautogui  # type: ignore
            return pyautogui.position()
        except Exception:
            return (0, 0)

    def move(self, x: int, y: int, duration: Optional[float] = None) -> bool:
        if not self._ready():
            return False
        try:
            import pyautogui  # type: ignore
            pyautogui.moveTo(x, y, duration=duration if duration is not None else self.default_duration)
            return True
        except Exception as exc:
            logger.warning("move failed: %s", exc)
            return False

    def click(self, x: Optional[int] = None, y: Optional[int] = None,
              button: str = "left", clicks: int = 1, duration: Optional[float] = None) -> bool:
        if not self._ready():
            return False
        try:
            import pyautogui  # type: ignore
            if x is not None and y is not None:
                pyautogui.click(x, y, button=button, clicks=clicks,
                                duration=duration if duration is not None else self.default_duration)
            else:
                pyautogui.click(button=button, clicks=clicks)
            return True
        except Exception as exc:
            logger.warning("click failed: %s", exc)
            return False

    def double_click(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        return self.click(x, y, clicks=2)

    def right_click(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        return self.click(x, y, button="right")

    def drag(self, x: int, y: int, duration: float = 0.5, button: str = "left") -> bool:
        if not self._ready():
            return False
        try:
            import pyautogui  # type: ignore
            pyautogui.dragTo(x, y, duration=duration, button=button)
            return True
        except Exception as exc:
            logger.warning("drag failed: %s", exc)
            return False

    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        if not self._ready():
            return False
        try:
            import pyautogui  # type: ignore
            pyautogui.scroll(clicks, x=x, y=y)
            return True
        except Exception as exc:
            logger.warning("scroll failed: %s", exc)
            return False

    def move_relative(self, dx: int, dy: int) -> bool:
        if not self._ready():
            return False
        try:
            import pyautogui  # type: ignore
            pyautogui.moveRel(dx, dy, duration=self.default_duration)
            return True
        except Exception as exc:
            logger.warning("move_relative failed: %s", exc)
            return False

    def _ready(self) -> bool:
        try:
            import pyautogui  # type: ignore  # noqa: F401
            return True
        except Exception:
            return False
