"""Telemetry dashboard - live system stats."""

from __future__ import annotations

from typing import Optional

try:
    import psutil

    _HAS_PSUTIL = True
except ImportError:  # pragma: no cover
    psutil = None
    _HAS_PSUTIL = False


class TelemetryDashboard:
    """Materialises a floating panel of live hardware/scene telemetry."""

    def __init__(self, ui=None):
        self.ui = ui
        self.holograms = 0

    def _snapshot(self) -> dict:
        if _HAS_PSUTIL:
            vm = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=None)
            return {
                "cpu_pct": cpu,
                "mem_pct": vm.percent,
                "mem_used_gb": round(vm.used / 1e9, 2),
                "mem_total_gb": round(vm.total / 1e9, 2),
                "holograms": self.holograms,
            }
        return {"cpu_pct": -1, "mem_pct": -1, "mem_used_gb": -1, "mem_total_gb": -1, "holograms": self.holograms}

    def materialise(self):
        snap = self._snapshot()
        if self.ui:
            body = (
                f"CPU        : {snap['cpu_pct']:5.1f} %\n"
                f"Memory     : {snap['mem_pct']:5.1f} %  "
                f"({snap['mem_used_gb']} / {snap['mem_total_gb']} GB)\n"
                f"Holograms  : {snap['holograms']}"
            )
            self.ui.panel(body, title="TELEMETRY DASHBOARD", style=self.ui.CYAN if self.ui else None)
        return snap

    def refresh(self):
        """Daemon tick - silently refresh snapshot (no print to avoid spam)."""
        self._snapshot()

    def add_hologram(self, n: int = 1):
        self.holograms += n

    def execute(self, task: str, context=None):
        if task in ("show", "materialise", "status"):
            return self.materialise()
        return {"module": "telemetry_dashboard", "task": task, "status": "unknown"}
