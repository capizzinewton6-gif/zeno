"""Cross-platform Bash/PowerShell script analyzer."""
from __future__ import annotations

import re
from languages.base import ExecResult, LanguageEngine, LintResult


class ShellScriptingEngine(LanguageEngine):
    name = "bash"
    extensions = (".sh", ".bash")

    def required_tools(self) -> list[str]:
        return ["bash", "shellcheck"]

    def lint(self, path: str) -> LintResult:
        shellcheck = self._bin("shellcheck")
        if not shellcheck:
            return self._heuristic_lint(path)
        result = self._exec(f"{shellcheck} --format=gcc {path}")
        errors, warnings = [], []
        for line in result.stdout.splitlines():
            if ": error" in line:
                errors.append(line)
            elif ": warning" in line or ": note" in line:
                warnings.append(line)
        return LintResult(ok=result.ok, errors=errors, warnings=warnings)

    def format(self, path: str) -> LintResult:
        shfmt = self._bin("shfmt")
        if not shfmt:
            return LintResult(ok=True, warnings=["shfmt not installed"])
        result = self._exec(f"{shfmt} -i 4 -w {path}")
        return LintResult(ok=result.ok, errors=[result.stderr] if result.stderr else [])

    def run(self, path: str) -> ExecResult:
        bash = self._bin("bash")
        if not bash:
            return ExecResult(False, -1, "", "bash not installed")
        return self._exec(f"{bash} {path}")

    def _heuristic_lint(self, path: str) -> LintResult:
        warnings: list[str] = []
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.readlines()
        except OSError:
            return LintResult(ok=False, errors=["file not readable"])
        for i, line in enumerate(lines, 1):
            if re.search(r"\brm\s+-rf\b", line) and "$" in line:
                warnings.append(f"line {i}: rm -rf with variable expansion (dangerous)")
            if line.strip().startswith("eval "):
                warnings.append(f"line {i}: eval usage is dangerous")
            if "$" in line and '"' not in line and "'" not in line and "=" in line:
                warnings.append(f"line {i}: unquoted variable (use \"\")")
        return LintResult(ok=True, warnings=warnings)


class PowerShellEngine(ShellScriptingEngine):
    name = "powershell"
    extensions = (".ps1",)

    def required_tools(self) -> list[str]:
        return ["pwsh", "powershell"]

    def run(self, path: str) -> ExecResult:
        pwsh = self._bin("pwsh") or self._bin("powershell")
        if not pwsh:
            return ExecResult(False, -1, "", "powershell not installed")
        return self._exec(f"{pwsh} -File {path}")

    def lint(self, path: str) -> LintResult:
        # PSScriptAnalyzer when available; heuristic otherwise
        pwsh = self._bin("pwsh")
        if pwsh:
            result = self._exec(
                f'{pwsh} -Command "Invoke-ScriptAnalyzer {path}"')
            return LintResult(ok=result.ok, warnings=result.stdout.splitlines())
        return LintResult(ok=True, warnings=["PSScriptAnalyzer not available"])
