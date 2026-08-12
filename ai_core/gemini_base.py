"""Shared base for Google Gemini engines with graceful degradation.

The AI Biology AI uses Google Gemini models exclusively (2.5 Flash and
1.5 Flash). When an API key is unavailable or a network error occurs, the
engines fall back to a deterministic local reasoning stub so the rest of the
application remains fully functional for offline / demonstration use.
"""
from __future__ import annotations

from pathlib import Path

from ai_core.config_loader import PROJECT_ROOT


class GeminiEngineBase:
    """Common interface for Gemini-backed reasoning engines."""

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float = 0.4,
        max_output_tokens: int = 8192,
        timeout: int = 60,
        **_ignored,
    ):
        self.api_key = (api_key or "").strip()
        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.timeout = timeout
        self._client = None
        self._available = False
        self._init_client()

    @property
    def role(self) -> str:
        raise NotImplementedError

    @property
    def available(self) -> bool:
        return self._available

    def _init_client(self):
        if not self.api_key:
            self._available = False
            return
        # Prefer the newer google-genai SDK, fall back to google.generativeai.
        try:  # google-genai
            from google import genai

            self._client = genai.Client(api_key=self.api_key)
            self._sdk = "genai"
            self._available = True
            return
        except Exception:
            pass
        try:  # legacy google-generativeai
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            self._client = genai.GenerativeModel(self.model)
            self._sdk = "generativeai"
            self._available = True
        except Exception:
            self._client = None
            self._available = False

    def generate(self, prompt: str, system: str | None = None) -> str:
        """Return the model's text response, or a local fallback answer."""
        if self._available and self._client is not None:
            try:
                return self._call_api(prompt, system)
            except Exception as exc:  # pragma: no cover - network path
                return self._fallback(prompt, system, error=str(exc))
        return self._fallback(prompt, system)

    def _call_api(self, prompt: str, system: str | None = None) -> str:
        if self._sdk == "genai":
            cfg = {
                "temperature": self.temperature,
                "max_output_tokens": self.max_output_tokens,
            }
            if system:
                resp = self._client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=cfg,
                )
            else:
                resp = self._client.models.generate_content(
                    model=self.model, contents=prompt, config=cfg
                )
            return getattr(resp, "text", "") or ""
        # legacy generativeai
        full = f"{system}\n\n{prompt}" if system else prompt
        resp = self._client.generate_content(
            full,
            generation_config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_output_tokens,
            },
        )
        return getattr(resp, "text", "") or ""

    def _fallback(self, prompt: str, system: str | None = None, error: str = "") -> str:
        """Deterministic offline answer used when no Gemini API is reachable."""
        note = ""
        if error:
            note = f" (API error: {error[:120]})"
        return (
            f"[local-fallback{note}] The {self.model} engine is not reachable "
            "because no Google API key is configured or the network is unavailable. "
            "Install a key in config/api_keys.json (field 'google_api_key') or set "
            "the GOOGLE_API_KEY environment variable to enable Gemini-powered reasoning. "
            "All biological capability modules continue to work using their built-in "
            "deterministic algorithms; only LLM-assisted reasoning is unavailable.\n\n"
            f"Prompt received: {prompt[:300]}"
        )


def load_system_prompt() -> str:
    p = PROJECT_ROOT / "ai_core" / "prompt.txt"
    try:
        return p.read_text(encoding="utf-8")
    except OSError:
        return ""
