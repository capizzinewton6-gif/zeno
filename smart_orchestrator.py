#!/usr/bin/env python3
"""
smart_orchestrator.py - the central brain.

Wires together the AI model router, all action tools, the workflow/automation
engine, smart agents, sensors, autonomy, security and integrations. Routes a
natural-language objective through planning -> capability execution -> response.
"""

import json
import os
import re
from typing import Any, Dict, List, Optional

from orchestrator import Orchestrator

import actions
import automation
import smart_agents
import sensors
import autonomy
import security
import integrations
import ai_models


CAPABILITY_KEYWORDS: Dict[str, List[str]] = {
    "actions.web_search": ["search", "google", "look up", "find online"],
    "actions.url_launcher": ["open url", "open website", "open link", "go to"],
    "actions.file_controller": ["create file", "move file", "copy file", "delete file"],
    "actions.terminal_manager": ["run command", "terminal", "shell", "bash"],
    "actions.system_monitor": ["system status", "cpu", "ram", "monitor"],
    "actions.screenshot": ["screenshot", "capture screen"],
    "actions.music_player": ["play music"],
    "actions.calendar_manager": ["schedule", "calendar", "meeting"],
    "actions.gmail_sender": ["send email", "email"],
    "actions.reminder": ["remind me", "reminder"],
    "actions.weather_report": ["weather", "forecast"],
    "actions.translation_service": ["translate"],
    "actions.qr_generator": ["qr code"],
}


class SmartOrchestrator:
    """Central brain that routes objectives to the right capabilities."""

    def __init__(self):
        # AI layer
        self.ai_models = ai_models.get_modules()
        self.model_router = integrations.get_module("ai_model_router") or _FallbackRouter()
        self.integrations = integrations.get_modules()

        # Capability layers
        self.actions = actions.get_actions()
        self.automation = automation.get_modules()
        self.smart_agents = smart_agents.get_modules()
        self.sensors = sensors.get_modules()
        self.autonomy = autonomy.get_modules()
        self.security = security.get_modules()

        # Planner
        self.planner = Orchestrator(model_router=self.model_router)

        print(
            f"[orchestrator] loaded "
            f"actions={len(self.actions)} automation={len(self.automation)} "
            f"agents={len(self.smart_agents)} sensors={len(self.sensors)} "
            f"autonomy={len(self.autonomy)} security={len(self.security)} "
            f"integrations={len(self.integrations)} ai_models={len(self.ai_models)}"
        )

    # -- public API ---------------------------------------------------------

    def run(self, objective: str) -> str:
        """Plan and execute an objective end to end."""
        steps = self.planner.plan(objective)
        results: List[str] = []
        for step in steps:
            capability = self._route(step)
            outcome = self._execute(capability, step.get("step", str(step)))
            results.append(outcome)
        return self._summarize(objective, results)

    # -- routing ------------------------------------------------------------

    def _route(self, step: Dict[str, Any]) -> Optional[Any]:
        text = (step.get("step") or "").lower()
        # explicit hint from planner
        hint = step.get("capability")
        if hint:
            found = self.actions.get(hint) or self.automation.get(hint)
            if found:
                return found
        for cap_key, keywords in CAPABILITY_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                pkg, _, name = cap_key.partition(".")
                registry = {"actions": self.actions, "automation": self.automation}.get(pkg, {})
                if name in registry:
                    return registry[name]
        return None

    def _execute(self, capability: Any, task: str) -> str:
        if capability is None:
            # fall back to the reasoning model
            return self.model_router.reason(task)
        try:
            result = capability.execute(task)
            if isinstance(result, dict):
                return result.get("status", json.dumps(result))
            return str(result)
        except Exception as exc:
            return f"capability error: {exc}"

    def _summarize(self, objective: str, results: List[str]) -> str:
        if len(results) == 1:
            return results[0]
        joined = " | ".join(results)
        try:
            return self.model_router.summarize(joined)
        except Exception:
            return joined


class _FallbackRouter:
    """Minimal stand-in used when no AI model router is configured."""

    def reason(self, prompt: str) -> str:
        return prompt

    def summarize(self, text: str) -> str:
        return text
