"""Automated typing with verification."""

from __future__ import annotations

import logging
import time
from typing import Optional

from automation.keyboard_controller import KeyboardController
from security.permission_manager import PermissionManager

logger = logging.getLogger(__name__)


class TypingAutomation:
    """High-level automated typing with permission gating."""

    def __init__(self, keyboard: Optional[KeyboardController] = None,
                 permissions: Optional[PermissionManager] = None) -> None:
        self.keyboard = keyboard or KeyboardController()
        self.permissions = permissions or PermissionManager()

    def type_text(self, text: str, confirm: bool = True, interval: float = 0.05) -> bool:
        if confirm and not self.permissions.check("type", {"text": text}):
            logger.info("Typing blocked by permission manager.")
            return False
        return self.keyboard.type(text, interval=interval)

    def type_into_field(self, text: str, field_bbox: tuple[float, float, float, float],
                       screen_size: tuple[int, int], clear_first: bool = True) -> bool:
        from automation.mouse_controller import MouseController
        mouse = MouseController()
        nx, ny, nw, nh = field_bbox
        w, h = screen_size
        cx = int((nx + nw / 2) * w)
        cy = int((ny + nh / 2) * h)
        if not mouse.click(cx, cy):
            return False
        time.sleep(0.2)
        if clear_first:
            self.keyboard.hotkey("ctrl", "a")
            self.keyboard.press("delete")
            time.sleep(0.1)
        return self.keyboard.type(text)

    def type_secure(self, text: str) -> bool:
        """Type text without logging its content."""
        if not self.permissions.check("type_secure", {}):
            return False
        ok = self.keyboard.type(text)
        logger.info("Typed secure text (length=%d).", len(text))
        return ok

    def paste_text(self, text: str) -> bool:
        import pyperclip  # type: ignore
        try:
            pyperclip.copy(text)
            return self.keyboard.hotkey("ctrl", "v")
        except Exception as exc:
            logger.warning("paste failed, falling back to typing: %s", exc)
            return self.keyboard.type(text)
