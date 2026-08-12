"""Main AI intelligence engine, powered exclusively by Google Gemini models."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "model_config.json"
_PROMPT_PATH = Path(__file__).resolve().parent / "prompt.txt"


class AIEngine:
    """Central Gemini-backed intelligence engine.

    Provides reasoning (Gemini 2.5 Flash) and fast analysis (Gemini 1.5 Flash).
    Falls back to a deterministic offline mode when the Gemini SDK or an API key
    is unavailable, so the rest of the system can still be imported and exercised.
    """

    def __init__(self, config_path: Optional[str] = None, api_key: Optional[str] = None) -> None:
        self.config_path = Path(config_path) if config_path else _CONFIG_PATH
        self.config = self._load_config()
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        self._client = None
        self._reasoning_model = self.config["reasoning_model"]["name"]
        self._fast_model = self.config["fast_model"]["name"]
        self._system_prompt = self._load_prompt()
        self._connect()

    # ------------------------------------------------------------------ config
    def _load_config(self) -> Dict[str, Any]:
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        logger.warning("Model config not found at %s; using defaults", self.config_path)
        return {
            "reasoning_model": {"name": "gemini-2.5-flash"},
            "fast_model": {"name": "gemini-1.5-flash"},
        }

    def _load_prompt(self) -> str:
        if _PROMPT_PATH.exists():
            with open(_PROMPT_PATH, "r", encoding="utf-8") as f:
                return f.read()
        return "You are Screen Recognition AI."

    # ------------------------------------------------------------------ connect
    def _connect(self) -> None:
        try:
            import google.generativeai as genai  # type: ignore

            if self.api_key:
                genai.configure(api_key=self.api_key)
                self._client = genai
                logger.info("Gemini SDK configured (reasoning=%s, fast=%s)",
                            self._reasoning_model, self._fast_model)
            else:
                logger.warning("No GEMINI_API_KEY set; running in offline stub mode.")
        except Exception as exc:  # pragma: no cover - environment dependent
            logger.warning("Gemini SDK unavailable (%s); running in offline stub mode.", exc)

    @property
    def is_online(self) -> bool:
        return self._client is not None and bool(self.api_key)

    # ------------------------------------------------------------------ generate
    def _generate(self, model_name: str, prompt: str, image: Any = None,
                  temperature: float = 0.4, max_tokens: int = 2048) -> str:
        if not self.is_online:
            return self._stub_response(model_name, prompt, image)
        try:
            model = self._client.GenerativeModel(
                model_name,
                system_instruction=self._system_prompt,
            )
            contents = [prompt] if image is None else [prompt, image]
            response = model.generate_content(
                contents,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                },
            )
            return getattr(response, "text", "") or ""
        except Exception as exc:  # pragma: no cover - network dependent
            logger.error("Gemini generation failed: %s", exc)
            return self._stub_response(model_name, prompt, image)

    def _stub_response(self, model_name: str, prompt: str, image: Any) -> str:
        has_img = "with image" if image is not None else "text only"
        return json.dumps({
            "offline": True,
            "model": model_name,
            "mode": has_img,
            "prompt_preview": prompt[:120],
            "note": "Gemini API not configured. Set GEMINI_API_KEY to enable live AI.",
        })

    # ------------------------------------------------------------------ public API
    def reason(self, prompt: str, image: Any = None, temperature: float = 0.4,
               max_tokens: int = 8192) -> str:
        """Deep reasoning via Gemini 2.5 Flash."""
        return self._generate(self._reasoning_model, prompt, image, temperature, max_tokens)

    def analyze_fast(self, prompt: str, image: Any = None, temperature: float = 0.2,
                     max_tokens: int = 4096) -> str:
        """Fast analysis via Gemini 1.5 Flash."""
        return self._generate(self._fast_model, prompt, image, temperature, max_tokens)

    def describe_screen(self, image: Any) -> str:
        """High-level description of a screen image."""
        return self.reason("Describe what is displayed on this screen in detail.", image)

    def get_system_prompt(self) -> str:
        return self._system_prompt


# Singleton-style accessor ----------------------------------------------------
_default_engine: Optional[AIEngine] = None


def get_engine() -> AIEngine:
    global _default_engine
    if _default_engine is None:
        _default_engine = AIEngine()
    return _default_engine
