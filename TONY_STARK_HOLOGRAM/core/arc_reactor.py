"""Arc reactor - power core with boot animation."""

from __future__ import annotations

import time
from typing import Optional


class ArcReactor:
    """Powers on the holographic stack and reports power state."""

    def __init__(self, ui=None, capacity: float = 8.0):
        self.ui = ui
        self.capacity = capacity  # gigajoules
        self.level = 0.0
        self.online = False

    def power_on(self):
        if self.ui:
            self.ui.arc_reactor()
        steps = 40
        for i in range(steps + 1):
            self.level = self.capacity * (i / steps)
            time.sleep(0.02)
        self.online = True
        if self.ui:
            self.ui.speak(f"Arc reactor online at {self.level:.1f} GJ capacity.")

    def status(self) -> dict:
        return {
            "online": self.online,
            "level_gj": round(self.level, 2),
            "capacity_gj": self.capacity,
            "load_pct": round(100 * (self.level / self.capacity), 1) if self.capacity else 0,
        }

    def execute(self, task: str, context=None):
        if task in ("power_on", "on", "boot"):
            self.power_on()
            return self.status()
        if task in ("status", "report"):
            return self.status()
        return {"module": "arc_reactor", "task": task, "status": "unknown"}
