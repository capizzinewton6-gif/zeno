"""Understand user commands and translate them to structured intents."""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, Optional

from ai_core.ai_engine import get_engine

logger = logging.getLogger(__name__)

_INTENT_KEYWORDS = {
    "click": ["click", "press", "tap"],
    "type": ["type", "write", "enter text"],
    "scroll": ["scroll", "swipe"],
    "open": ["open", "launch", "start"],
    "close": ["close", "exit", "quit"],
    "find": ["find", "locate", "search for", "where is"],
    "read": ["read", "what does", "ocr", "what text"],
    "describe": ["describe", "what is on", "what's on", "explain"],
    "automate": ["automate", "repeat", "workflow", "do this every"],
    "screenshot": ["screenshot", "capture", "snapshot"],
    "help": ["help", "what can you do"],
}


class CommandParser:
    """Parses natural-language user commands into structured intents."""

    def __init__(self, engine=None) -> None:
        self.engine = engine or get_engine()

    def parse(self, command: str) -> Dict[str, Any]:
        command = (command or "").strip()
        if not command:
            return {"intent": "empty", "raw": "", "target": None, "params": {}}

        intent = self._detect_intent(command)
        target = self._extract_target(command, intent)
        result = {
            "intent": intent,
            "raw": command,
            "target": target,
            "params": {},
        }
        # Augment with Gemini for ambiguous commands
        if intent in ("unknown", "automate") or target is None:
            refined = self._refine_with_gemini(command)
            if refined:
                result.update(refined)
        return result

    # ------------------------------------------------------------------ heuristic
    def _detect_intent(self, command: str) -> str:
        low = command.lower()
        for intent, keywords in _INTENT_KEYWORDS.items():
            if any(kw in low for kw in keywords):
                return intent
        return "unknown"

    def _extract_target(self, command: str, intent: str) -> Optional[str]:
        low = command.lower()
        for kw in _INTENT_KEYWORDS.get(intent, []):
            idx = low.find(kw)
            if idx != -1:
                remainder = command[idx + len(kw):].strip(" .,:!")
                if remainder:
                    return remainder
        return None

    # ------------------------------------------------------------------ gemini
    def _refine_with_gemini(self, command: str) -> Dict[str, Any]:
        prompt = (
            "Parse this user command for a screen automation assistant. "
            "Return JSON with keys: intent (click/type/scroll/open/close/find/read/describe/"
            "automate/screenshot/help), target, params (dict). "
            f"Command: {command}\nRespond with ONLY JSON."
        )
        try:
            raw = self.engine.analyze_fast(prompt)
            text = raw.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.lower().startswith("json"):
                    text = text[4:]
            data = json.loads(text)
            if isinstance(data, dict):
                return data
        except Exception as exc:
            logger.debug("Gemini command refinement failed: %s", exc)
        return {}
