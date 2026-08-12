"""Alert popups: visual alert notifications for unknown faces / restricted zones."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from tracking_analytics.event_trigger import Alert


@dataclass
class AlertPopup:
    alert: Alert
    shown: bool = False
    acknowledged: bool = False


class AlertPopups:
    """Manage a queue of alert popups with severity-based styling."""

    def __init__(self, max_visible: int = 5) -> None:
        self.max_visible = max_visible
        self._queue: List[AlertPopup] = []

    def push(self, alert: Alert) -> None:
        self._queue.append(AlertPopup(alert=alert, shown=True))
        if len(self._queue) > self.max_visible:
            self._queue.pop(0)

    def acknowledge(self, index: int) -> None:
        if 0 <= index < len(self._queue):
            self._queue[index].acknowledged = True

    def clear_acknowledged(self) -> None:
        self._queue = [p for p in self._queue if not p.acknowledged]

    def render_text(self) -> str:
        if not self._queue:
            return "No active alerts."
        lines = ["=== ALERTS ==="]
        for i, p in enumerate(self._queue):
            a = p.alert
            tag = f"[{a.severity.upper()}]" if a.severity else "[INFO]"
            lines.append(f"{i}: {tag} {a.kind}: {a.message}")
        return "\n".join(lines)

    @property
    def active(self) -> List[Alert]:
        return [p.alert for p in self._queue if not p.acknowledged]
