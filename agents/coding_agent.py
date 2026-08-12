"""Primary software engineer for code writing and editing."""
from __future__ import annotations

from typing import Any

from agents.base import AgentResult, BaseAgent
from capabilities.code_synthesis import CodeSynthesis


class CodingAgent(BaseAgent):
    name = "coding"
    capability = "code_synthesis"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.synthesis = CodeSynthesis(self.backbone, self.safety, self.workspace)

    def _execute(self, message: str, **kwargs: Any) -> AgentResult:
        plan = kwargs.get("plan")
        language = kwargs.get("language", "python")
        filename = kwargs.get("filename")

        spec = message
        if plan and plan.tasks:
            spec = plan.tasks[0].description or message

        file = self.synthesis.generate(spec, language=language, filename=filename)
        patch = self.synthesis.write_file(file, overwrite=kwargs.get("overwrite", False))

        return AgentResult(
            agent=self.name, capability=self.capability,
            content=file.content,
            actions=[f"wrote {patch.path} (+{patch.additions}/-{patch.deletions})"],
            artifacts=[{"path": file.path, "language": file.language}],
            error=patch.error or None,
        )

    def edit(self, message: str, path: str, patch: str) -> dict[str, Any]:
        result = self.synthesis.apply_patch(path, patch)
        return AgentResult(
            self.name, self.capability, "",
            actions=[f"patched {result.path} (+{result.additions}/-{result.deletions})"],
            error=result.error or None,
        ).to_dict()
