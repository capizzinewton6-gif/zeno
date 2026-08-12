"""Code formatting integration (Prettier, Black, rustfmt)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from capabilities.terminal_execution import CommandResult, TerminalExecution


@dataclass
class FormatResult:
    ok: bool
    formatted: str = ""
    tool: str = ""
    message: str = ""


class FormattingEngine:
    """Dispatches to the right formatter per language."""

    FORMATTERS = {
        "python": "ruff format",
        "javascript": "prettier",
        "typescript": "prettier",
        "rust": "rustfmt",
        "go": "gofmt",
        "cpp": "clang-format",
        "java": "google-java-format",
        "json": "prettier",
        "yaml": "prettier",
        "html": "prettier",
        "css": "prettier",
    }

    def __init__(self, terminal: TerminalExecution | None = None,
                 workspace: str = ".") -> None:
        self.terminal = terminal or TerminalExecution(workspace=workspace)
        self.workspace = workspace

    def format_file(self, path: str, language: str) -> FormatResult:
        cmd = self.FORMATTERS.get(language.lower())
        if not cmd:
            return FormatResult(ok=False, message=f"no formatter for {language}")
        result = self.terminal.run(f"{cmd} {path}")
        return FormatResult(ok=result.ok, tool=cmd, message=result.stderr or "formatted")

    def format_source(self, source: str, language: str) -> FormatResult:
        """Format a source string by writing to a temp file."""
        import tempfile
        import os
        ext = {"python": ".py", "javascript": ".js", "typescript": ".ts",
               "rust": ".rs", "go": ".go", "cpp": ".cpp", "java": ".java"}.get(language, ".txt")
        with tempfile.NamedTemporaryFile("w", suffix=ext, delete=False, dir=self.workspace) as f:
            f.write(source)
            tmp = f.name
        try:
            res = self.format_file(tmp, language)
            if res.ok:
                with open(tmp, encoding="utf-8") as f:
                    return FormatResult(ok=True, formatted=f.read(), tool=res.tool)
            return res
        finally:
            os.unlink(tmp)
