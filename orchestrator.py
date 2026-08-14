#!/usr/bin/env python3
"""
orchestrator.py - LLM planner.

Breaks a high-level objective into concrete, executable steps and hands each
step to the smart orchestrator for routing to a capability.

When a real Gemini key is configured, planning is delegated to Gemini 2.5
Flash. Without a key, the deterministic local planner in :mod:`core.llm`
produces a single routed step for direct capability requests.
"""

import json
import re
from typing import Any, Dict, List, Optional


class Orchestrator:
    """Plans multi-step tasks using the reasoning LLM."""

    def __init__(self, model_router: Any = None):
        self.model_router = model_router

    def plan(self, objective: str, context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Return an ordered list of step dicts: {step, capability, args}."""
        text = self._reason(objective, context)
        steps = self._parse_steps(text, objective)
        return steps

    def _reason(self, objective: str, context: Optional[Dict[str, Any]] = None) -> str:
        ctx = json.dumps(context or {})
        prompt = (
            "You are the planner of an Autonomous Computer AI Assistant. "
            "Break the following objective into a JSON array of concrete steps. "
            "Each step must be an object with keys 'step' (the action), "
            "'capability' (the capability name to use, or null), and 'args' (a string argument or null). "
            "Only output the JSON array, nothing else.\n\n"
            f"Objective: {objective}\nContext: {ctx}\n\n"
            "Return JSON like: [{\"step\": \"...\", \"capability\": \"...\", \"args\": \"...\"}]"
        )
        if self.model_router is None:
            return prompt
        try:
            return self.model_router.reason(prompt)
        except Exception:
            return prompt

    def _parse_steps(self, text: str, objective: str) -> List[Dict[str, Any]]:
        steps: List[Dict[str, Any]] = []
        # Try to find a JSON array in the LLM response.
        match = re.search(r"\[.*\]", text, re.S)
        if match:
            try:
                parsed = json.loads(match.group(0))
                if isinstance(parsed, list):
                    for item in parsed:
                        if isinstance(item, dict) and "step" in item:
                            steps.append({
                                "step": str(item["step"]),
                                "capability": item.get("capability"),
                                "args": item.get("args"),
                            })
            except json.JSONDecodeError:
                pass
        # Fallback: parse numbered/bulleted lines.
        if not steps:
            for line in text.splitlines():
                stripped = line.strip()
                if not stripped:
                    continue
                if stripped[0].isdigit() or stripped.startswith(("- ", "* ")):
                    clean = re.sub(r"^[\d\.\-\*\)\s]+", "", stripped).strip()
                    if clean:
                        steps.append({"step": clean, "capability": None, "args": None})
        if not steps:
            steps.append({"step": objective, "capability": None, "args": None})
        return steps
