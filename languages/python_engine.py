"""Python AST manipulation, execution, and Ruff linter."""
from __future__ import annotations

import ast
from typing import Any

from languages.base import ExecResult, LanguageEngine, LintResult


class PythonEngine(LanguageEngine):
    name = "python"
    extensions = (".py",)

    def required_tools(self) -> list[str]:
        return ["python", "ruff"]

    def lint(self, path: str) -> LintResult:
        ruff = self._bin("ruff")
        if not ruff:
            # Fall back to py_compile for syntax checking
            return self._syntax_check(path)
        result = self._exec(f"{ruff} check --output-format=concise {path}")
        errors, warnings, fixable = [], [], 0
        for line in (result.stdout + result.stderr).splitlines():
            if path in line:
                errors.append(line)
            elif line.strip().startswith("Found"):
                fixable = int(any(c.isdigit() for c in line))
        return LintResult(ok=result.ok, errors=errors, warnings=warnings, fixable=fixable)

    def format(self, path: str) -> LintResult:
        ruff = self._bin("ruff")
        if not ruff:
            return LintResult(ok=True, warnings=["ruff not installed; skipping format"])
        result = self._exec(f"{ruff} format {path}")
        return LintResult(ok=result.ok, errors=[result.stderr] if result.stderr else [])

    def run(self, path: str) -> ExecResult:
        python = self._bin("python") or "python3"
        return self._exec(f"{python} {path}")

    def parse_ast(self, source: str) -> ast.AST | None:
        try:
            return ast.parse(source)
        except SyntaxError:
            return None

    def list_symbols(self, source: str) -> list[str]:
        tree = self.parse_ast(source)
        if not tree:
            return []
        return [n.name for n in ast.walk(tree)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]

    def _syntax_check(self, path: str) -> LintResult:
        import py_compile
        try:
            py_compile.compile(path, doraise=True)
            return LintResult(ok=True)
        except py_compile.PyCompileError as exc:
            return LintResult(ok=False, errors=[str(exc)])
