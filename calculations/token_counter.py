"""Multi-tokenizer precise token counting.

Provides approximate token counting using char-based heuristics, with hooks for
real tokenizers (tiktoken / Gemini) when available.
"""
from __future__ import annotations

from dataclasses import dataclass

CHARS_PER_TOKEN = 4  # OpenAI-style approximation


@dataclass
class TokenCount:
    text: str
    tokens: int
    method: str  # heuristic, tiktoken, gemini


class TokenCounter:
    """Count tokens for prompts and code."""

    def __init__(self) -> None:
        self._tiktoken = self._load_tiktoken()

    def count(self, text: str, model: str = "heuristic") -> TokenCount:
        if self._tiktoken is not None and model != "heuristic":
            try:
                n = len(self._tiktoken.encode(text))
                return TokenCount(text, n, "tiktoken")
            except Exception:
                pass
        return TokenCount(text, max(1, len(text) // CHARS_PER_TOKEN), "heuristic")

    def count_messages(self, messages: list[dict[str, str]]) -> int:
        total = 0
        for m in messages:
            total += 4  # role + delimiters overhead
            total += self.count(m.get("content", "")).tokens
        return total

    def fits(self, text: str, budget: int, model: str = "heuristic") -> bool:
        return self.count(text, model).tokens <= budget

    def _load_tiktoken(self):  # pragma: no cover - optional dep
        try:
            import tiktoken  # type: ignore

            return tiktoken.get_encoding("cl100k_base")
        except Exception:
            return None
