"""Shared helpers for biology domain modules."""
from __future__ import annotations

import re


def extract_sequence(text: str, min_len: int = 5) -> str:
    """Pull the first nucleotide-like or protein-like token from text."""
    nuc = re.findall(r"[ACGTUNacgtun]{%d,}" % min_len, text)
    return nuc[0].upper() if nuc else ""


def safe_ai_reason(query: str, ctx=None) -> str:
    """Return a helpful offline note when the AI engine is not reachable.

    Biology modules call this as a last resort for free-text questions that
    cannot be answered with their deterministic algorithms.
    """
    ctx_str = ctx.context_string() if ctx is not None else ""
    return (
        f"[deterministic module] I cannot fully answer this with built-in "
        f"calculations alone.\nContext: {ctx_str}\nQuery: {query}\n"
        "Connect a Gemini API key (config 'google_api_key') to enable "
        "LLM-assisted reasoning for this question."
    )
