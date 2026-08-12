"""Version manager: tracks design versions."""

from __future__ import annotations

import time
from typing import Any, Dict, List


class VersionManager:
    def __init__(self):
        self.versions: List[Dict[str, Any]] = []

    def commit(self, design_id: str, description: str,
               changes: str = "") -> Dict[str, Any]:
        version = {
            "design_id": design_id,
            "version": f"v{len([v for v in self.versions if v['design_id'] == design_id]) + 1}",
            "description": description, "changes": changes,
            "timestamp": time.time(),
        }
        self.versions.append(version)
        return version

    def history(self, design_id: str) -> List[Dict[str, Any]]:
        return [v for v in self.versions if v["design_id"] == design_id]

    def latest(self, design_id: str) -> Dict[str, Any] | None:
        hist = self.history(design_id)
        return hist[-1] if hist else None

    def rollback(self, design_id: str, version: str) -> Dict[str, Any] | None:
        for v in self.versions:
            if v["design_id"] == design_id and v["version"] == version:
                return v
        return None
