"""Configuration and path resolution helpers."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT_DIR / "config"
MEMORY_DIR = ROOT_DIR / "memory"
DATABASE_DIR = ROOT_DIR / "database"


def load_json(path: Path | str) -> dict[str, Any]:
    """Load a JSON file, returning an empty dict if missing or invalid."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_json(path: Path | str, data: dict[str, Any]) -> None:
    """Persist a JSON file with indentation."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_settings() -> dict[str, Any]:
    return load_json(CONFIG_DIR / "settings.json")


def get_api_keys() -> dict[str, Any]:
    return load_json(CONFIG_DIR / "api_keys.json")


def get_paths() -> dict[str, Any]:
    return load_json(CONFIG_DIR / "paths.json")


def tool_path(name: str) -> str | None:
    """Resolve a configured system tool path, falling back to PATH lookup."""
    paths = get_paths()
    configured = paths.get(name)
    if configured:
        return configured
    from shutil import which

    return which(name)


def memory_file(name: str) -> Path:
    return MEMORY_DIR / name


def database_file(name: str) -> Path:
    return DATABASE_DIR / name


def env_or_key(key_name: str, env_var: str | None = None) -> str:
    """Return an API key from the environment or the api_keys config."""
    if env_var and os.environ.get(env_var):
        return os.environ[env_var]
    return str(get_api_keys().get(key_name, "")) or ""
