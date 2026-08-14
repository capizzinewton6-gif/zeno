"""
core.llm - unified LLM client for the assistant.

The architecture spec designates Gemini 2.5 Flash as the reasoning engine and
Gemini 1.5 Flash as the fast processing engine. This module provides a single
:class:`LLMClient` that:

* uses Google's ``google-generativeai`` SDK when ``GEMINI_API_KEY`` /
  ``GOOGLE_API_KEY`` is available (and the package is installed);
* otherwise falls back to a deterministic local responder so the assistant
  remains fully functional offline / without credentials.

The local responder is intentionally rule-based: it plans simple objectives
and routes common requests to the right capability keywords. It is NOT a
substitute for a real LLM but keeps the system runnable end-to-end.
"""

from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Optional

# Model names per the architecture spec.
REASONING_MODEL = "gemini-2.5-flash"
PROCESSING_MODEL = "gemini-1.5-flash"


class LLMClient:
    """Thin wrapper around the Gemini SDK with an offline fallback."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or ""
        )
        self._genai = None
        self._reasoning_model = None
        self._processing_model = None
        self.available = bool(self.api_key)
        if self.available:
            self._init_genai()

    def _init_genai(self) -> None:
        try:
            import google.generativeai as genai  # type: ignore

            genai.configure(api_key=self.api_key)
            self._genai = genai
            self._reasoning_model = genai.GenerativeModel(REASONING_MODEL)
            self._processing_model = genai.GenerativeModel(PROCESSING_MODEL)
        except Exception:
            # SDK not installed or configuration failed -> use fallback.
            self._genai = None
            self._reasoning_model = None
            self._processing_model = None
            self.available = False

    # -- public API --------------------------------------------------------

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Use the reasoning engine (Gemini 2.5 Flash) for planning/decisions."""
        if self._reasoning_model is not None:
            try:
                resp = self._reasoning_model.generate_content(prompt)
                return self._extract_text(resp)
            except Exception as exc:  # pragma: no cover - network/runtime errors
                return f"[llm:reasoning error: {exc}]\n" + _local_reason(prompt)
        return _local_reason(prompt)

    def process(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Use the processing engine (Gemini 1.5 Flash) for fast extraction."""
        if self._processing_model is not None:
            try:
                resp = self._processing_model.generate_content(prompt)
                return self._extract_text(resp)
            except Exception as exc:  # pragma: no cover
                return f"[llm:processing error: {exc}]\n" + _local_process(prompt)
        return _local_process(prompt)

    def summarize(self, text: str) -> str:
        if not text:
            return ""
        if self._processing_model is not None:
            try:
                resp = self._processing_model.generate_content(
                    f"Summarize the following concisely:\n\n{text}"
                )
                return self._extract_text(resp)
            except Exception:  # pragma: no cover
                pass
        return _local_summarize(text)

    def is_available(self) -> bool:
        return self.available

    # -- internal ----------------------------------------------------------

    @staticmethod
    def _extract_text(resp: Any) -> str:
        # google-generativeai response objects expose .text in recent versions.
        try:
            return resp.text
        except Exception:
            try:
                return resp.candidates[0].content.parts[0].text
            except Exception:
                return str(resp)


# --------------------------------------------------------------------------- #
# Offline deterministic fallback
# --------------------------------------------------------------------------- #

_CAPABILITY_HINTS: List[tuple] = [
    (["search", "google", "look up", "find online", "find info"], "web_search"),
    (["open url", "open website", "open link", "go to http", "navigate to"], "url_launcher"),
    (["open ", "launch ", "start app", "open app"], "app_manager"),
    (["create file", "write file", "make file"], "file_controller"),
    (["move file", "copy file", "delete file", "rename file"], "file_controller"),
    (["list file", "list dir", "show files", "find file"], "file_controller"),
    (["run command", "terminal", "shell", "bash", "run "], "terminal_manager"),
    (["system status", "cpu", "ram", "memory", "monitor system"], "system_monitor"),
    (["disk", "storage", "free space"], "system_monitor"),
    (["screenshot", "capture screen"], "screenshot"),
    (["play music"], "music_player"),
    (["schedule", "calendar", "meeting"], "calendar_manager"),
    (["send email", "email", "gmail"], "gmail_sender"),
    (["remind me", "reminder", "set reminder"], "reminder"),
    (["weather", "forecast"], "weather_report"),
    (["translate", "translation"], "translation_service"),
    (["qr code", "generate qr"], "qr_generator"),
    (["ip address", "my ip", "public ip"], "ip_checker"),
    (["note", "take note"], "note_taker"),
    (["calc", "calculate", "math", "what is", "what's"], "calculator"),
]


def _match_capability(text: str) -> Optional[str]:
    low = text.lower()
    for keywords, cap in _CAPABILITY_HINTS:
        if any(kw in low for kw in keywords):
            return cap
    return None


def _local_reason(prompt: str) -> str:
    """Deterministic planner used when no LLM key is configured.

    Produces a JSON array of steps so the orchestrator can parse them. When the
    prompt looks like a direct capability request, it returns a single step.
    """
    stripped = prompt.strip()
    # If the prompt already looks like a JSON plan request from the orchestrator,
    # parse out the objective and emit a simple plan.
    obj_match = re.search(r"Objective:\s*(.+?)(?:\n|Context:|$)", stripped, re.S)
    objective = obj_match.group(1).strip() if obj_match else stripped
    cap = _match_capability(objective)
    if cap:
        steps = [{"step": objective, "capability": cap, "args": objective}]
    else:
        steps = [{"step": objective, "capability": None, "args": None}]
    return json.dumps(steps)


def _local_process(prompt: str) -> str:
    return prompt


def _local_summarize(text: str) -> str:
    if "\n" in text or " | " in text:
        # Join pipe-separated results into a compact summary.
        parts = [p.strip() for p in text.split(" | ") if p.strip()]
        if len(parts) > 1:
            return f"Completed {len(parts)} steps: " + "; ".join(parts)
    if len(text) > 280:
        return text[:277] + "..."
    return text
