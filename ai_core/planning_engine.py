"""Step-by-step execution planner for project-wide edits.

Translates a high-level goal into an ordered, dependency-aware task plan that
targets specific files, agents, and capabilities. Coordinates with the
reasoning engine for decomposition and the context manager for grounding.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ai_core.context_manager import ContextManager, ContextRequest
from ai_core.reasoning_engine import ReasoningEngine, ReasoningPlan
from modeling.neural_backbones import NeuralBackbone, get_backbone

PLANNER_SYSTEM = (
    "You are an execution planner for a multi-file codebase. Given a goal and "
    "repository context, produce an ordered execution plan. For each task, "
    "specify: target file(s), the responsible agent, the capability used, and "
    "a one-line description. Respect existing style and minimize changes."
)


@dataclass
class ExecutionTask:
    index: int
    target_files: list[str]
    agent: str
    capability: str
    description: str
    depends_on: list[int] = field(default_factory=list)


@dataclass
class ExecutionPlan:
    goal: str
    tasks: list[ExecutionTask] = field(default_factory=list)
    rationale: str = ""
    raw: str = ""


class PlanningEngine:
    """Produces execution plans for project-wide work."""

    def __init__(self, backbone: NeuralBackbone | None = None,
                 context_manager: ContextManager | None = None,
                 reasoning: ReasoningEngine | None = None) -> None:
        self.backbone = backbone or get_backbone()
        self.context_manager = context_manager or ContextManager()
        self.reasoning = reasoning or ReasoningEngine(self.backbone)

    def plan(self, goal: str, workspace: str = ".",
             relevant_files: list[str] | None = None,
             directives: list[str] | None = None) -> ExecutionPlan:
        request = ContextRequest(
            user_message=goal, workspace=workspace,
            relevant_files=relevant_files or [], extra_directives=directives or [])
        context = self.context_manager.build(request)
        reasoning_plan = self.reasoning.plan(goal, context=context)

        prompt = self._build_prompt(goal, context, reasoning_plan)
        resp = self.backbone.reason(prompt, system=PLANNER_SYSTEM)
        tasks = self._parse_tasks(resp.text)
        return ExecutionPlan(goal=goal, tasks=tasks,
                             rationale=reasoning_plan.summary, raw=resp.text)

    def _build_prompt(self, goal: str, context: str, reasoning: ReasoningPlan) -> str:
        steps = "\n".join(f"  {i + 1}. {s.goal}" for i, s in enumerate(reasoning.steps))
        return (
            f"# Goal\n{goal}\n\n"
            f"# Reasoning steps\n{steps or '(none)'}\n\n"
            f"# Context\n{context}\n\n"
            "# Task\n"
            "Produce an ordered execution plan. Format each task as:\n"
            "[N] FILES: <files> | AGENT: <agent> | CAPABILITY: <capability> | DESC: <description> | DEPS: <indices>\n"
            "Use agents: coding, architect, refactoring, debugging, testing, review, project."
        )

    def _parse_tasks(self, text: str) -> list[ExecutionTask]:
        tasks: list[ExecutionTask] = []
        for line in text.splitlines():
            line = line.strip()
            if not line or not line[0].isdigit():
                continue
            if "|" not in line:
                continue
            parts = self._split_task(line)
            if not parts:
                continue
            try:
                idx = int(parts.get("index", "0").strip("[] "))
            except ValueError:
                continue
            tasks.append(ExecutionTask(
                index=idx,
                target_files=[f.strip() for f in parts.get("files", "").split(",") if f.strip()],
                agent=parts.get("agent", "coding").strip(),
                capability=parts.get("capability", "code_synthesis").strip(),
                description=parts.get("desc", "").strip(),
                depends_on=self._parse_deps(parts.get("deps", "")),
            ))
        return tasks

    def _split_task(self, line: str) -> dict[str, str] | None:
        # "[1] FILES: a.py, b.py | AGENT: coding | CAPABILITY: code_synthesis | DESC: ... | DEPS: 0"
        try:
            head, rest = line.split("]", 1)
            idx = head.strip("[")
            result = {"index": idx}
            for seg in rest.split("|"):
                if ":" in seg:
                    k, v = seg.split(":", 1)
                    result[k.strip().lower()] = v.strip()
            return result
        except ValueError:
            return None

    def _parse_deps(self, deps: str) -> list[int]:
        out: list[int] = []
        for tok in deps.replace(",", " ").split():
            try:
                out.append(int(tok))
            except ValueError:
                continue
        return out
