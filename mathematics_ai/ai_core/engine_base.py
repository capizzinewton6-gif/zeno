"""Base class and shared utilities for the Gemini engine adapters.

The engines are thin adapters around the Google ``google-genai`` SDK. They
implement a single ``complete`` method returning an :class:`EngineResponse`.
When no API key is configured the engine transparently falls back to a
deterministic local reasoning path so that the rest of the system keeps working
in offline or unprovisioned environments.

Mathematics AI uses Google Gemini models exclusively. No OpenAI, Claude,
DeepSeek, Grok, Mistral or Llama models are used.
"""

from __future__ import annotations

import json
import re
import textwrap
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mathematics_ai.config import get_config

PROMPT_PATH = Path(__file__).resolve().parent / "prompt.txt"


def _load_system_prompt() -> str:
    try:
        return PROMPT_PATH.read_text(encoding="utf-8")
    except OSError:
        return "You are Mathematics AI, a rigorous mathematical research assistant."


@dataclass
class EngineResponse:
    """Structured response returned by every engine."""

    text: str
    engine: str
    model: str
    used_fallback: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return self.text


@dataclass
class EngineConfig:
    model: str
    temperature: float = 0.2
    max_output_tokens: int = 8192
    role: str = "advanced_reasoning"


class GeminiEngineBase:
    """Common implementation for the Gemini model adapters."""

    model_name: str = "gemini"
    role: str = "advanced_reasoning"

    def __init__(self, engine_config: EngineConfig | None = None) -> None:
        self.config = get_config()
        self.engine_config = engine_config or EngineConfig(model=self.model_name, role=self.role)
        self.system_prompt = _load_system_prompt()
        self._client = None
        self._init_client()

    def _init_client(self) -> None:
        """Initialise the ``google-genai`` client when an API key exists."""
        api_key = self.config.gemini_api_key
        if not api_key or self.config.offline_mode:
            return
        try:
            from google import genai  # type: ignore
            self._client = genai.Client(api_key=api_key)
        except Exception:
            self._client = None

    @property
    def available(self) -> bool:
        return self._client is not None

    # --- public API ---------------------------------------------------
    def complete(self, prompt: str, **kwargs: Any) -> EngineResponse:
        """Return a completion for ``prompt``.

        Uses the real Gemini API when available; otherwise delegates to the
        deterministic local fallback.
        """
        if self.available:
            try:
                return self._call_gemini(prompt, **kwargs)
            except Exception as exc:
                if self.config.fallback_to_local_reasoning:
                    return self._fallback(prompt, error=str(exc))
                raise
        return self._fallback(prompt)

    def _call_gemini(self, prompt: str, **kwargs: Any) -> EngineResponse:
        from google import genai  # type: ignore
        cfg = {
            "temperature": kwargs.get("temperature", self.engine_config.temperature),
            "max_output_tokens": kwargs.get("max_output_tokens", self.engine_config.max_output_tokens),
        }
        response = self._client.models.generate_content(
            model=self.engine_config.model,
            contents=prompt,
            config=cfg,
        )
        text = getattr(response, "text", "") or ""
        return EngineResponse(
            text=text,
            engine=self.__class__.__name__,
            model=self.engine_config.model,
            used_fallback=False,
            metadata={"finish_reason": getattr(response, "candidates", None)},
        )

    # --- deterministic local fallback --------------------------------
    def _fallback(self, prompt: str, error: str | None = None) -> EngineResponse:
        """Produce a structured, deterministic local response.

        This is intentionally conservative: it does not attempt to invent
        mathematical facts. It recognises a small set of structured requests
        (JSON action plans) and otherwise returns the system prompt guidance so
        that orchestration agents can still drive the computational modules.
        """
        text = self._local_reason(prompt)
        meta = {"fallback": True}
        if error:
            meta["upstream_error"] = error
        return EngineResponse(
            text=text,
            engine=self.__class__.__name__,
            model=self.engine_config.model + " (local-fallback)",
            used_fallback=True,
            metadata=meta,
        )

    def _local_reason(self, prompt: str) -> str:
        """Best-effort deterministic response generator.

        Recognises JSON-encoded action requests used by the agent layer and
        returns a minimal but well-formed acknowledgement. For free-form
        prompts it echoes the core guidance so downstream modules (SymPy etc.)
        remain the source of mathematical truth.
        """
        stripped = prompt.strip()
        # Detect an embedded JSON action plan.
        m = re.search(r"\{.*\}", stripped, re.DOTALL)
        if m:
            try:
                plan = json.loads(m.group(0))
                return json.dumps({
                    "status": "ok",
                    "acknowledged": True,
                    "plan": plan,
                    "note": "local-fallback acknowledges plan; computational modules own the math.",
                }, indent=2)
            except json.JSONDecodeError:
                pass
        guidance = textwrap.dedent(f"""\
            [local-fallback] No Gemini API key configured or upstream unavailable.
            Delegate concrete computation to the capability modules (SymPy/NumPy/mpmath).
            Prompt summary: {stripped[:500]}""")
        return guidance
