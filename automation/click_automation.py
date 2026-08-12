"""Automated clicking with safety checks."""

from __future__ import annotations

import logging
import time
from typing import Optional, Tuple

from automation.mouse_controller import MouseController
from security.permission_manager import PermissionManager

logger = logging.getLogger(__name__)


class ClickAutomation:
    """High-level automated clicking with permission gating."""

    def __init__(self, mouse: Optional[MouseController] = None,
                 permissions: Optional[PermissionManager] = None) -> None:
        self.mouse = mouse or MouseController()
        self.permissions = permissions or PermissionManager()

    def click_at(self, x: int, y: int, button: str = "left", double: bool = False,
                 confirm: bool = True) -> bool:
        if confirm and not self.permissions.check("click", {"x": x, "y": y}):
            logger.info("Click at (%d, %d) blocked by permission manager.", x, y)
            return False
        if double:
            return self.mouse.double_click(x, y) if button == "left" else self.mouse.click(x, y, button=button, clicks=2)
        return self.mouse.click(x, y, button=button)

    def click_element(self, bbox: Tuple[float, float, float, float],
                      screen_size: Tuple[int, int], confirm: bool = True) -> bool:
        """Click the center of a normalized bbox [x, y, w, h]."""
        nx, ny, nw, nh = bbox
        w, h = screen_size
        cx = int((nx + nw / 2) * w)
        cy = int((ny + nh / 2) * h)
        return self.click_at(cx, cy, confirm=confirm)

    def multi_click(self, points: list[Tuple[int, int]], delay: float = 0.5,
                    confirm: bool = True) -> int:
        count = 0
        for x, y in points:
            if self.click_at(x, y, confirm=confirm):
                count += 1
            time.sleep(delay)
        return count

    def safe_click(self, x: int, y: int) -> bool:
        """Click only after verifying the cursor reaches the target."""
        if not self.mouse.move(x, y):
            return False
        time.sleep(0.1)
        if self.mouse.position() != (x, y):
            logger.warning("Cursor did not reach target (%d, %d).", x, y)
            return False
        return self.mouse.click()
