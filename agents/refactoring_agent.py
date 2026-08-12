"""Code modernization, dead code removal, and performance optimization."""
from __future__ import annotations

from typing import Any

from agents.base import AgentResult, BaseAgent
from capabilities.code_synthesis import CodeSynthesis
from modeling.ast_manager import ASTManager

REFACTOR_SYSTEM = (
    "You are a refactoring specialist. Improve code for readability, modernity, "
    "and performance WITHOUT changing behavior. Apply standard patterns, remove "
    "dead code, and use idiomatic constructs. Return the FULL refactored source."
)


class RefactoringAgent(BaseAgent):
    name = "refactoring"
    capability = "code_synthesis"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.synthesis = CodeSynthesis(self.backbone, self.safety, self.workspace)
        self.ast = ASTManager()

    def _execute(self, message: str, **kwargs: Any) -> AgentResult:
        source = kwargs.get("source") or message
        language = kwargs.get("language", "python")
        focus = kwargs.get("focus", "readability")  # readability, modernize, performance, dead-code

        prompt = (
            f"Refactor the following {language} code focusing on {focus}.\n"
            "Preserve behavior. Return the full refactored source only.\n\n"
            f"{source}"
        )
        resp = self.backbone.reason(prompt, system=REFACTOR_SYSTEM, task="refactor")
        refactored = self._strip_fence(resp.text) or source

        actions = self._summarize_changes(source, refactored, focus)
        return AgentResult(
            self.name, self.capability, content=refactored,
            actions=actions,
            artifacts=[{"type": "refactored_source", "language": language}],
        )

    def _summarize_changes(self, before: str, after: str, focus: str) -> list[str]:
        before_lines = before.splitlines()
        after_lines = after.splitlines()
        delta = len(after_lines) - len(before_lines)
        return [
            f"refactored for {focus}",
            f"line delta: {delta:+d} ({len(before_lines)} -> {len(after_lines)})",
        ]

    def _strip_fence(self, text: str) -> str | None:
        import re
        m = re.search(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
        return m.group(1) if m else None
