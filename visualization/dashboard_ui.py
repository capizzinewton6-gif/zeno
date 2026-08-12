"""Dashboard UI: real-time multi-camera grid and performance telemetry.

Note: the interactive text-GUI lives in ``ui.py``. This module provides the
data model and a text renderer for multi-camera telemetry.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CameraTelemetry:
    name: str
    fps: float = 0.0
    latency_ms: float = 0.0
    detections: int = 0
    alerts: int = 0
    status: str = "ok"  # ok | degraded | error


class DashboardUI:
    """Aggregate telemetry from multiple cameras and render a text dashboard."""

    def __init__(self) -> None:
        self.cameras: Dict[str, CameraTelemetry] = {}

    def update(self, telemetry: CameraTelemetry) -> None:
        self.cameras[telemetry.name] = telemetry

    def render_text(self) -> str:
        header = f"{'Camera':<16}{'FPS':>6}{'Lat(ms)':>9}{'Dets':>6}{'Alerts':>8}  Status"
        lines = [header, "-" * len(header)]
        for t in self.cameras.values():
            lines.append(f"{t.name:<16}{t.fps:>6.1f}{t.latency_ms:>9.1f}"
                         f"{t.detections:>6d}{t.alerts:>8d}  {t.status}")
        return "\n".join(lines)

    @property
    def total_detections(self) -> int:
        return sum(t.detections for t in self.cameras.values())

    @property
    def total_alerts(self) -> int:
        return sum(t.alerts for t in self.cameras.values())
