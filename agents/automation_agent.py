"""Automation agent: automates screen tasks."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from automation.task_executor import TaskExecutor
from automation.workflow_builder import WorkflowBuilder
from agents.assistant_agent import AssistantAgent
from ai_core.context_manager import ContextManager

logger = logging.getLogger(__name__)


class AutomationAgent:
    """Plans and executes automated screen workflows."""

    def __init__(self, assistant: AssistantAgent | None = None,
                 executor: TaskExecutor | None = None,
                 context: ContextManager | None = None) -> None:
        self.assistant = assistant or AssistantAgent(context=context)
        self.executor = executor or TaskExecutor()
        self.context = context or self.assistant.context

    def build_workflow(self, goal: str, screen_context: Dict[str, Any],
                       image: Any = None) -> Dict[str, Any]:
        steps = self.assistant.plan(goal, screen_context, image)
        builder = WorkflowBuilder(name=goal, description=f"Auto-generated workflow for: {goal}")
        for step in steps:
            action = step.get("action", "wait")
            target = step.get("target")
            description = step.get("description", "")
            if action in ("click", "type", "key", "wait", "scroll"):
                builder.add_step({"action": action, "target": target, "description": description})
            else:
                builder.add_step({"action": "wait", "target": 0.5, "description": description})
        return builder.build()

    def execute_goal(self, goal: str, screen_context: Dict[str, Any],
                     image: Any = None, dry_run: bool = False) -> Dict[str, Any]:
        workflow = self.build_workflow(goal, screen_context, image)
        # Risk evaluation per step
        for step in workflow["steps"]:
            risk = self.assistant.evaluate_risk(step, screen_context)
            step["risk"] = risk.get("risk_level", "unknown")
        result = self.executor.execute(workflow, dry_run=dry_run)
        self.context.set("last_execution", result)
        return result

    def execute_workflow(self, workflow: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
        return self.executor.execute(workflow, dry_run=dry_run)

    def list_workflows(self) -> List[Dict[str, Any]]:
        return WorkflowBuilder.list_workflows()
