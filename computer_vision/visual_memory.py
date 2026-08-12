"""Remember previous screens."""

from __future__ import annotations

import json
import logging
import time
from collections import deque
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_MEMORY_DIR = Path(__file__).resolve().parent.parent / "memory"
_HISTORY_FILE = _MEMORY_DIR / "screen_history.json"


class VisualMemory:
    """Stores and recalls previous screen states."""

    def __init__(self, max_entries: int = 1000, history_file: Optional[str] = None) -> None:
        self.max_entries = max_entries
        self.history_file = Path(history_file) if history_file else _HISTORY_FILE
        self._entries: deque = deque(maxlen=max_entries)
        self._load()

    def _load(self) -> None:
        if not self.history_file.exists():
            return
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entry in data.get("history", []):
                self._entries.append(entry)
        except Exception as exc:
            logger.warning("Failed to load visual memory: %s", exc)

    def save(self) -> None:
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump({"version": 1, "history": list(self._entries)}, f, indent=2)
        except Exception as exc:
            logger.warning("Failed to save visual memory: %s", exc)

    def remember(self, state: Dict[str, Any]) -> Dict[str, Any]:
        state = dict(state)
        state.setdefault("timestamp", time.time())
        self._entries.append(state)
        return state

    def recall_last(self) -> Optional[Dict[str, Any]]:
        return dict(self._entries[-1]) if self._entries else None

    def recall_all(self) -> list:
        return list(self._entries)

    def search(self, key: str, value: str) -> list:
        low = str(value).lower()
        return [e for e in self._entries if low in str(e.get(key, "")).lower()]

    def forget(self) -> None:
        self._entries.clear()
        self.save()

    def __len__(self) -> int:
        return len(self._entries)
