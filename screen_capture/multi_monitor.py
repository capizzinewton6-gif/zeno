"""Handle multiple displays."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class MultiMonitor:
    """Discovers and manages multiple monitors."""

    def __init__(self) -> None:
        self._cached: List[Dict[str, Any]] = []

    def list_monitors(self) -> List[Dict[str, Any]]:
        try:
            import mss  # type: ignore
            with mss.mss() as sct:
                monitors = []
                for i, mon in enumerate(sct.monitors):
                    monitors.append({
                        "index": i,
                        "left": mon.get("left", 0),
                        "top": mon.get("top", 0),
                        "width": mon.get("width", 0),
                        "height": mon.get("height", 0),
                        "is_primary": i == 0,
                    })
                self._cached = monitors
                return monitors
        except Exception as exc:
            logger.debug("mss not available (%s); returning virtual monitor.", exc)
            virtual = [{
                "index": 0, "left": 0, "top": 0,
                "width": 1920, "height": 1080, "is_primary": True,
            }]
            self._cached = virtual
            return virtual

    @property
    def count(self) -> int:
        if not self._cached:
            self.list_monitors()
        return max(0, len(self._cached) - 1)  # index 0 is the virtual "all" monitor

    def get_primary(self) -> Dict[str, Any]:
        monitors = self._cached or self.list_monitors()
        return monitors[0]

    def get_monitor(self, index: int) -> Dict[str, Any] | None:
        monitors = self._cached or self.list_monitors()
        for mon in monitors:
            if mon["index"] == index:
                return mon
        return None

    def total_bounds(self) -> Dict[str, int]:
        monitors = self._cached or self.list_monitors()
        if not monitors:
            return {"left": 0, "top": 0, "width": 0, "height": 0}
        left = min(m["left"] for m in monitors)
        top = min(m["top"] for m in monitors)
        right = max(m["left"] + m["width"] for m in monitors)
        bottom = max(m["top"] + m["height"] for m in monitors)
        return {"left": left, "top": top, "width": right - left, "height": bottom - top}
