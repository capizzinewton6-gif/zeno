"""Code reviewer for security patterns, style guides, and efficiency."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from agents.base import AgentResult, BaseAgent
from modeling.ast_manager import ASTManager
from modeling.coding_rules import ruleset_for

REVIEW_SYSTEM = (
    "You are a rigorous code reviewer. Review the code for: security, "
    "correctness, style, and efficiency. Output JSON: {issues: [{severity, "
    "category, line, message, suggestion}], summary, score (0-100)}."
)

SEVERITIES = ("critical", "high", "medium", "low", "info")


@dataclass
class ReviewIssue:
    severity: str
    category: str
    line: int
    message: str
    suggestion: str = ""


@dataclass
class ReviewReport:
    issues: list[ReviewIssue] = field(default_factory=list)
    summary: str = ""
    score: int = 100

    @property
    def passed(self) -> bool:
        return self.score >= 70 and not any(i.severity == "critical" for i in self.issues)


class ReviewAgent(BaseAgent):
    name = "review"
    capability = "code_explainer"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.ast = ASTManager()

    def _execute(self, message: str, **kwargs: Any) -> AgentResult:
        source = kwargs.get("source") or message
        language = kwargs.get("language", "python")
        rules = ruleset_for(language)

        prompt = (
            f"Review this {language} code against these rules: {rules.rules}.\n\n"
            f"# Source\n{source}\n\nReturn JSON review."
        )
        resp = self.backbone.reason(prompt, system=REVIEW_SYSTEM, task="review")
        report = self._parse(resp.text)
        content = json.dumps(
            {"summary": report.summary, "score": report.score,
             "issues": [i.__dict__ for i in report.issues]}, indent=2)
        return AgentResult(
            self.name, self.capability, content=content,
            actions=[f"found {len(report.issues)} issues, score {report.score}"],
            artifacts=[{"type": "review", "report": report.__dict__,
                        "passed": report.passed}],
        )

    def _parse(self, text: str) -> ReviewReport:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            return ReviewReport(summary="Could not parse review.", score=50)
        try:
            data = json.loads(m.group(0))
        except json.JSONDecodeError:
            return ReviewReport(summary="Malformed review JSON.", score=50)
        issues = [ReviewIssue(
            severity=i.get("severity", "info"),
            category=i.get("category", "general"),
            line=int(i.get("line", 0) or 0),
            message=i.get("message", ""),
            suggestion=i.get("suggestion", ""),
        ) for i in data.get("issues", [])]
        return ReviewReport(
            issues=issues,
            summary=data.get("summary", ""),
            score=int(data.get("score", 100)),
        )
