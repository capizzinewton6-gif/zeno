"""AI engine modules: Gemini 2.5 Flash, Gemini 1.5 Flash, model router.

Re-exports the engine implementations from ``ai_core``.
"""
from mathematics_ai.src.gemini_25_flash_engine import Gemini25FlashEngine
from mathematics_ai.src.gemini_15_flash_engine import Gemini15FlashEngine
from mathematics_ai.src.model_router import ModelRouter
__all__ = ["Gemini25FlashEngine", "Gemini15FlashEngine", "ModelRouter"]
