"""Curriculum and project idea engine tailored to developer skill level."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from ai_core.knowledge_engine import KnowledgeEngine
from agents.base import AgentResult, BaseAgent

RECOMMEND_SYSTEM = (
    "You are a project curriculum designer. Given a developer's skill level "
    "and goals, recommend 3 projects of increasing difficulty. For each: name, "
    "difficulty (beginner/intermediate/advanced), skills_practiced, description. "
    "Output JSON."
)

LEVELS = ("beginner", "intermediate", "advanced")


@dataclass
class ProjectIdea:
    name: str
    difficulty: str
    skills: list[str] = field(default_factory=list)
    description: str = ""


class ProjectRecommenderAgent(BaseAgent):
    name = "project_recommender"
    capability = "code_synthesis"

    def __init__(self, backbone: Any = None, knowledge: KnowledgeEngine | None = None) -> None:
        super().__init__(backbone)
        self.knowledge = knowledge or KnowledgeEngine()

    def _execute(self, message: str, **kwargs: Any) -> AgentResult:
        level = kwargs.get("level", "beginner")
        goal = message
        prompt = (
            f"Recommend 3 projects for a {level} developer with this goal: {goal}.\n"
            "Each project should build real skills. Output JSON array."
        )
        resp = self.backbone.reason(prompt, system=RECOMMEND_SYSTEM, task="recommend")
        ideas = self._parse(resp.text)
        if not ideas:
            ideas = self._fallback(goal, level)
        return AgentResult(
            self.name, self.capability,
            content=json.dumps(ideas, indent=2),
            actions=[f"recommended {len(ideas)} projects for {level}"],
            artifacts=[{"type": "recommendations", "ideas": ideas}],
        )

    def _parse(self, text: str) -> list[dict[str, Any]]:
        m = re.search(r"\[.*\]", text, re.DOTALL)
        if not m:
            return []
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            return []

    def _fallback(self, goal: str, level: str) -> list[dict[str, Any]]:
        base = [
            {"name": "CLI Todo Manager", "difficulty": "beginner",
             "skills": ["CLI", "file I/O", "tests"],
             "description": "A command-line todo app with persistence."},
            {"name": "REST API with Auth", "difficulty": "intermediate",
             "skills": ["HTTP", "auth", "database", "tests"],
             "description": "A REST API with JWT auth and a SQL backend."},
            {"name": "Multi-Agent Coding Tool", "difficulty": "advanced",
             "skills": ["LLM integration", "agents", "sandboxing"],
             "description": "A tool that coordinates agents to build features."},
        ]
        return [b for b in base if _level_rank(b["difficulty"]) >= _level_rank(level)][:3]


def _level_rank(level: str) -> int:
    return LEVELS.index(level) if level in LEVELS else 0
