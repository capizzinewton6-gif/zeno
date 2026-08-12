"""Node/Bun execution, TypeScript compiler, and ESLint integration."""
from __future__ import annotations

from languages.base import ExecResult, LanguageEngine, LintResult


class JavaScriptEngine(LanguageEngine):
    name = "javascript"
    extensions = (".js", ".jsx", ".mjs", ".cjs")

    def required_tools(self) -> list[str]:
        return ["node", "npm", "eslint", "tsc", "bun"]

    def runtime(self) -> str:
        return self._bin("bun") or self._bin("node") or "node"

    def lint(self, path: str) -> LintResult:
        eslint = self._bin("eslint")
        if not eslint:
            return LintResult(ok=True, warnings=["eslint not installed"])
        result = self._exec(f"{eslint} --format compact {path}")
        errors, warnings = [], []
        for line in result.stdout.splitlines():
            if "error" in line.lower():
                errors.append(line)
            elif "warning" in line.lower():
                warnings.append(line)
        return LintResult(ok=result.ok, errors=errors, warnings=warnings)

    def format(self, path: str) -> LintResult:
        prettier = self._bin("prettier")
        if not prettier:
            return LintResult(ok=True, warnings=["prettier not installed"])
        result = self._exec(f"{prettier} --write {path}")
        return LintResult(ok=result.ok, errors=[result.stderr] if result.stderr else [])

    def run(self, path: str) -> ExecResult:
        return self._exec(f"{self.runtime()} {path}")

    def typecheck(self, path: str) -> LintResult:
        tsc = self._bin("tsc")
        if not tsc:
            return LintResult(ok=True, warnings=["tsc not installed"])
        result = self._exec(f"{tsc} --noEmit {path}")
        return LintResult(ok=result.ok, errors=result.stdout.splitlines())


class TypeScriptEngine(JavaScriptEngine):
    name = "typescript"
    extensions = (".ts", ".tsx")

    def run(self, path: str) -> ExecResult:
        # Prefer bun for direct TS execution, fall back to tsx/tsc + node
        bun = self._bin("bun")
        if bun:
            return self._exec(f"{bun} {path}")
        tsc = self._bin("tsc")
        if tsc:
            return self._exec(f"{tsc} {path} && node {path.replace('.ts', '.js')}")
        return ExecResult(False, -1, "", "no TS runtime available")
