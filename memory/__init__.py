"""Memory store: persists projects, inventions, designs, components, preferences."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List

DEFAULT_DIR = os.path.join(os.path.dirname(__file__))


class MemoryStore:
    """Thin JSON-backed key/value store over the memory/*.json files."""

    def __init__(self, memory_dir: str | None = None):
        self.memory_dir = memory_dir or DEFAULT_DIR
        os.makedirs(self.memory_dir, exist_ok=True)
        self._files = {
            "projects": "projects.json",
            "inventions": "inventions.json",
            "designs": "designs.json",
            "components": "components.json",
            "preferences": "preferences.json",
        }
        for name in self._files.values():
            path = os.path.join(self.memory_dir, name)
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    json.dump([], f)

    def _path(self, store: str) -> str:
        return os.path.join(self.memory_dir, self._files[store])

    def _load_raw(self, store: str):
        with open(self._path(store), encoding="utf-8") as f:
            return json.load(f)

    def load(self, store: str) -> list[dict[str, Any]]:
        data = self._load_raw(store)
        return data if isinstance(data, list) else []

    def save(self, store: str, data: list[dict[str, Any]]):
        with open(self._path(store), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def append(self, store: str, item: dict[str, Any]):
        data = self.load(store)
        data.append(item)
        self.save(store, data)

    def get_preference(self, key: str, default: Any = None) -> Any:
        prefs = self._load_raw("preferences")
        if isinstance(prefs, dict):
            return prefs.get(key, default)
        for p in prefs:
            if isinstance(p, dict) and p.get("key") == key:
                return p.get("value")
        return default

    def set_preference(self, key: str, value: Any):
        prefs = self._load_raw("preferences")
        if isinstance(prefs, dict):
            prefs[key] = value
            with open(self._path("preferences"), "w", encoding="utf-8") as f:
                json.dump(prefs, f, indent=2)
            return
        for p in prefs:
            if isinstance(p, dict) and p.get("key") == key:
                p["value"] = value
                self.save("preferences", prefs)
                return
        prefs.append({"key": key, "value": value})
        self.save("preferences", prefs)

    def stores(self) -> list[str]:
        return list(self._files.keys())
