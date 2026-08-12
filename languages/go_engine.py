"""Go static analysis, formatting, and module management."""
from __future__ import annotations

from languages.base import ExecResult, LanguageEngine, LintResult


class GoEngine(LanguageEngine):
    name = "go"
    extensions = (".go",)

    def required_tools(self) -> list[str]:
        return ["go", "golangci-lint"]

    def lint(self, path: str) -> LintResult:
        go = self._bin("go")
        if not go:
            return LintResult(ok=True, warnings=["go not installed"])
        vet = self._exec(f"{go} vet {path}")
        errors = vet.stderr.splitlines() if not vet.ok else []
        golangci = self._bin("golangci-lint")
        warnings: list[str] = []
        if golangci:
            lint_res = self._exec(f"{golangci} run {path}")
            warnings = [l for l in lint_res.stdout.splitlines() if l.strip()]
        return LintResult(ok=vet.ok, errors=errors, warnings=warnings)

    def format(self, path: str) -> LintResult:
        go = self._bin("go")
        if not go:
            return LintResult(ok=True, warnings=["go not installed"])
        result = self._exec(f"{go} fmt {path}")
        return LintResult(ok=result.ok, errors=[result.stderr] if result.stderr else [])

    def run(self, path: str) -> ExecResult:
        go = self._bin("go")
        if not go:
            return ExecResult(False, -1, "", "go not installed")
        if path.endswith(".go"):
            return self._exec(f"{go} run {path}")
        return self._exec(f"{go} run .")

    def mod_tidy(self) -> ExecResult:
        go = self._bin("go")
        if not go:
            return ExecResult(False, -1, "", "go not installed")
        return self._exec(f"{go} mod tidy")
