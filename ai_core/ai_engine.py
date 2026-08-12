"""AI engine: main decision-making intelligence tying the brain to capabilities.

The AI engine is the conductor. It uses:
- Gemini 2.5 Flash for high-level visual reasoning, planning, decisions.
- Gemini 1.5 Flash for fast preprocessing/OCR/validation.
Local calculations + capability modules execute the actual work.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from ai_core.context_manager import ContextManager
from ai_core.knowledge_engine import KnowledgeEngine
from ai_core.planning_engine import PlanningEngine, Plan
from ai_core.reasoning_engine import ReasoningEngine, ReasoningResult
from ai_core.safety_layer import SafetyLayer


@dataclass
class Decision:
    goal: str
    plan: Plan
    reasoning: ReasoningResult
    alerts: List[str]
    summary: str


class AIEngine:
    """Main AI decision-making intelligence."""

    def __init__(self, flash25=None, flash15=None,
                 context: Optional[ContextManager] = None,
                 knowledge: Optional[KnowledgeEngine] = None,
                 safety: Optional[SafetyLayer] = None,
                 planner: Optional[PlanningEngine] = None) -> None:
        # Lazy import to avoid hard dependency at module load.
        if flash25 is None:
            from src.gemini_25_flash_engine import Gemini25FlashEngine
            flash25 = Gemini25FlashEngine()
        if flash15 is None:
            from src.gemini_15_flash_engine import Gemini15FlashEngine
            flash15 = Gemini15FlashEngine()
        self.flash25 = flash25
        self.flash15 = flash15
        self.context = context or ContextManager()
        self.knowledge = knowledge or KnowledgeEngine()
        self.safety = safety or SafetyLayer()
        self.planner = planner or PlanningEngine()

    @property
    def reasoning(self) -> ReasoningEngine:
        return ReasoningEngine(self.context)

    def understand_instruction(self, instruction: str, images: Sequence[bytes] = ()) -> Dict[str, Any]:
        """Convert a high-level instruction into a structured intent/plan JSON."""
        plan_json = self.flash25.plan(instruction, images)
        return plan_json if isinstance(plan_json, dict) else {"plan": [], "decision": str(plan_json)}

    def decide(self, instruction: str, images: Sequence[bytes] = ()) -> Decision:
        intent = self.understand_instruction(instruction, images)
        plan = self.planner.from_intent(intent)
        reasoning = self.reasoning.reason()
        alerts: List[str] = list(intent.get("alerts", [])) if isinstance(intent, dict) else []
        alerts.extend(reasoning.anomalies)
        summary = intent.get("decision", "") if isinstance(intent, dict) else ""
        if not summary:
            summary = reasoning.findings[0] if reasoning.findings else "No decision."
        return Decision(goal=instruction, plan=plan, reasoning=reasoning,
                        alerts=alerts, summary=summary)

    def describe(self, image_bytes: bytes) -> Dict[str, Any]:
        return self.flash25.describe_scene(image_bytes)

    def validate(self, image_bytes: bytes, label: str) -> bool:
        return self.flash15.validate_detection(image_bytes, label)

    def to_report(self, decision: Decision) -> Dict[str, Any]:
        return {
            "goal": decision.goal,
            "summary": decision.summary,
            "alerts": decision.alerts,
            "plan": decision.plan.to_dict(),
            "reasoning": {
                "findings": decision.reasoning.findings,
                "anomalies": decision.reasoning.anomalies,
                "behaviors": decision.reasoning.behaviors,
            },
            "context_summary": self.context.summarize(),
        }
