"""Shared configuration and path utilities for Mathematics AI.

Loads JSON config from the packaged ``config`` directory and provides a single
``Config`` object consumed by every module. Keeping configuration access in one
place avoids scattered file IO and makes the system testable.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import mathematics_ai

_PACKAGE_ROOT = Path(mathematics_ai.__file__).resolve().parent
CONFIG_DIR = _PACKAGE_ROOT / "config"
MEMORY_DIR = _PACKAGE_ROOT / "memory"


def _load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


class Config:
    """Typed view over the JSON configuration files."""

    def __init__(self) -> None:
        self.settings: dict[str, Any] = _load_json(CONFIG_DIR / "settings.json", {})
        self.api_keys: dict[str, Any] = _load_json(CONFIG_DIR / "api_keys.json", {})
        self.paths: dict[str, Any] = _load_json(CONFIG_DIR / "paths.json", {})

    # --- convenience accessors -----------------------------------------
    @property
    def default_precision(self) -> int:
        return int(self.settings.get("default_precision", 50))

    @property
    def max_recursion_depth(self) -> int:
        return int(self.settings.get("max_recursion_depth", 20))

    @property
    def max_computation_seconds(self) -> float:
        return float(self.settings.get("max_computation_seconds", 30))

    @property
    def default_engine(self) -> str:
        return self.settings.get("default_engine", "gemini-2.5-flash")

    @property
    def fallback_to_local_reasoning(self) -> bool:
        return bool(self.settings.get("fallback_to_local_reasoning", True))

    @property
    def offline_mode(self) -> bool:
        env_offline = os.environ.get("MATH_AI_OFFLINE", "").lower() in {"1", "true", "yes"}
        return bool(self.settings.get("offline_mode", False)) or env_offline

    @property
    def gemini_api_key(self) -> str:
        env_key = os.environ.get("GEMINI_API_KEY", "")
        return env_key or str(self.api_keys.get("gemini_api_key", ""))

    @property
    def plot_style(self) -> str:
        return self.settings.get("plot_style", "default")


_config: Config | None = None


def get_config() -> Config:
    """Return the process-wide :class:`Config` singleton."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config() -> Config:
    """Force a fresh reload of configuration (mainly for tests)."""
    global _config
    _config = Config()
    return _config
