"""Main AI intelligence engine.

Coordinates the reasoning, planning, context, knowledge, and safety
subsystems, and dispatches work between the Gemini 2.5 Flash (deep
reasoning) and Gemini 1.5 Flash (fast processing) engines.
"""

import logging

from .reasoning_engine import ReasoningEngine
from .planning_engine import PlanningEngine
from .context_manager import ContextManager
from .knowledge_engine import KnowledgeEngine
from .safety_layer import SafetyLayer

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.gemini_25_flash_engine import reason as gemini25_reason, describe as gemini25_describe
from src.gemini_15_flash_engine import process as gemini15_process, describe as gemini15_describe

logger = logging.getLogger(__name__)


class AIEngine:
    """Top-level AI intelligence orchestrator."""

    def __init__(self, api_key=None):
        self.reasoning = ReasoningEngine(api_key=api_key)
        self.planning = PlanningEngine()
        self.context = ContextManager()
        self.knowledge = KnowledgeEngine()
        self.safety = SafetyLayer()

    # --- Engine routing -------------------------------------------------
    def deep_reason(self, prompt, context=None):
        """Route advanced reasoning to Gemini 2.5 Flash."""
        ctx = self.context.snapshot() if context is None else context
        self.context.set_last_task(prompt)
        safety = self.safety.screen(prompt)
        if safety.get("blocked"):
            return {
                "engine": "safety_layer",
                "blocked": True,
                "response": safety["message"],
                "reason": safety["reason"],
            }
        plan = self.planning.plan(prompt, ctx)
        reasoning = self.reasoning.reason(prompt, ctx)
        return {
            "engine": "AIEngine",
            "plan": plan,
            "reasoning": reasoning,
            "safety": safety,
        }

    def fast_process(self, prompt, context=None):
        """Route fast processing to Gemini 1.5 Flash."""
        return gemini15_process(prompt, context)

    # --- Introspection --------------------------------------------------
    def describe(self):
        return {
            "ai_engine": "AIEngine orchestrator",
            "engines": [gemini25_describe(), gemini15_describe()],
            "subsystems": {
                "reasoning": "ReasoningEngine",
                "planning": "PlanningEngine",
                "context": "ContextManager",
                "knowledge": "KnowledgeEngine",
                "safety": "SafetyLayer",
            },
        }
