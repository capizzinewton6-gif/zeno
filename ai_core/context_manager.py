"""Maintain screen context across recognition cycles."""

from __future__ import annotations

import json
import logging
import time
from collections import deque
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_MAX_CONTEXT = 100


class ContextManager:
    """Tracks the evolving state of the screen across time."""

    def __init__(self, max_history: int = _MAX_CONTEXT) -> None:
        self.max_history = max_history
        self._history: deque = deque(maxlen=max_history)
        self._current: Dict[str, Any] = {}
        self._session_start = time.time()

    # ------------------------------------------------------------------ update
    def update(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context = dict(context)
        context.setdefault("timestamp", time.time())
        self._history.append(context)
        self._current = context
        return context

    def set(self, key: str, value: Any) -> None:
        self._current[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._current.get(key, default)

    # ------------------------------------------------------------------ query
    @property
    def current(self) -> Dict[str, Any]:
        return dict(self._current)

    @property
    def previous(self) -> Optional[Dict[str, Any]]:
        if len(self._history) < 2:
            return None
        return dict(self._history[-2])

    @property
    def history(self) -> list:
        return list(self._history)

    def what_changed(self) -> Dict[str, Any]:
        """Diff current vs previous context (top-level keys)."""
        prev = self.previous or {}
        changes = {}
        for key in set(list(prev) + list(self._current)):
            if prev.get(key) != self._current.get(key):
                changes[key] = {"from": prev.get(key), "to": self._current.get(key)}
        return changes

    def clear(self) -> None:
        self._history.clear()
        self._current = {}

    def summary(self) -> str:
        return json.dumps(self._current, default=str)[:1000]
