"""Engineering planning engine: decomposes objectives into structured,
multi-stage engineering plans."""

from __future__ import annotations

from typing import List

from src.gemini_25_flash_engine import Gemini25FlashEngine


class PlanningEngine:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def decompose(self, objective: str) -> List[str]:
        text = self.engine.generate(
            f"Decompose this objective into an ordered list of engineering tasks, "
            f"one per line, numbered: {objective}",
            system="You are a senior engineering planner.")
        return [line for line in text.splitlines() if line.strip()]

    def milestones(self, plan: List[str]) -> str:
        joined = "\n".join(plan)
        return self.engine.generate(
            f"Define milestones, deliverables, and acceptance criteria for:\n{joined}",
            system="You are a project planning engine.")

    def risk_plan(self, plan: List[str]) -> str:
        joined = "\n".join(plan)
        return self.engine.generate(
            f"Identify risks and mitigations for this plan:\n{joined}",
            system="You are a risk management engineer.")

    def schedule(self, tasks: List[str]) -> str:
        joined = "\n".join(tasks)
        return self.engine.generate(
            f"Create a dependency-aware schedule (Gantt-style text) for:\n{joined}",
            system="You are a scheduling engine.")
