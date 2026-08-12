"""Startup sequence - orchestrates the cinematic boot experience."""

from __future__ import annotations

from typing import Optional


class StartupSequence:
    """Drives: arc reactor -> room scan -> grid -> dashboard -> greeting."""

    def __init__(self, reactor, grid, dashboard, ui=None):
        self.reactor = reactor
        self.grid = grid
        self.dashboard = dashboard
        self.ui = ui

    def run(self, user: str = "Operator"):
        # 1. Arc reactor powers on.
        self.reactor.power_on()
        # 2. Room spatially scanned.
        if self.ui:
            self.ui.progress("Scanning spatial environment", total=100, sleep=0.01)
            self.ui.speak("Spatial scan complete. Environment mapped.")
        # 3. Holographic grid appears.
        self.grid.raise_grid()
        # 4. Telemetry dashboard materialises.
        self.dashboard.materialise()
        # 5. Voice greets the user.
        if self.ui:
            self.ui.speak(f"Good evening, {user}. All systems are operational and at your service.")
        return {
            "reactor": self.reactor.status(),
            "grid": self.grid.status(),
            "boot": "complete",
        }

    def execute(self, task: str, context=None):
        if task in ("boot", "run", "start"):
            user = (context or {}).get("user", "Operator")
            return self.run(user=user)
        return {"module": "startup", "task": task, "status": "unknown"}
