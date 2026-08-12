"""Stack trace interpreter, root-cause analyzer, and patch applier."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from agents.base import AgentResult, BaseAgent

DEBUG_SYSTEM = (
    "You are a debugging specialist. Given an error and its stack trace, "
    "perform: (1) root-cause analysis, (2) a precise fix, (3) a verification "
    "step. Return JSON: {root_cause, fix, verification, patched_code}."
)


@dataclass
class BugAnalysis:
    root_cause: str
    fix: str
    verification: str
    patched_code: str = ""


class DebuggingAgent(BaseAgent):
    name = "debugging"
    capability = "code_synthesis"

    def _execute(self, message: str, **kwargs: Any) -> AgentResult:
        stack_trace = kwargs.get("stack_trace", "")
        source = kwargs.get("source", "")
        language = kwargs.get("language", "python")

        trace = self.parse_stack_trace(stack_trace or message)
        prompt = (
            f"# Error\n{message}\n\n# Stack trace\n{trace.summary or stack_trace}\n\n"
            f"# Source\n{source[:3000]}\n\n# Language\n{language}\n\n"
            "Provide root-cause analysis and a patched version. JSON format."
        )
        resp = self.backbone.reason(prompt, system=DEBUG_SYSTEM, task="debug")
        analysis = self._parse(resp.text, message)
        return AgentResult(
            self.name, self.capability,
            content=analysis.patched_code or analysis.fix,
            actions=[
                f"root cause: {analysis.root_cause[:80]}",
                f"proposed fix: {analysis.fix[:80]}",
            ],
            artifacts=[{"type": "bug_analysis", "analysis": analysis.__dict__,
                        "trace": trace.frames}],
        )

    def parse_stack_trace(self, trace: str) -> "StackTrace":
        """Extract frames from a Python-style traceback."""
        frames: list[dict[str, Any]] = []
        for m in re.finditer(
            r'File "(?P<file>[^"]+)", line (?P<line>\d+), in (?P<func>\S+)',
            trace,
        ):
            frames.append({"file": m.group("file"), "line": int(m.group("line")),
                           "func": m.group("func")})
        exc = ""
        exc_match = re.search(r"^(\w*(?:Error|Exception|Warning)):\s*(.*)$", trace, re.MULTILINE)
        if exc_match:
            exc = f"{exc_match.group(1)}: {exc_match.group(2)}"
        return StackTrace(frames=frames, summary=exc, raw=trace)

    def _parse(self, text: str, fallback: str) -> BugAnalysis:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            return BugAnalysis(root_cause=fallback, fix=text, verification="")
        import json
        try:
            data = json.loads(m.group(0))
            return BugAnalysis(
                root_cause=data.get("root_cause", ""),
                fix=data.get("fix", ""),
                verification=data.get("verification", ""),
                patched_code=data.get("patched_code", ""),
            )
        except json.JSONDecodeError:
            return BugAnalysis(root_cause=fallback, fix=text, verification="")


@dataclass
class StackTrace:
    frames: list[dict[str, Any]]
    summary: str
    raw: str
