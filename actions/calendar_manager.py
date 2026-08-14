"""
actions - calendar_manager
===========================
Google and Outlook calendar.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, Optional

from core.capability import Capability


class CalendarManager(Capability):
    """Google and Outlook calendar (local-store backed)."""

    STORE = Path(__file__).resolve().parent.parent / "memory" / "calendar.json"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "calendar_manager"
        self.description = "Google and Outlook calendar."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        low = task.lower()
        if low.startswith(("list event", "show event", "calendar", "schedule list")):
            return self._list()
        text = self._extract_text(task)
        if not text:
            return self.error("No event title found in task.")
        event = {"title": text, "when": self._extract_when(task), "created_at": time.strftime("%Y-%m-%d %H:%M:%S")}
        self._append(event)
        return self.ok(f"Event scheduled: {text}" + (f" on {event['when']}" if event['when'] else ""))

    def _extract_text(self, task: str) -> str:
        task = task.strip()
        for prefix in ("schedule", "calendar", "add event", "event"):
            if task.lower().startswith(prefix):
                task = task[len(prefix):].strip()
        import re
        task = re.split(r"\s+(?:on|at|in)\s+", task, maxsplit=1)[0]
        return task.strip().strip("\"\'")

    @staticmethod
    def _extract_when(task: str):
        import re
        m = re.search(r"\bon\s+(\d{4}-\d{2}-\d{2}(?:\s+\d{1,2}:\d{2})?)", task, re.I)
        if m:
            return m.group(1)
        m = re.search(r"\bat\s+(\d{1,2}[:.]?\d{0,2}\s*(?:am|pm)?)", task, re.I)
        if m:
            return m.group(1)
        return None

    def _append(self, event):
        self.STORE.parent.mkdir(parents=True, exist_ok=True)
        data = []
        if self.STORE.exists():
            try:
                data = json.loads(self.STORE.read_text())
            except Exception:
                data = []
        data.append(event)
        self.STORE.write_text(json.dumps(data, indent=2))

    def _list(self) -> Any:
        if not self.STORE.exists():
            return self.ok("No events scheduled.")
        try:
            data = json.loads(self.STORE.read_text())
        except Exception:
            data = []
        if not data:
            return self.ok("No events scheduled.")
        lines = [f"- {r['title']}" + (f" | {r['when']}" if r.get('when') else "") for r in data]
        return self.ok("\n".join(lines), count=len(data))

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
