"""Multistep experimental and cloning planning engine."""
from __future__ import annotations

import json

from ai_core.ai_engine import AIEngine


class PlanningEngine:
    """Decomposes a high-level goal into ordered, validated steps."""

    def __init__(self, ai: AIEngine | None = None):
        self.ai = ai or AIEngine()

    def plan_experiment(self, goal: str, constraints: str = "") -> list[dict]:
        prompt = (
            "Decompose the following experimental goal into an ordered list of steps. "
            "For each step return a JSON object with keys: step, action, reagents, "
            "duration, expected_outcome, risk. Return ONLY a JSON list.\n\n"
            f"Goal: {goal}\nConstraints: {constraints or 'none'}"
        )
        raw = self.ai.reason(prompt)
        steps = self._safe_parse(raw)
        if not steps:
            steps = self._generic_plan(goal)
        return steps

    def plan_cloning(self, goal: str) -> list[dict]:
        prompt = (
            "Design a molecular cloning workflow (PCR, restriction, ligation or "
            "Gibson/Golden Gate, transformation, screening) for the following goal. "
            "Return ONLY a JSON list of steps with keys: step, action, reagents, "
            "duration, expected_outcome, risk.\n\nGoal: " + goal
        )
        raw = self.ai.reason(prompt)
        steps = self._safe_parse(raw)
        if not steps:
            steps = self._generic_plan(goal)
        return steps

    @staticmethod
    def _safe_parse(raw: str) -> list[dict]:
        try:
            start = raw.index("[")
            end = raw.rindex("]")
            return json.loads(raw[start : end + 1])
        except (ValueError, json.JSONDecodeError):
            return []

    @staticmethod
    def _generic_plan(goal: str) -> list[dict]:
        return [
            {"step": 1, "action": "Define objective", "reagents": "none",
             "duration": "15 min", "expected_outcome": "Written hypothesis", "risk": "low"},
            {"step": 2, "action": "Design protocol", "reagents": "none",
             "duration": "30 min", "expected_outcome": "Protocol draft", "risk": "low"},
            {"step": 3, "action": "Prepare reagents", "reagents": "TBD",
             "duration": "1 h", "expected_outcome": "Master mix / media ready", "risk": "low"},
            {"step": 4, "action": "Execute experiment", "reagents": "TBD",
             "duration": "varies", "expected_outcome": "Raw data", "risk": "medium"},
            {"step": 5, "action": "Analyze results", "reagents": "none",
             "duration": "1 h", "expected_outcome": "Annotated data", "risk": "low"},
        ]
