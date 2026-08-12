"""Shared configuration loader and helpers for AI Biology AI."""
from __future__ import annotations

import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _load_json(path: Path, default):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def load_settings():
    return _load_json(PROJECT_ROOT / "config" / "settings.json", {})


def load_api_keys():
    return _load_json(PROJECT_ROOT / "config" / "api_keys.json", {})


def load_paths():
    return _load_json(PROJECT_ROOT / "config" / "paths.json", {})


def get_api_key(name: str) -> str:
    """Return an API key from env (preferred) or the configured keys file."""
    env_name = name.upper()
    val = os.environ.get(env_name, "")
    if val:
        return val
    return load_api_keys().get(name, "")


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
