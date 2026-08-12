#!/usr/bin/env python3
"""
orchestrator.py - LLM planner.

Breaks a high-level objective into concrete, executable steps and hands each
step to the smart orchestrator for routing to a capability.
"""

import json
import os
from typing import Any, Dict, List, Optional


class Orchestrator:
    """Plans multi-step tasks using the reasoning LLM."""

    def __init__(self, model_router: Any = None):
        self.model_router = model_router

    def _reason(self, prompt: str) -> str:
        if self.model_router is None:
            return prompt
        try:
            return self.model_router.reason(prompt)
        except Exception:
            return prompt

    def plan(self, objective: str, context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Return an ordered list of step dicts: {step, capability, args}."""
        ctx = json.dumps(context or {})
        prompt = (
            "Break the following objective into a numbered list of concrete steps. "
            "For each step suggest which capability should perform it.\n\n"
            f"Objective: {objective}\nContext: {ctx}\n\n"
            "Return JSON like: [{\"step\": \"...\", \"capability\": \"...\", \"args\": \"...\"}]"
        )
        text = self._reason(prompt)
        steps = self._parse_steps(text, objective)
        return steps

    def _parse_steps(self, text: str, objective: str) -> List[Dict[str, Any]]:
        steps: List[Dict[str, Any]] = []
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or not (stripped[0].isdigit() or stripped.startswith(("- ", "* "))):
                continue
            steps.append({"step": stripped, "capability": None, "args": None})
        if not steps:
            steps.append({"step": objective, "capability": None, "args": None})
        return steps
