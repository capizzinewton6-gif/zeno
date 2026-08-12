"""
ai_models - model_evaluator
============================
Compare and evaluate models.
"""

import os
from typing import Any, Dict, Optional


class ModelEvaluator:
    """Compare and evaluate models."""

    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.config = config or {}
        self.model = None
        self.available = bool(self.api_key)

    def execute(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Run a prompt through the model."""
        if not self.available:
            return "ModelEvaluator: no API key configured"
        # TODO: wire to real provider SDK
        return f"{class_name} stub response for: {prompt[:80]}"

    def is_available(self) -> bool:
        return self.available
