#!/usr/bin/env python3
"""
smart_orchestrator.py - the central brain.

Wires together the AI model router, all action tools, the workflow/automation
engine, smart agents, sensors, autonomy, security and integrations. Routes a
natural-language objective through planning -> capability execution -> response.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from orchestrator import Orchestrator
from core.capability import result_to_text

import actions
import automation
import smart_agents
import sensors
import autonomy
import security
import integrations
import ai_models


CAPABILITY_KEYWORDS: Dict[str, List[str]] = {
    "web_search": ["search", "google", "look up", "find online", "find info", "search the web"],
    "url_launcher": ["open url", "open website", "open link", "go to http", "navigate to http", "open http"],
    "file_controller": ["create file", "move file", "copy file", "delete file", "rename file",
                        "list file", "list dir", "show files", "find file", "read file", "create dir", "mkdir"],
    "terminal_manager": ["run command", "run cmd", "terminal", "shell", "bash", "execute command", "run "],
    "system_monitor": ["system status", "cpu", "ram", "memory usage", "monitor system",
                       "disk", "storage", "free space", "battery", "power status", "network usage"],
    "screenshot": ["screenshot", "capture screen", "take screenshot"],
    "music_player": ["play music", "play song", "stop music", "pause music"],
    "calendar_manager": ["schedule", "calendar", "meeting", "event", "list events"],
    "gmail_sender": ["send email", "send gmail", "email to"],
    "reminder": ["remind me", "reminder", "set reminder", "list reminder"],
    "note_taker": ["take note", "note that", "remember that", "list note", "show note"],
    "weather_report": ["weather", "forecast"],
    "translation_service": ["translate", "translation"],
    "qr_generator": ["qr code", "generate qr", "make qr"],
    "ip_checker": ["ip address", "my ip", "public ip", "what is my ip"],
    "app_manager": ["open app", "launch app", "start app", "close app", "install ", "uninstall "],
    "calculator": ["calculate", "calc ", "what is", "what's", "compute", "evaluate", "math"],
}


class SmartOrchestrator:
    """Central brain that routes objectives to the right capabilities."""

    def __init__(self):
        # AI layer
        self.ai_models = ai_models.get_modules()
        self.model_router = integrations.get_module("ai_model_router")
        if self.model_router is None:
            self.model_router = _FallbackRouter()
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

        # System prompt
        self.prompt = self._load_prompt()

        llm_status = "online" if getattr(self.model_router, "is_available", lambda: False)() else "offline (local fallback)"
        print(
            f"[orchestrator] llm={llm_status} | "
            f"actions={len(self.actions)} automation={len(self.automation)} "
            f"agents={len(self.smart_agents)} sensors={len(self.sensors)} "
            f"autonomy={len(self.autonomy)} security={len(self.security)} "
            f"integrations={len(self.integrations)} ai_models={len(self.ai_models)}"
        )

    @staticmethod
    def _load_prompt() -> str:
        path = Path(__file__).resolve().parent / "core" / "prompt.txt"
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    # -- public API ---------------------------------------------------------

    def run(self, objective: str) -> str:
        """Plan and execute an objective end to end."""
        # Built-in meta commands.
        low = objective.lower().strip()
        if low in {"help", "?", "capabilities", "list capabilities", "what can you do"}:
            return self.list_capabilities()
        if low in {"status", "system status"}:
            return result_to_text(self.actions.get("system_monitor").execute("system status"))

        steps = self.planner.plan(objective)
        results: List[str] = []
        for step in steps:
            capability = self._route(step)
            outcome = self._execute(capability, step)
            results.append(outcome)
        return self._summarize(objective, results)

    def list_capabilities(self) -> str:
        """Return a human-readable summary of available capabilities."""
        names = sorted(self.actions.keys())
        return (
            f"I have {len(names)} action capabilities. A few useful ones:\n"
            + ", ".join(names[:40])
            + ("\n  ..." if len(names) > 40 else "")
            + "\n\nExamples: 'system status', 'search for AI news', 'weather in London', "
            "'translate \"hello\" to es', 'calculate 12 * (3 + 4)', 'create file \"a.txt\" \"hi\"'."
        )

    # -- routing ------------------------------------------------------------

    def _route(self, step: Dict[str, Any]) -> Optional[Any]:
        text = (step.get("step") or "").lower()
        args = step.get("args")
        if args and isinstance(args, str):
            text = f"{text} {args}".lower()
        # explicit hint from planner
        hint = step.get("capability")
        if hint:
            found = self.actions.get(hint) or self.automation.get(hint)
            if found:
                return found
        # keyword match
        for cap_name, keywords in CAPABILITY_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                found = self.actions.get(cap_name) or self.automation.get(cap_name)
                if found:
                    return found
        return None

    def _execute(self, capability: Any, step: Dict[str, Any]) -> str:
        # Prefer the step's args, fall back to the step text itself.
        task = step.get("args") or step.get("step") or str(step)
        if capability is None:
            # No matching capability - ask the reasoning model to respond.
            return self.model_router.reason(task)
        try:
            result = capability.execute(task)
            return result_to_text(result)
        except Exception as exc:
            return f"capability error: {exc}"

    def _summarize(self, objective: str, results: List[str]) -> str:
        results = [r for r in results if r]
        if len(results) == 1:
            return results[0]
        joined = "\n".join(f"- {r}" for r in results)
        try:
            summary = self.model_router.summarize(joined)
            return f"{summary}\n\nDetails:\n{joined}"
        except Exception:
            return joined


class _FallbackRouter:
    """Minimal stand-in used when no AI model router is configured."""

    def reason(self, prompt: str) -> str:
        return prompt

    def summarize(self, text: str) -> str:
        return text

    def is_available(self) -> bool:
        return False
