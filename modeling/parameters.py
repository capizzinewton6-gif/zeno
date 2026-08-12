"""Generation parameters (temperature, top_p, max_tokens).

Re-exported here so callers can import from ``modeling.parameters`` rather than
the backbone module directly, keeping the capability-source-of-truth rule clean.
"""
from __future__ import annotations

from modeling.neural_backbones import GenerationParameters

__all__ = ["GenerationParameters"]
