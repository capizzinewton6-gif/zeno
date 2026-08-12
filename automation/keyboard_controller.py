"""Control keyboard input."""

from __future__ import annotations

import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)


class KeyboardController:
    """Programmatic keyboard control."""

    def __init__(self, default_delay: float = 0.05) -> None:
        self.default_delay = default_delay

    @staticmethod
    def _ready() -> bool:
        try:
            import pyautogui  # type: ignore  # noqa: F401
            return True
        except Exception:
            return False

    def type(self, text: str, interval: Optional[float] = None) -> bool:
        if not self._ready():
            logger.warning("Keyboard unavailable; cannot type.")
            return False
        try:
            import pyautogui  # type: ignore
            pyautogui.typewrite(text, interval=interval if interval is not None else self.default_delay)
            return True
        except Exception as exc:
            logger.warning("type failed: %s", exc)
            return False

    def press(self, key: str, presses: int = 1) -> bool:
        if not self._ready():
            return False
        try:
            import pyautogui  # type: ignore
            pyautogui.press(key, presses=presses)
            return True
        except Exception as exc:
            logger.warning("press failed: %s", exc)
            return False

    def hotkey(self, *keys) -> bool:
        if not self._ready():
            return False
        try:
            import pyautogui  # type: ignore
            pyautogui.hotkey(*keys)
            return True
        except Exception as exc:
            logger.warning("hotkey failed: %s", exc)
            return False

    def key_down(self, key: str) -> bool:
        if not self._ready():
            return False
        try:
            import pyautogui  # type: ignore
            pyautogui.keyDown(key)
            return True
        except Exception:
            return False

    def key_up(self, key: str) -> bool:
        if not self._ready():
            return False
        try:
            import pyautogui  # type: ignore
            pyautogui.keyUp(key)
            return True
        except Exception:
            return False

    def enter(self) -> bool:
        return self.press("enter")

    def tab(self) -> bool:
        return self.press("tab")

    def escape(self) -> bool:
        return self.press("escape")

    def ctrl(self, key: str) -> bool:
        return self.hotkey("ctrl", key)
