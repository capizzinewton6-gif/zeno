"""Model router: routes requests between Gemini 2.5 Flash and 1.5 Flash.

Re-exports the router implementation from ``ai_core``. This module is the
spec-mandated namespace ``src/model_router``.
"""
from mathematics_ai.ai_core.model_router import ModelRouter
__all__ = ["ModelRouter"]
