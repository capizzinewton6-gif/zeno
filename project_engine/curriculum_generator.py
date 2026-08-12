"""Generates step-by-step project build specifications."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from modeling.neural_backbones import NeuralBackbone, get_backbone

CURRICULUM_SYSTEM = (
    "You are a curriculum generator. Break a project goal into a progressive, "
    "step-by-step build specification. Each step has: title, objective, skills, "
    "and acceptance criteria. Output JSON."
)


@dataclass
class CurriculumStep:
    index: int
    title: str
    objective: str
    skills: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)


@dataclass
class Curriculum:
    project: str
    steps: list[CurriculumStep] = field(default_factory=list)

    @property
    def total_steps(self) -> int:
        return len(self.steps)


class CurriculumGenerator:
    """Generates build specifications from a project description."""

    def __init__(self, backbone: NeuralBackbone | None = None) -> None:
        self.backbone = backbone or get_backbone()

    def generate(self, project: str, level: str = "intermediate",
                 steps: int = 8) -> Curriculum:
        prompt = (
            f"Create a {steps}-step curriculum to build: {project}.\n"
            f"Target level: {level}. Output JSON array of steps."
        )
        resp = self.backbone.reason(prompt, system=CURRICULUM_SYSTEM, task="curriculum")
        parsed = self._parse(resp.text)
        curric_steps = [
            CurriculumStep(
                index=i,
                title=s.get("title", f"Step {i}"),
                objective=s.get("objective", ""),
                skills=s.get("skills", []),
                acceptance_criteria=s.get("acceptance_criteria", []),
            )
            for i, s in enumerate(parsed, 1)
        ] or self._fallback(project, steps)
        return Curriculum(project=project, steps=curric_steps)

    def _parse(self, text: str) -> list[dict[str, Any]]:
        import json
        import re
        m = re.search(r"\[.*\]", text, re.DOTALL)
        if not m:
            return []
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            return []

    def _fallback(self, project: str, n: int) -> list[CurriculumStep]:
        titles = ["Setup & structure", "Core data model", "Business logic",
                  "CLI/UI layer", "Persistence", "Tests", "Documentation",
                  "Polish & deploy"]
        return [
            CurriculumStep(index=i, title=titles[i - 1] if i <= len(titles) else f"Step {i}",
                           objective=f"Implement {titles[i-1].lower()} for {project}.")
            for i in range(1, n + 1)
        ]
