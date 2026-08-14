"""
integrations - ai_model_router
===============================
Route to Gemini, Claude and GPT.

Central AI routing layer. The architecture is Gemini-first (Gemini 2.5 Flash
for reasoning, Gemini 1.5 Flash for processing). Other providers (Claude, GPT,
Llama) are exposed as optional fallbacks when their wrappers are available.
"""

from typing import Any, Dict, Optional

from ai_models.llm_gemini import LlmGemini
from core.llm import LLMClient


class AiModelRouter:
    """Route prompts to the best available AI model."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "ai_model_router"
        self.description = "Route to Gemini, Claude and GPT."
        # Primary engine (Gemini) with offline fallback baked in.
        self.gemini = LlmGemini()
        self.client: Optional[LLMClient] = self.gemini.client
        self.default_provider = "gemini"

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Capability contract entrypoint - reasons over the task."""
        return self.reason(task)

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Reasoning (planning/decisions) via the configured provider."""
        if self.client is not None:
            return self.client.reason(prompt, context)
        return prompt

    def process(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Fast processing/extraction via the configured provider."""
        if self.client is not None:
            return self.client.process(prompt, context)
        return prompt

    def summarize(self, text: str) -> str:
        if self.client is not None:
            return self.client.summarize(text)
        return text

    def is_available(self) -> bool:
        return self.gemini.is_available()

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
