"""
ai_models - llm_gemini
=======================
Google Gemini model wrapper.

Bridges the architecture's designated reasoning engine (Gemini 2.5 Flash) and
processing engine (Gemini 1.5 Flash) onto the shared :mod:`core.llm` client.
Falls back to a deterministic local responder when no API key is configured.
"""

import os
from typing import Any, Dict, Optional

from core.llm import LLMClient, REASONING_MODEL


class LlmGemini:
    """Google Gemini model wrapper (reasoning + processing engines)."""

    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
        self.config = config or {}
        self.client = LLMClient(api_key=self.api_key)
        self.model = REASONING_MODEL
        self.available = self.client.is_available()

    def execute(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Run a prompt through the reasoning engine."""
        return self.reason(prompt, context)

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Gemini 2.5 Flash - planning, analysis, decisions."""
        return self.client.reason(prompt, context)

    def process(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Gemini 1.5 Flash - extraction, summarisation, fast lookup."""
        return self.client.process(prompt, context)

    def summarize(self, text: str) -> str:
        return self.client.summarize(text)

    def is_available(self) -> bool:
        return self.available
