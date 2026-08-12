"""Context window optimization and token truncation heuristics.

Estimates token counts (or char/4 fallback) and assembles a context payload
that fits within a configured budget while preserving the most relevant content.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from config import get_settings

_APPROX_CHARS_PER_TOKEN = 4


@dataclass
class TokenBudget:
    max_tokens: int = 1_000_000
    reserve_for_response: int = 8192
    strategy: str = "keep_imports_and_signatures"

    @classmethod
    def from_settings(cls) -> "TokenBudget":
        cfg = get_settings().get("token_budget", {})
        return cls(
            max_tokens=cfg.get("context_window", 1_000_000),
            reserve_for_response=cfg.get("reserve_for_response", 8192),
            strategy=cfg.get("truncation_strategy", "keep_imports_and_signatures"),
        )

    @property
    def available(self) -> int:
        return max(0, self.max_tokens - self.reserve_for_response)


def estimate_tokens(text: str) -> int:
    """Cheap token estimate (chars/4) used when no tokenizer is available."""
    return max(1, len(text) // _APPROX_CHARS_PER_TOKEN)


@dataclass
class ContextChunk:
    label: str
    content: str
    priority: int = 0  # higher = more important
    tokens: int = 0

    def __post_init__(self) -> None:
        if self.tokens == 0:
            self.tokens = estimate_tokens(self.content)


class ContextWindow:
    """Assembles and truncates context to fit a token budget."""

    def __init__(self, budget: TokenBudget | None = None) -> None:
        self.budget = budget or TokenBudget.from_settings()
        self._chunks: list[ContextChunk] = []

    def add(self, label: str, content: str, priority: int = 0) -> None:
        self._chunks.append(ContextChunk(label=label, content=content, priority=priority))

    def reset(self) -> None:
        self._chunks.clear()

    def assemble(self) -> str:
        """Return concatenated context fitting the budget.

        Chunks are kept in priority order (highest first); if they exceed the
        budget, lower-priority chunks are truncated or dropped.
        """
        available = self.budget.available
        ordered = sorted(self._chunks, key=lambda c: -c.priority)
        parts: list[str] = []
        used = 0
        for chunk in ordered:
            if used + chunk.tokens <= available:
                parts.append(self._fmt(chunk))
                used += chunk.tokens
            else:
                remaining = available - used
                if remaining > 0:
                    text = chunk.content[: remaining * _APPROX_CHARS_PER_TOKEN]
                    parts.append(self._fmt(chunk, truncated=text))
                break
        return "\n\n".join(parts)

    def _fmt(self, chunk: ContextChunk, truncated: str | None = None) -> str:
        body = truncated if truncated is not None else chunk.content
        return f"## {chunk.label}\n{body}"

    def usage(self) -> dict[str, int]:
        total = sum(c.tokens for c in self._chunks)
        return {"used": total, "budget": self.budget.available,
                "remaining": max(0, self.budget.available - total)}
