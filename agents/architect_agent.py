"""System designer for blueprinting directory schemas and interfaces."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from agents.base import AgentResult, BaseAgent
from modeling.neural_backbones import get_backbone

ARCHITECT_SYSTEM = (
    "You are a software architect. Given a project description, produce a "
    "blueprint: directory schema, module responsibilities, key interfaces, and "
    "data flow. Output JSON with keys: directories, interfaces, data_flow, notes."
)


@dataclass
class ArchitectureBlueprint:
    directories: list[dict[str, str]]
    interfaces: list[dict[str, str]]
    data_flow: list[str]
    notes: str = ""


class ArchitectAgent(BaseAgent):
    name = "architect"
    capability = "code_synthesis"

    def _execute(self, message: str, **kwargs: Any) -> AgentResult:
        prompt = (
            "Design an architecture blueprint as JSON for this project:\n\n"
            f"{message}\n\n"
            "JSON schema: {directories: [{path, responsibility}], "
            "interfaces: [{name, signature, description}], data_flow: [steps], notes: str}"
        )
        resp = self.backbone.reason(prompt, system=ARCHITECT_SYSTEM, task="architect")
        blueprint = self._parse(resp.text)
        content = json.dumps(blueprint, indent=2)
        actions = [f"defined {len(blueprint.get('directories', []))} directories",
                   f"defined {len(blueprint.get('interfaces', []))} interfaces"]
        return AgentResult(
            self.name, self.capability, content, actions=actions,
            artifacts=[{"type": "blueprint", "blueprint": blueprint}],
        )

    def _parse(self, text: str) -> dict[str, Any]:
        import re
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            return {"directories": [], "interfaces": [], "data_flow": [], "notes": text}
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            return {"directories": [], "interfaces": [], "data_flow": [],
                    "notes": "Failed to parse blueprint; raw text returned.",
                    "raw": text}
