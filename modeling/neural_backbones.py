"""Neural backbone router for the Gemini model family.

Routes requests to either the *reasoning* model (Gemini 2.5 Flash) or the
*fast* model (Gemini 1.5 Flash) based on the task profile. When the
``google-genai`` SDK is installed and an API key is available, requests are
served live. Otherwise a deterministic offline stub is used so the rest of the
agent stack remains functional during development.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any, Literal

from config import env_or_key, get_settings

# Model identifiers -----------------------------------------------------------
REASONING_MODEL = "gemini-2.5-flash"
FAST_MODEL = "gemini-1.5-flash"

Role = Literal["reasoning", "fast"]

try:  # pragma: no cover - import gated on SDK presence
    from google import genai  # type: ignore
    from google.genai import types  # type: ignore

    _GENAI_AVAILABLE = True
except Exception:  # pragma: no cover
    genai = None  # type: ignore
    types = None  # type: ignore
    _GENAI_AVAILABLE = False


@dataclass
class GenerationParameters:
    """Generation parameters forwarded to the model."""

    temperature: float = 0.2
    top_p: float = 0.95
    max_tokens: int = 8192
    timeout: float = 120.0

    @classmethod
    def from_settings(cls) -> "GenerationParameters":
        cfg = get_settings().get("generation", {})
        return cls(
            temperature=cfg.get("temperature", 0.2),
            top_p=cfg.get("top_p", 0.95),
            max_tokens=cfg.get("max_tokens", 8192),
            timeout=cfg.get("timeout_seconds", 120),
        )

    def to_config(self) -> dict[str, Any]:
        return {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_output_tokens": self.max_tokens,
        }


@dataclass
class ModelResponse:
    """Normalized response envelope for a single model call."""

    text: str
    model: str
    role: Role
    usage: dict[str, int] = field(default_factory=lambda: {"input": 0, "output": 0})
    latency_ms: float = 0.0
    offline: bool = False

    @property
    def ok(self) -> bool:
        return bool(self.text)


def _resolve_role(role: Role, task: str | None) -> Role:
    """Pick the model role, heuristically upgrading to reasoning for hard tasks."""
    if task and role == "fast":
        hard_markers = (
            "architect", "design", "reason", "plan", "refactor",
            "debug", "complex", "analyze", "optimi",
        )
        if any(m in task.lower() for m in hard_markers):
            return "reasoning"
    return role


class NeuralBackbone:
    """Single entry point for LLM access across all capabilities."""

    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or env_or_key("gemini_api_key", "GEMINI_API_KEY")
        self._client = None
        if _GENAI_AVAILABLE and self._api_key:
            try:  # pragma: no cover - network path
                self._client = genai.Client(api_key=self._api_key)
            except Exception:
                self._client = None

    @property
    def available(self) -> bool:
        return self._client is not None

    # -- public API ----------------------------------------------------------
    def reason(self, prompt: str, *, system: str | None = None,
               params: GenerationParameters | None = None) -> ModelResponse:
        """Send a request to the reasoning model (Gemini 2.5 Flash)."""
        return self.generate(prompt, role="reasoning", system=system, params=params)

    def fast(self, prompt: str, *, system: str | None = None,
             params: GenerationParameters | None = None) -> ModelResponse:
        """Send a request to the fast model (Gemini 1.5 Flash)."""
        return self.generate(prompt, role="fast", system=system, params=params)

    def generate(self, prompt: str, *, role: Role = "fast", system: str | None = None,
                 task: str | None = None, params: GenerationParameters | None = None) -> ModelResponse:
        """Generate a completion, routing to the appropriate model."""
        params = params or GenerationParameters.from_settings()
        role = _resolve_role(role, task)
        model = REASONING_MODEL if role == "reasoning" else FAST_MODEL
        start = time.perf_counter()

        if self.available:  # pragma: no cover - live network path
            try:
                cfg = self._build_config(params, system)
                resp = self._client.models.generate_content(
                    model=model, contents=prompt, config=cfg,
                )
                text = getattr(resp, "text", "") or ""
                usage = self._extract_usage(resp)
                return ModelResponse(
                    text=text, model=model, role=role, usage=usage,
                    latency_ms=(time.perf_counter() - start) * 1000,
                )
            except Exception as exc:  # fall back to offline
                return self._offline(prompt, model, role, start, error=str(exc))

        return self._offline(prompt, model, role, start)

    # -- internals -----------------------------------------------------------
    def _build_config(self, params: GenerationParameters, system: str | None):  # pragma: no cover
        cfg_args = {"temperature": params.temperature, "top_p": params.top_p,
                    "max_output_tokens": params.max_tokens}
        if system:
            cfg_args["system_instruction"] = system
        return types.GenerateContentConfig(**cfg_args) if types else None

    def _extract_usage(self, resp) -> dict[str, int]:  # pragma: no cover
        usage = getattr(resp, "usage_metadata", None)
        if not usage:
            return {"input": 0, "output": 0}
        return {
            "input": getattr(usage, "prompt_token_count", 0) or 0,
            "output": getattr(usage, "candidates_token_count", 0) or 0,
        }

    def _offline(self, prompt: str, model: str, role: Role, start: float,
                 error: str | None = None) -> ModelResponse:
        """Deterministic offline stub used when no SDK/key is configured.

        Returns a clearly-marked placeholder so callers can detect the absence
        of a live model and degrade gracefully.
        """
        note = error or "no API key / SDK configured"
        text = (
            "[offline-stub] The Gemini backbone is not configured live "
            f"(reason: {note}). Echoing the request for wiring/debugging:\n\n"
            f">>> {prompt[:500]}{'...' if len(prompt) > 500 else ''}"
        )
        return ModelResponse(
            text=text, model=model, role=role, offline=True,
            latency_ms=(time.perf_counter() - start) * 1000,
        )


# Module-level singleton for convenient sharing across capabilities ----------
_backbone: NeuralBackbone | None = None


def get_backbone() -> NeuralBackbone:
    global _backbone
    if _backbone is None:
        _backbone = NeuralBackbone()
    return _backbone


def reset_backbone() -> None:
    """Reset the shared backbone (useful for tests / config reloads)."""
    global _backbone
    _backbone = None
