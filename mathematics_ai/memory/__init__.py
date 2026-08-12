"""Persistent JSON-backed memory stores.

These stores persist research notes, conjectures, proven theorems, definitions
and user preferences. Each store wraps a small JSON file so that agents can
append structured records without re-implementing file IO.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

from mathematics_ai.config import MEMORY_DIR


def _uuid() -> str:
    return f"{int(time.time() * 1000)}-{os.urandom(4).hex()}"


class JsonStore:
    """Generic append/query store over a JSON file holding a list/dict."""

    def __init__(self, name: str, default: Any) -> None:
        self.path = MEMORY_DIR / name
        self._default = default
        self._data: Any = self._load()

    def _load(self) -> Any:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return json.loads(json.dumps(self._default))

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")

    def reload(self) -> None:
        self._data = self._load()

    @property
    def data(self) -> Any:
        return self._data


class ListStore(JsonStore):
    """A store whose top-level value is a JSON list under a named key."""

    def __init__(self, name: str, key: str) -> None:
        super().__init__(name, {key: []})
        self.key = key

    @property
    def items(self) -> list[dict[str, Any]]:
        return self._data.setdefault(self.key, [])

    def add(self, record: dict[str, Any]) -> dict[str, Any]:
        record = {"id": _uuid(), "created_at": time.time(), **record}
        self.items.append(record)
        self._save()
        return record

    def all(self) -> list[dict[str, Any]]:
        return list(self.items)

    def find(self, **filters: Any) -> list[dict[str, Any]]:
        out = []
        for item in self.items:
            if all(item.get(k) == v for k, v in filters.items()):
                out.append(item)
        return out


class DictStore(JsonStore):
    """A store whose top-level value is a JSON object (dict)."""

    def __init__(self, name: str) -> None:
        super().__init__(name, {})

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._save()

    def all(self) -> dict[str, Any]:
        return dict(self._data)


# --- concrete stores -------------------------------------------------
research_notes = ListStore("research_notes.json", "projects")
conjectures = ListStore("conjectures.json", "conjectures")
proven_theorems = ListStore("proven_theorems.json", "theorems")
definitions = DictStore("definitions.json")
preferences = DictStore("preferences.json")
