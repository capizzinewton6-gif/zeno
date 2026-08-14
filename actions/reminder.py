"""
actions - reminder
===================
Set reminders.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional

from core.capability import Capability


class Reminder(Capability):
    """Set reminders."""

    STORE = Path(__file__).resolve().parent.parent / "memory" / "reminders.json"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "reminder"
        self.description = "Set reminders."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        low = task.lower()
        if low.startswith(("list reminder", "show reminder", "reminders")):
            return self._list()
        text = self._extract_text(task)
        if not text:
            return self.error("No reminder text found in task.")
        reminder = {"text": text, "created_at": time.strftime("%Y-%m-%d %H:%M:%S"), "due": self._extract_due(task)}
        self._append(reminder)
        return self.ok(f"Reminder set: {text}" + (f" (due {reminder['due']})" if reminder['due'] else ""))

    def _extract_text(self, task: str) -> str:
        task = task.strip()
        for prefix in ("remind me to", "remind me", "set reminder:", "reminder:", "remind:"):
            if task.lower().startswith(prefix):
                task = task[len(prefix):].strip()
        # strip "at <time>" / "in <duration>" tail for the text portion
        import re
        task = re.split(r"\s+(?:at|in)\s+", task, maxsplit=1)[0]
        return task.strip().strip("\"\'")

    @staticmethod
    def _extract_due(task: str):
        import re
        m = re.search(r"\bat\s+(\d{1,2}[:.]?\d{0,2}\s*(?:am|pm)?)", task, re.I)
        if m:
            return m.group(1)
        m = re.search(r"\bin\s+(\d+)\s*(minute|hour|day)s?", task, re.I)
        if m:
            return f"in {m.group(1)} {m.group(2)}{'s' if int(m.group(1)) != 1 else ''}"
        return None

    def _append(self, reminder):
        self.STORE.parent.mkdir(parents=True, exist_ok=True)
        data = []
        if self.STORE.exists():
            try:
                data = json.loads(self.STORE.read_text())
            except Exception:
                data = []
        data.append(reminder)
        self.STORE.write_text(json.dumps(data, indent=2))

    def _list(self) -> Any:
        if not self.STORE.exists():
            return self.ok("No reminders set.")
        try:
            data = json.loads(self.STORE.read_text())
        except Exception:
            data = []
        if not data:
            return self.ok("No reminders set.")
        lines = [f"{i+1}. {r['text']}" + (f" (due {r['due']})" if r.get('due') else "") for i, r in enumerate(data)]
        return self.ok("\n".join(lines), count=len(data))

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
