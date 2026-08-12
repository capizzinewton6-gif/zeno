"""Automated test suite generator (unit, integration, regression)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from agents.base import AgentResult, BaseAgent
from modeling.ast_manager import ASTManager

TEST_SYSTEM = (
    "You are a test engineer. Generate comprehensive tests for the given code. "
    "Cover happy paths, edge cases, and error conditions. Use idiomatic test "
    "frameworks (pytest for Python, jest for JS/TS). Return only test code."
)


@dataclass
class TestSuite:
    framework: str
    file_path: str
    code: str
    cases: list[str] = field(default_factory=list)


class TestingAgent(BaseAgent):
    name = "testing"
    capability = "code_synthesis"

    FRAMEWORKS = {"python": "pytest", "javascript": "jest", "typescript": "jest",
                  "rust": "cargo test", "go": "go test"}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.ast = ASTManager()

    def _execute(self, message: str, **kwargs: Any) -> AgentResult:
        source = kwargs.get("source") or message
        language = kwargs.get("language", "python")
        test_type = kwargs.get("test_type", "unit")  # unit, integration, regression

        symbols = self.ast.parse(source, language).symbols
        targets = [s.name for s in symbols if s.kind in ("function", "method", "class")]
        framework = self.FRAMEWORKS.get(language, "pytest")

        prompt = (
            f"Generate {test_type} tests using {framework} for this {language} code.\n"
            f"# Targets\n{', '.join(targets) or 'general behavior'}\n\n"
            f"# Source\n{source}\n\nReturn only the test file."
        )
        resp = self.backbone.reason(prompt, system=TEST_SYSTEM, task="test")
        code = self._strip_fence(resp.text) or resp.text
        cases = self._extract_cases(code, framework)

        suite = TestSuite(framework=framework,
                          file_path=self._test_path(source, language), code=code, cases=cases)
        return AgentResult(
            self.name, self.capability, content=code,
            actions=[f"generated {len(cases)} {test_type} cases with {framework}"],
            artifacts=[{"type": "test_suite", **suite.__dict__}],
        )

    def _strip_fence(self, text: str) -> str | None:
        m = re.search(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
        return m.group(1) if m else None

    def _extract_cases(self, code: str, framework: str) -> list[str]:
        if framework == "pytest":
            return re.findall(r"def (test_\w+)\(", code)
        if framework == "jest":
            return re.findall(r"(?:it|test)\(['\"]([^'\"]+)", code)
        return []

    def _test_path(self, source: str, language: str) -> str:
        if language == "python":
            return "test_module.py"
        if language in ("javascript", "typescript"):
            return "module.test.js"
        return "tests"
