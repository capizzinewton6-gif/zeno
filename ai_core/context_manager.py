"""Assembles code, documentation, and user guidelines into prompt context.

Combines the system persona, repository map, relevant file contents, symbol
information, and user preferences into a single context payload bounded by the
configured token budget.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ai_core.safety_layer import SafetyLayer
from config import env_or_key, load_json, memory_file
from modeling.context_window import ContextWindow, TokenBudget
from modeling.repo_map import RepoMapper, RepoMap


@dataclass
class ContextRequest:
    user_message: str
    workspace: str = "."
    relevant_files: list[str] = field(default_factory=list)
    extra_directives: list[str] = field(default_factory=list)
    include_repo_map: bool = True
    include_preferences: bool = True


class ContextManager:
    """Builds the prompt context for a given user request."""

    def __init__(self, repo_mapper: RepoMapper | None = None,
                 budget: TokenBudget | None = None) -> None:
        self.repo_mapper = repo_mapper or RepoMapper()
        self.budget = budget or TokenBudget.from_settings()

    def build(self, request: ContextRequest) -> str:
        ctx = ContextWindow(self.budget)

        # System persona (highest priority)
        persona = self._load_persona()
        ctx.add("System Persona", persona, priority=100)

        # User preferences
        if request.include_preferences:
            prefs = load_json(memory_file("preferences.json"))
            ctx.add("User Preferences", self._fmt_prefs(prefs), priority=90)

        # Repository map
        repo_map: RepoMap | None = None
        if request.include_repo_map and Path(request.workspace).exists():
            repo_map = self.repo_mapper.map_directory(request.workspace)
            ctx.add("Repository Map", repo_map.to_skeleton(), priority=80)

        # Relevant files
        for rel in request.relevant_files:
            content = self._read_file(request.workspace, rel)
            if content:
                ctx.add(f"File: {rel}", content, priority=70)

        # Directives
        if request.extra_directives:
            ctx.add("Directives", "\n".join(f"- {d}" for d in request.extra_directives), priority=60)

        # The actual user request (always included, high priority)
        ctx.add("User Request", request.user_message, priority=95)

        return ctx.assemble()

    def _load_persona(self) -> str:
        prompt_path = Path(__file__).parent / "prompt.txt"
        try:
            return prompt_path.read_text(encoding="utf-8")
        except OSError:
            return "You are CODING_AI, a Principal Software Engineer AI."

    def _fmt_prefs(self, prefs: dict[str, Any]) -> str:
        if not prefs:
            return "No preferences recorded."
        lines = [f"- {k}: {v}" for k, v in prefs.items() if not k.startswith("_")]
        return "\n".join(lines)

    def _read_file(self, workspace: str, rel: str) -> str | None:
        path = Path(workspace) / rel
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None
