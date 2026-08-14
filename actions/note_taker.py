"""
actions - note_taker
=====================
Auto meeting notes.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, Optional

from core.capability import Capability


class NoteTaker(Capability):
    """Auto meeting notes."""

    STORE = Path(__file__).resolve().parent.parent / "memory" / "notes.json"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "note_taker"
        self.description = "Auto meeting notes."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        low = task.lower()
        if low.startswith(("list note", "show note", "notes")):
            return self._list()
        text = self._extract_text(task)
        if not text:
            return self.error("No note content found in task.")
        note = {"text": text, "created_at": time.strftime("%Y-%m-%d %H:%M:%S")}
        self._append(note)
        return self.ok(f"Note saved: {text[:80]}")

    def _extract_text(self, task: str) -> str:
        task = task.strip()
        for prefix in ("take note:", "note:", "note that", "take note", "remember that"):
            if task.lower().startswith(prefix):
                return task[len(prefix):].strip().strip("\"\'")
        return task.strip().strip("\"\'")

    def _append(self, note):
        self.STORE.parent.mkdir(parents=True, exist_ok=True)
        data = []
        if self.STORE.exists():
            try:
                data = json.loads(self.STORE.read_text())
            except Exception:
                data = []
        data.append(note)
        self.STORE.write_text(json.dumps(data, indent=2))

    def _list(self) -> Any:
        if not self.STORE.exists():
            return self.ok("No notes saved.")
        try:
            data = json.loads(self.STORE.read_text())
        except Exception:
            data = []
        if not data:
            return self.ok("No notes saved.")
        lines = [f"[{r['created_at']}] {r['text']}" for r in data]
        return self.ok("\n".join(lines), count=len(data))

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
