"""Workspace coordinator, issue generator, and PR manager."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from agents.base import AgentResult, BaseAgent

PROJECT_SYSTEM = (
    "You are a project coordinator. Manage tasks, milestones, and developer "
    "workflow. Output actionable, structured task lists and next steps."
)


@dataclass
class Task:
    id: str
    title: str
    status: str = "todo"  # todo, in_progress, done, blocked
    priority: str = "medium"
    assignee: str = ""
    description: str = ""


@dataclass
class ProjectState:
    goal: str
    tasks: list[Task] = field(default_factory=list)
    milestones: list[dict[str, Any]] = field(default_factory=list)


class ProjectAgent(BaseAgent):
    name = "project"
    capability = "repository_indexer"

    def _execute(self, message: str, **kwargs: Any) -> AgentResult:
        plan = kwargs.get("plan")
        if plan and plan.tasks:
            tasks = self._tasks_from_plan(plan)
        else:
            tasks = self._tasks_from_message(message)
        state = ProjectState(goal=message, tasks=tasks)
        content = json.dumps(
            {"goal": state.goal,
             "tasks": [t.__dict__ for t in state.tasks]}, indent=2)
        return AgentResult(
            self.name, self.capability, content=content,
            actions=[f"created {len(tasks)} tasks"],
            artifacts=[{"type": "project_state", "tasks": [t.__dict__ for t in tasks]}],
        )

    def _tasks_from_plan(self, plan: Any) -> list[Task]:
        return [
            Task(id=f"T{i}", title=t.description[:80], status="todo",
                 priority="medium", assignee=t.agent,
                 description=t.description)
            for i, t in enumerate(plan.tasks, 1)
        ]

    def _tasks_from_message(self, message: str) -> list[Task]:
        return [
            Task(id="T1", title=message[:80], status="todo",
                 description=message),
        ]

    def create_pr(self, title: str, body: str, files: list[str]) -> dict[str, Any]:
        """Produce a PR description artifact (does not push to remote)."""
        return {
            "title": title,
            "body": body,
            "files": files,
            "status": "draft",
            "note": "PR artifact generated; push to create the actual PR.",
        }
