"""HTML, CSS, Tailwind, React, and Vue framework support."""
from __future__ import annotations

import re
from languages.base import ExecResult, LanguageEngine, LintResult


class WebStackEngine(LanguageEngine):
    name = "web"
    extensions = (".html", ".htm", ".css", ".scss")

    def required_tools(self) -> list[str]:
        return ["node", "npm", "prettier", "eslint"]

    def lint(self, path: str) -> LintResult:
        warnings: list[str] = []
        try:
            with open(path, encoding="utf-8") as f:
                content = f.read()
        except OSError:
            return LintResult(ok=False, errors=["file not readable"])
        if path.endswith((".html", ".htm")):
            if "<img" in content and 'alt=' not in content:
                warnings.append("Images missing alt attributes (accessibility)")
            if re.search(r"<style", content):
                warnings.append("Inline styles detected")
        if path.endswith((".css", ".scss")):
            if "!important" in content:
                warnings.append("Use of !important detected")
        return LintResult(ok=True, warnings=warnings)

    def format(self, path: str) -> LintResult:
        prettier = self._bin("prettier")
        if not prettier:
            return LintResult(ok=True, warnings=["prettier not installed"])
        result = self._exec(f"{prettier} --write {path}")
        return LintResult(ok=result.ok, errors=[result.stderr] if result.stderr else [])

    def run(self, path: str) -> ExecResult:
        # Web files aren't "run"; serve via a dev server if available
        return ExecResult(False, -1, "", "web files are not directly executable; use a dev server")

    def detect_framework(self, path: str) -> str | None:
        try:
            with open(path, encoding="utf-8") as f:
                content = f.read().lower()
        except OSError:
            return None
        if "react" in content or "jsx" in content:
            return "react"
        if "vue" in content:
            return "vue"
        if "@tailwind" in content or "tailwind" in content:
            return "tailwind"
        if "<html" in content:
            return "html"
        return None
