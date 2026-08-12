"""Chain-of-thought planner for complex algorithmic problems.

Uses the reasoning model to decompose a problem into explicit steps, then
returns a structured plan that downstream agents can execute.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from modeling.neural_backbones import NeuralBackbone, get_backbone

REASONING_SYSTEM = (
    "You are a reasoning engine. Decompose the user's technical problem into "
    "explicit, ordered steps using chain-of-thought. For each step, state the "
    "goal, the approach, and the expected outcome. End with a concise action list."
)


@dataclass
class PlanStep:
    index: int
    goal: str
    approach: str
    expected_outcome: str


@dataclass
class ReasoningPlan:
    summary: str
    steps: list[PlanStep] = field(default_factory=list)
    action_list: list[str] = field(default_factory=list)
    raw: str = ""

    @property
    def ok(self) -> bool:
        return bool(self.steps) or bool(self.action_list)


class ReasoningEngine:
    """Wraps the reasoning model for structured chain-of-thought planning."""

    def __init__(self, backbone: NeuralBackbone | None = None) -> None:
        self.backbone = backbone or get_backbone()

    def plan(self, problem: str, context: str | None = None) -> ReasoningPlan:
        prompt = self._build_prompt(problem, context)
        resp = self.backbone.reason(prompt, system=REASONING_SYSTEM)
        return self._parse(resp.text, problem)

    def _build_prompt(self, problem: str, context: str | None) -> str:
        parts = [f"# Problem\n{problem}"]
        if context:
            parts.append(f"# Context\n{context}")
        parts.append(
            "# Task\n"
            "1. Restate the problem in one sentence.\n"
            "2. Decompose into numbered steps. For each: GOAL / APPROACH / OUTCOME.\n"
            "3. End with 'ACTIONS:' followed by a bulleted action list."
        )
        return "\n\n".join(parts)

    def _parse(self, text: str, problem: str) -> ReasoningPlan:
        steps: list[PlanStep] = []
        actions: list[str] = []
        summary = problem
        lines = text.splitlines()
        idx = 0
        for line in lines:
            stripped = line.strip()
            if stripped.lower().startswith("actions:"):
                break
            if stripped and (stripped[0].isdigit() or stripped.startswith("- ")):
                goal = stripped.lstrip("0123456789.-) ").strip()
                steps.append(PlanStep(
                    index=idx, goal=goal, approach="", expected_outcome=""))
                idx += 1
        # capture actions
        in_actions = False
        for line in lines:
            stripped = line.strip()
            if stripped.lower().startswith("actions:"):
                in_actions = True
                continue
            if in_actions and stripped:
                actions.append(stripped.lstrip("-*0123456789.) ").strip())
        # first non-empty line as summary
        for line in lines:
            if line.strip() and not line.strip().startswith("#"):
                summary = line.strip()
                break
        return ReasoningPlan(summary=summary, steps=steps, action_list=actions, raw=text)
