"""Loader for the VISION_AI system prompt."""

from __future__ import annotations

import os

_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompt.txt")


def load_prompt() -> str:
    """Return the full system prompt text from prompt.txt."""
    try:
        with open(_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return "You are VISION_AI, an autonomous AI Vision & Scene Understanding Assistant."
