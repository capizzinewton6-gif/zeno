"""Understand running applications."""

from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

from ai_core.ai_engine import get_engine
from recognition.window_detector import WindowDetector

logger = logging.getLogger(__name__)

_BASE_DIR = Path(__file__).resolve().parent.parent
_APP_MEMORY = _BASE_DIR / "memory" / "application_memory.json"
_APP_DB = _BASE_DIR / "database" / "applications.db"


class ApplicationAnalyzer:
    """Identifies and learns about running applications."""

    def __init__(self, engine=None) -> None:
        self.engine = engine or get_engine()
        self.windows = WindowDetector()
        self._memory = self._load_memory()

    def analyze(self, image: Any = None) -> Dict[str, Any]:
        windows = self.windows.list_windows()
        active = self.windows.active_window()
        name = (active or {}).get("title", "unknown")
        info: Dict[str, Any] = {
            "active": active,
            "windows": windows,
            "count": len(windows),
        }
        if image is not None:
            info["description"] = self.engine.analyze_fast(
                "What application is shown on this screen? Describe its purpose and the "
                "current view in 1-2 sentences.",
                image,
            )
        self._remember_app(name, info)
        return info

    def identify(self, image: Any) -> str:
        return self.engine.analyze_fast(
            "Name the application shown on this screen. Respond with only the application name.",
            image,
        )

    def learn_app(self, name: str, features: Dict[str, Any]) -> None:
        entry = self._memory.setdefault("applications", {}).setdefault(name, {})
        entry["features"] = features
        entry["last_seen"] = __import__("time").strftime("%Y-%m-%dT%H:%M:%S")
        self._save_memory()

    def get_known_app(self, name: str) -> Dict[str, Any] | None:
        return self._memory.get("applications", {}).get(name)

    # ------------------------------------------------------------------ storage
    def _remember_app(self, name: str, info: Dict[str, Any]) -> None:
        try:
            conn = sqlite3.connect(str(_APP_DB))
            ts = __import__("time").strftime("%Y-%m-%dT%H:%M:%S")
            conn.execute(
                "INSERT INTO applications (name, window_title, process_name, os, first_seen, last_seen, metadata) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, name, name, __import__("platform").system(), ts, ts, json.dumps(info, default=str)[:1000]),
            )
            conn.commit()
            conn.close()
        except Exception as exc:
            logger.debug("Failed to record application: %s", exc)

    def _load_memory(self) -> Dict[str, Any]:
        try:
            if _APP_MEMORY.exists():
                with open(_APP_MEMORY, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as exc:
            logger.warning("Failed to load application memory: %s", exc)
        return {"version": 1, "applications": {}}

    def _save_memory(self) -> None:
        try:
            _APP_MEMORY.parent.mkdir(parents=True, exist_ok=True)
            with open(_APP_MEMORY, "w", encoding="utf-8") as f:
                json.dump(self._memory, f, indent=2)
        except Exception as exc:
            logger.warning("Failed to save application memory: %s", exc)
